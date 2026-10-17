# 좀보이드 B42 모드팩 정적 호환성 분석
#
#   python -I mod_analyze.py --game <PZ 설치 폴더> --content <workshop/content/108600>
#                            --mods-json data/mods.json [--add 3812345678[:ModA,ModB]] --out <출력 폴더>
#
# 게임 jar 와 바닐라 Lua 를 기준으로 팩 전체(+ 후보)를 대조해 report.json 과 report.md 를 쓴다.
# 게임 규칙(버전 폴더 선택, require 앞당김, 파일 덮어쓰기 순서)은 42.21 jar 디컴파일로 확인한 것을
# 그대로 옮겼다. 근거 클래스는 references/game-rules.md 에 있다.
import argparse, collections, json, os, re, struct, sys, zipfile

ap = argparse.ArgumentParser()
ap.add_argument('--game', required=True)
ap.add_argument('--content', required=True, help='steamapps/workshop/content/108600')
ap.add_argument('--mods-json', required=True)
ap.add_argument('--add', action='append', default=[], help='후보 창작마당 번호[:Mod ID,...] (여러 번 가능)')
ap.add_argument('--out', required=True)
ap.add_argument('--game-version', help='예: 42.21 (없으면 ~/Zomboid/version.txt)')
args = ap.parse_args()

PZ, WS, OUT = args.game, args.content, args.out
os.makedirs(OUT, exist_ok=True)


def read_text(path):
    with open(path, 'rb') as f:
        b = f.read()
    if b.startswith(b'\xef\xbb\xbf'):
        b = b[3:]
    return b.decode('utf-8', 'replace')


def game_version():
    """--game-version 이 없으면 게임이 마지막 실행 때 쓴 ~/Zomboid/version.txt 를 읽는다."""
    text = args.game_version
    path = os.path.join(os.path.expanduser('~'), 'Zomboid', 'version.txt')
    if not text and os.path.isfile(path):
        text = read_text(path).split()[0]
    m = re.match(r'^(\d+)\.(\d+)', text or '')
    if not m:
        sys.exit('게임 버전을 모른다. --game-version 42.21 처럼 넘긴다.')
    return int(m.group(1)), int(m.group(2)), text


GV_MAJOR, GV_MINOR, GV_TEXT = game_version()
GAME_VER = GV_MAJOR * 1000 + GV_MINOR


# ---------- 게임 규칙 (ZomboidFileSystem.getModVersionDirName / getGameVersionIntFromName) ----------
def ver_int(name):
    parts = name.split('.')

    def p(s):
        try:
            return int(s)
        except ValueError:
            return 0
    if len(parts) == 1:
        return p(parts[0]) * 1000
    return p(parts[0]) * 1000 + min(p(parts[1]), 999)


def version_dir_name(mod_dir):
    best_name, best = '42.0', 42000
    for name in sorted(os.listdir(mod_dir)):
        v = ver_int(name)
        if v < best or v > GAME_VER:
            continue
        best_name, best = name, v
    return best_name


def read_mod_info(path):
    info = {}
    for raw in read_text(path).splitlines():
        if '=' in raw:
            k, v = raw.split('=', 1)
            info.setdefault(k.strip().lower(), v.strip())
    return info


def id_list(s):
    return [x.strip().lstrip('\\').strip() for x in (s or '').split(',') if x.strip().lstrip('\\').strip()]


# ---------- 모드 찾기 ----------
avail, by_workshop = {}, collections.defaultdict(list)
for wid in sorted(os.listdir(WS)):
    mroot = os.path.join(WS, wid, 'mods')
    if not os.path.isdir(mroot):
        continue
    for folder in sorted(os.listdir(mroot)):
        mdir = os.path.join(mroot, folder)
        if not os.path.isdir(mdir):
            continue
        vname = version_dir_name(mdir)
        common, vdir = os.path.join(mdir, 'common'), os.path.join(mdir, vname)
        mi = next((c for c in (os.path.join(vdir, 'mod.info'), os.path.join(common, 'mod.info')) if os.path.isfile(c)), None)
        if not mi:
            continue
        info = read_mod_info(mi)
        mid = info.get('id', folder)
        avail[mid] = dict(workshop=wid, folder=folder, dir=mdir, common=common, vname=vname, vdir=vdir, info=info, info_path=mi)
        by_workshop[wid].append(mid)

pack = json.load(open(args.mods_json, encoding='utf-8'))
listed = [mid for m in sorted(pack['mods'], key=lambda m: m['loadOrder']) for mid in m['modIds']]
candidates = []
for a in args.add:
    wid, _, ids = a.partition(':')
    ids = [x for x in ids.split(',') if x] if ids else by_workshop.get(wid, [])
    if not by_workshop.get(wid):
        sys.exit('창작마당 %s 를 %s 에서 찾지 못했다. fetch_mods.py 로 먼저 받아라.' % (wid, WS))
    if not ids or (':' not in a and len(ids) > 1):
        sys.exit('창작마당 %s 에 Mod ID 가 여러 개다. --add %s:<ID,...> 로 고른다: %s' % (wid, wid, ', '.join(by_workshop[wid])))
    candidates += ids
listed += [c for c in candidates if c not in listed]

order, missing = [], []


def load_and_required(mid):
    """ZomboidFileSystem.loadModAndRequired 와 같다: require 를 먼저 넣는다."""
    if not mid or mid in order:
        return None
    if mid not in avail:
        missing.append(mid)
        return mid
    for r in id_list(avail[mid]['info'].get('require')):
        f = load_and_required(r)
        if f:
            return f
    order.append(mid)
    return None


for mid in listed:
    load_and_required(mid)


# ---------- 파일 덮어쓰기 (activeFileMap) ----------
def walk(root):
    out = {}
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            for f in fn:
                ap_ = os.path.join(dp, f)
                out[os.path.relpath(ap_, root).replace('\\', '/').lower()] = ap_
    return out


vanilla_media = {'media/' + rel: ap_ for rel, ap_ in walk(os.path.join(PZ, 'media')).items()}
active, mod_files, overrides, vanilla_overrides = {}, {}, [], []
for mid in order:
    m = avail[mid]
    files = {}
    for part in (m['common'], m['vdir']):
        files.update(walk(part))  # 같은 모드 안에서는 버전 폴더가 common 을 덮는다
    mod_files[mid] = files
    for rel, ap_ in files.items():
        if not rel.startswith('media/'):
            continue
        harmless = rel.startswith('media/lua/shared/translate/') or rel == 'media/sandbox-options.txt'
        if rel in active and active[rel][0] != mid:
            overrides.append(dict(path=rel, earlier=active[rel][0], later=mid, harmless=harmless))
        if rel in vanilla_media:
            vanilla_overrides.append(dict(mod=mid, path=rel, harmless=harmless))
        active[rel] = (mid, ap_)


# ---------- Lua 전처리 ----------
def strip_lua(src):
    """(주석만 지운 코드, 문자열까지 비운 코드). 줄 수는 유지한다."""
    out_c, out_s = [], []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith('--', i):
            m = re.match(r'--\[(=*)\[', src[i:i + 40])
            if m:
                end = src.find(']' + m.group(1) + ']', i + len(m.group(0)))
                end = n if end < 0 else end + len(m.group(1)) + 2
            else:
                end = src.find('\n', i)
                end = n if end < 0 else end
            blank = re.sub(r'[^\n]', ' ', src[i:end])
            out_c.append(blank); out_s.append(blank)
            i = end
            continue
        m = re.match(r'\[(=*)\[', src[i:i + 40]) if c == '[' else None
        if m:
            end = src.find(']' + m.group(1) + ']', i + len(m.group(0)))
            end = n if end < 0 else end + len(m.group(1)) + 2
            seg = src[i:end]
            out_c.append(seg); out_s.append('""' + re.sub(r'[^\n]', ' ', seg[2:]))
            i = end
            continue
        if c in '"\'':
            j = i + 1
            while j < n and src[j] != c and src[j] != '\n':
                j += 2 if src[j] == '\\' else 1
            j = min(j + 1, n)
            seg = src[i:j]
            out_c.append(seg); out_s.append(c + ' ' * max(len(seg) - 2, 0) + (c if len(seg) >= 2 else ''))
            i = j
            continue
        out_c.append(c); out_s.append(c)
        i += 1
    return ''.join(out_c), ''.join(out_s)


NAME = r'[A-Za-z_][A-Za-z0-9_]*'
PATH = NAME + r'(?:\s*[.:]\s*' + NAME + r')*'
re_def_func = re.compile(r'(?<![\w.])function\s+(' + PATH + r')\s*\(')
re_def_assign = re.compile(r'(?<![\w.:])(' + NAME + r'(?:\.' + NAME + r')+)\s*=(?!=)\s*(function\b|\{|' + PATH + r')')
# 들여쓰기 없는 최상위 대입만 전역으로 본다(함수 안의 o = ..., self.x = ... 를 빼려고)
re_global_table = re.compile(r'(?m)^(' + NAME + r')\s*=(?!=)')
RUNTIME_ROOTS = {'self', 'SandboxVars', 'ModData', 'Events'}  # 실행 중에 채워지거나 지역처럼 쓰는 이름
re_method_call = re.compile(r'[\w\)\]]\s*:\s*(' + NAME + r')\s*[\(\{"\']')
re_events = re.compile(r'\bEvents\s*\.\s*(' + NAME + r')\s*\.\s*(Add|Remove)\b')
re_add_event = re.compile(r'LuaEventManager\s*\.\s*AddEvent\s*\(\s*["\'](' + NAME + r')["\']')
re_require = re.compile(r'\brequire\s*\(?\s*["\']([^"\']+)["\']')
re_instanceof = re.compile(r'\binstanceof\s*\(\s*[^,]+,\s*["\'](' + NAME + r')["\']')
re_locals = re.compile(r'\blocal\s+(?:function\s+)?(' + NAME + r'(?:\s*,\s*' + NAME + r')*)')
re_params = re.compile(r'function\s*(?:' + PATH + r')?\s*\(([^)]*)\)')


def norm(path):
    return re.sub(r'\s*[.:]\s*', '.', path)


def line_of(text, pos):
    return text.count('\n', 0, pos) + 1


def lua_of(files):
    return {rel: ap_ for rel, ap_ in files.items() if rel.startswith('media/lua/') and rel.endswith('.lua')}


def file_locals(nostr):
    out = set()
    for grp in re_locals.findall(nostr):
        out.update(x.strip() for x in grp.split(','))
    for params in re_params.findall(nostr):
        out.update(x.strip() for x in params.split(',') if x.strip() and x.strip() != '...')
    for grp in re.findall(r'\bfor\s+([\w\s,]+?)\s+in\b', nostr) + re.findall(r'\bfor\s+(' + NAME + r')\s*=', nostr):
        out.update(x.strip() for x in grp.split(','))
    return out


def collect_defs(nostr, code, defs, fields, globals_, owner, funcs=None):
    for m in re_def_func.finditer(nostr):
        p = norm(m.group(1)); defs[p].add(owner); fields.add(p.split('.')[-1])
        if funcs is not None:
            funcs.add(p)
        if '.' not in p:
            globals_.add(p)
    for m in re_def_assign.finditer(nostr):
        p = norm(m.group(1)); defs[p].add(owner); fields.add(p.split('.')[-1])
        if funcs is not None and m.group(2) == 'function':
            funcs.add(p)
    for m in re_global_table.finditer(nostr):
        globals_.add(m.group(1))
    for m in re.finditer(r'\b(' + NAME + r')\s*=\s*function', nostr):
        fields.add(m.group(1))
    for m in re.finditer(r'[{,]\s*(' + NAME + r')\s*=', nostr):
        fields.add(m.group(1))
    for m in re.finditer(r'\[\s*["\'](' + NAME + r')["\']\s*\]\s*=', code):
        fields.add(m.group(1))


van_defs, van_fields, van_globals, van_funcs = collections.defaultdict(set), set(), set(), set()
van_lua = {rel: ap_ for rel, ap_ in vanilla_media.items() if rel.startswith('media/lua/') and rel.endswith('.lua')}
lua_events_added = set()
for rel, ap_ in van_lua.items():
    code, nostr = strip_lua(read_text(ap_))
    collect_defs(nostr, code, van_defs, van_fields, van_globals, rel, van_funcs)
    lua_events_added.update(re_add_event.findall(code))


# ---------- Java: 상수 풀만 읽는다 (디컴파일러 없이) ----------
def parse_class(b):
    if b[:4] != b'\xca\xfe\xba\xbe':
        return None
    i = 8
    cpn = struct.unpack('>H', b[i:i + 2])[0]; i += 2
    cp, strings, classrefs = [None] * cpn, [], []
    k = 1
    while k < cpn:
        t = b[i]; i += 1
        if t == 1:
            l = struct.unpack('>H', b[i:i + 2])[0]; i += 2
            cp[k] = b[i:i + l].decode('utf-8', 'replace'); i += l
        elif t in (3, 4):
            i += 4
        elif t in (5, 6):
            i += 8; k += 1
        elif t == 7:
            cp[k] = ('C', struct.unpack('>H', b[i:i + 2])[0]); classrefs.append(k); i += 2
        elif t == 8:
            cp[k] = ('S', struct.unpack('>H', b[i:i + 2])[0]); strings.append(k); i += 2
        elif t in (16, 19, 20):
            i += 2
        elif t in (9, 10, 11, 12, 17, 18):
            i += 4
        elif t == 15:
            i += 3
        else:
            raise ValueError(t)
        k += 1
    _, this_c, super_c = struct.unpack('>HHH', b[i:i + 6]); i += 6
    ic = struct.unpack('>H', b[i:i + 2])[0]; i += 2
    ifaces = [cp[cp[struct.unpack('>H', b[i + 2 * j:i + 2 * j + 2])[0]][1]] for j in range(ic)]
    i += 2 * ic

    def members(i):
        cnt = struct.unpack('>H', b[i:i + 2])[0]; i += 2
        out = []
        for _ in range(cnt):
            acc, ni, _ = struct.unpack('>HHH', b[i:i + 6]); i += 6
            out.append((cp[ni], acc))
            ac = struct.unpack('>H', b[i:i + 2])[0]; i += 2
            for _ in range(ac):
                l = struct.unpack('>I', b[i + 2:i + 6])[0]; i += 6 + l
        return out, i
    _, i = members(i)
    methods, i = members(i)
    return dict(name=cp[cp[this_c][1]], sup=cp[cp[super_c][1]] if super_c else None, ifaces=ifaces, methods=methods,
                strings=[cp[cp[x][1]] for x in strings], classrefs=[cp[cp[x][1]] for x in classrefs],
                utf8=[x for x in cp if isinstance(x, str)])


classes = {}
with zipfile.ZipFile(os.path.join(PZ, 'projectzomboid.jar')) as z:
    for e in z.namelist():
        if e.endswith('.class') and not e.startswith('META-INF/versions/'):
            try:
                r = parse_class(z.read(e))
            except Exception:
                continue
            if r:
                classes[r['name']] = r
simple_names = {fq.split('/')[-1].split('$')[-1] for fq in classes}
all_java_methods = {mn for c in classes.values() for mn, acc in c['methods']}
exposer = classes.get('zombie/Lua/LuaManager$Exposer')
exposed, stack = set(), list(exposer['classrefs']) if exposer else []
exposed_methods = set()
while stack:
    fq = stack.pop()
    if fq in exposed or fq not in classes:
        continue
    exposed.add(fq)
    c = classes[fq]
    exposed_methods.update(mn for mn, acc in c['methods'] if acc & 0x0001)
    stack.extend(([c['sup']] if c['sup'] else []) + c['ifaces'])
gobj = classes.get('zombie/Lua/LuaManager$GlobalObject')
global_funcs = {s for s in (gobj['utf8'] if gobj else []) if re.fullmatch(NAME, s)}
lem = classes.get('zombie/Lua/LuaEventManager')
java_events = {s for s in (lem['strings'] if lem else []) if re.fullmatch(r'[A-Z][A-Za-z0-9_]+', s)}

LUA_STD = set('''print pairs ipairs next type tostring tonumber error assert pcall xpcall select unpack rawget rawset rawequal
setmetatable getmetatable require loadstring loadfile dofile string table math os coroutine getfenv setfenv collectgarbage
instanceof _G self'''.split())
LUA_KEYWORDS = set('function if elseif while until return and or not local for in repeat then do end else'.split())
STR_METHODS = set('byte char find format gmatch gsub len lower match rep reverse sub upper trim split contains startsWith endsWith'.split())
JAVA_STD = set('''size get add remove isEmpty contains clear indexOf set put containsKey containsValue keySet values iterator hasNext next
toString equals hashCode getClass addAll removeAll entrySet getKey getValue sort length charAt intValue floatValue doubleValue
longValue booleanValue compareTo name ordinal getName getSimpleName close readLine write newLine flush getFirst getLast
removeFirst removeLast push pop peek toArray subList lastIndexOf replace substring startsWith endsWith toLowerCase toUpperCase
isBlank'''.split())

# ---------- 모드 Lua ----------
scans, mod_defs, mod_fields, mod_globals = {}, collections.defaultdict(set), set(), set()
for mid in order:
    for rel, ap_ in lua_of(mod_files[mid]).items():
        if active.get(rel, (None,))[0] != mid:
            continue  # 다른 모드에 덮여 실행되지 않는 파일
        code, nostr = strip_lua(read_text(ap_))
        scans[(mid, rel)] = (code, nostr)
        collect_defs(nostr, code, mod_defs, mod_fields, mod_globals, mid)
        lua_events_added.update(re_add_event.findall(code))
all_lua_paths = set(van_lua) | {rel for (_, rel) in scans}
known_events = java_events | lua_events_added

R = dict(game_version=GV_TEXT, candidates=candidates, missing=missing, load_order=[], profiles={}, overrides=overrides,
         vanilla_overrides=vanilla_overrides, patches=collections.defaultdict(list), shared_patches=[], missing_targets=[],
         unknown_events=[], missing_requires=[], bad_instanceof=[], unknown_methods=[], subfolder_lua=[], duplicate_event_handlers=[],
         scripts={}, script_conflicts=[], json_errors=[], translation_key_conflicts={}, sandbox_options={}, sandbox_conflicts=[],
         incompatible_hits=[], binaries=[])

for (mid, rel), (code, nostr) in scans.items():
    loc = file_locals(nostr)
    # 바닐라 함수 다시 정의 → 감싸기(wrap)인지 교체(replace)인지
    for rx in (re_def_func, re_def_assign):
        for m in rx.finditer(nostr):
            t = norm(m.group(1))
            if '.' not in t or t not in van_funcs:
                continue  # 바닐라에서 함수로 정의된 이름만 본다(값 필드 대입은 패치가 아니다)
            root = t.split('.')[0]
            if root not in van_globals or root in loc or root in RUNTIME_ROOTS:
                continue  # 지역 변수(o, self, option 등)를 바닐라 함수로 잘못 잡지 않는다
            if rx is re_def_assign and m.group(2) == '{':
                continue
            a, b = t.rsplit('.', 1)
            cap = re.search(r'=\s*' + re.escape(a).replace(r'\.', r'\s*\.\s*') + r'\s*[.:]\s*' + re.escape(b) + r'\b(?!\s*\()', nostr) \
                or re.search(re.escape(a) + r'\s*\[\s*["\']' + re.escape(b) + r'["\']\s*\]', code)
            R['patches'][t].append(dict(mod=mid, file=rel, line=line_of(nostr, m.start()), kind='wrap' if cap else 'replace'))
    for m in re_events.finditer(nostr):
        if m.group(1) not in known_events:
            R['unknown_events'].append(dict(mod=mid, file=rel, line=line_of(nostr, m.start()), event=m.group(1)))
    for m in re_require.finditer(code):
        name = m.group(1).replace('\\', '/').lower()
        name = name[:-4] if name.endswith('.lua') else name
        if not any(p.endswith('/' + name + '.lua') for p in all_lua_paths):
            R['missing_requires'].append(dict(mod=mid, file=rel, line=line_of(code, m.start()), require=m.group(1)))
    for m in re_instanceof.finditer(code):
        if m.group(1) not in simple_names:
            R['bad_instanceof'].append(dict(mod=mid, file=rel, line=line_of(code, m.start()), cls=m.group(1)))
    for m in re_method_call.finditer(nostr):
        nm = m.group(1)
        if nm in exposed_methods or nm in van_fields or nm in mod_fields or nm in STR_METHODS or nm in JAVA_STD:
            continue
        R['unknown_methods'].append(dict(mod=mid, file=rel, line=line_of(nostr, m.start()), name=nm,
                                         in_java=nm in all_java_methods))
    # 감싸려고 잡아 둔 함수가 바닐라·모드 어디에도 없다 (빌드가 바뀌며 사라진 함수)
    for m in re.finditer(r'\blocal\s+(' + NAME + r')\s*=\s*(' + NAME + r'(?:\s*[.:]\s*' + NAME + r')+)\s*(?=$|[\n;]|\s+local\b|\s+--)', nostr, re.M):
        t = norm(m.group(2))
        root, leaf = t.split('.')[0], t.split('.')[-1]
        if root in LUA_STD or root in loc or root in RUNTIME_ROOTS or root not in van_globals | mod_globals:
            continue
        if t in van_defs or t in mod_defs or leaf in exposed_methods or leaf in van_fields or leaf in mod_fields:
            continue
        R['missing_targets'].append(dict(mod=mid, file=rel, line=line_of(nostr, m.start()), local=m.group(1), target=t))

# UTF-8 바이트를 가정한 문자열 처리. Kahlua 문자열은 Java 문자열이라 한글이 한 글자(U+AC00~)로 들어와서
# s:byte 로 UTF-8 을 풀거나 string.char 로 바이트를 다시 붙이면 한글이 깨진다(SRJ #154 를 42.21 에서 재현함).
R['utf8_byte_code'] = []
for (mid, rel), (code, nostr) in scans.items():
    if re.search(r':\s*byte\s*\(|string\.byte\s*\(', nostr) and re.search(r'0x[CcEeFf]0\b|\b(192|224|240)\b', nostr):
        R['utf8_byte_code'].append(dict(mod=mid, file=rel, line=line_of(nostr, re.search(r':\s*byte\s*\(|string\.byte\s*\(', nostr).start())))

for t, sites in R['patches'].items():
    mods_here = list(dict.fromkeys(s['mod'] for s in sites))
    if len(mods_here) > 1:
        R['shared_patches'].append(dict(target=t, sites=sites))

# 하위 폴더에 같은 전역 클래스·이벤트 핸들러를 다시 정의한 파일(Stack All 의 "New folder" 같은 잔여물)
for mid in order:
    by_global = collections.defaultdict(list)
    for (m_, rel), (code, nostr) in scans.items():
        if m_ != mid:
            continue
        for m in re.finditer(r'(?m)^(' + NAME + r')\s*=\s*' + NAME + r'\s*:\s*derive\s*\(', nostr):
            by_global[m.group(1)].append(rel)
        for m in re.finditer(r'(?m)^function\s+(' + NAME + r')\s*\(', nostr):
            by_global[m.group(1)].append(rel)
    for g, rels in by_global.items():
        if len(set(rels)) > 1:
            R['subfolder_lua'].append(dict(mod=mid, global_=g, files=sorted(set(rels)), winner=sorted(set(rels))[-1]))


# ---------- 스크립트(아이템·레시피 등) ----------
re_block = re.compile(r'(?im)^\s*(item|craftRecipe|recipe|entity|fluid|model|sound|vehicle|xuiSkin|template|fixing|evolvedrecipe|timedAction)\s+([A-Za-z0-9_.\-]+)\s*\n?\s*\{')


def script_defs(ap_):
    t = re.sub(r'/\*.*?\*/', '', read_text(ap_), flags=re.S)
    mm = re.findall(r'(?im)^\s*module\s+(\w+)', t)
    return {(mm[0] if mm else '?', k.lower(), n) for k, n in re_block.findall(t)}


van_script = {}
for rel, ap_ in vanilla_media.items():
    if rel.startswith('media/scripts/') and rel.endswith('.txt'):
        for d in script_defs(ap_):
            van_script.setdefault(d, rel)
owners = collections.defaultdict(list)
for mid in order:
    defs = set()
    for rel, ap_ in mod_files[mid].items():
        if rel.startswith('media/scripts/') and rel.endswith('.txt') and active.get(rel, (None,))[0] == mid:
            for d in script_defs(ap_):
                defs.add(d); owners[d].append(mid)
    if defs:
        R['scripts'][mid] = dict(count=len(defs), kinds=dict(collections.Counter(k for _, k, _ in defs)),
                                 overrides_vanilla=sorted('%s %s.%s' % (k, a, n) for a, k, n in defs if (a, k, n) in van_script))
for d, ms in owners.items():
    if len(set(ms)) > 1:
        R['script_conflicts'].append(dict(defn='%s %s.%s' % (d[1], d[0], d[2]), mods=sorted(set(ms))))

# ---------- 번역 ----------
key_vals = collections.defaultdict(list)
for mid in order:
    for rel, ap_ in mod_files[mid].items():
        m = re.match(r'media/lua/shared/translate/([a-z_\-]+)/([^/]+)\.json$', rel)
        if not m:
            continue
        try:
            data = json.loads(read_text(ap_))
        except Exception as ex:
            lenient = True
            try:
                data = json.loads(re.sub(r',\s*([}\]])', r'\1', read_text(ap_)))
            except Exception:
                lenient = False
                data = None
            R['json_errors'].append(dict(mod=mid, file=rel, error=str(ex)[:120], game_accepts_trailing_comma=lenient))
        if isinstance(data, dict) and m.group(1) == 'ko':
            for k, v in data.items():
                key_vals[(m.group(2), k)].append((mid, str(v)))
pairs = collections.Counter()
for (f, k), vals in key_vals.items():
    ms = list(dict.fromkeys(mid for mid, _ in vals))
    if len(ms) > 1 and len({v for _, v in vals}) > 1:
        pairs['%s -> %s' % (', '.join(ms[:-1]), ms[-1])] += 1
R['translation_key_conflicts'] = dict(pairs.most_common())

# ---------- 샌드박스 옵션 ----------
sb = collections.defaultdict(list)
for mid in order:
    p = mod_files[mid].get('media/sandbox-options.txt')
    if p:
        for nm in re.findall(r'(?m)^\s*option\s+([A-Za-z0-9_.]+)', read_text(p)):
            sb[nm].append(mid)
R['sandbox_options'] = {k: v for k, v in sb.items()}
R['sandbox_conflicts'] = [dict(option=k, mods=v) for k, v in sb.items() if len(set(v)) > 1]

# ---------- mod.info 의 incompatible, 바이너리 ----------
for mid in order:
    for x in id_list(avail[mid]['info'].get('incompatible')):
        if x in order:
            R['incompatible_hits'].append(dict(mod=mid, incompatible_with=x))
    for rel in mod_files[mid]:
        if re.search(r'\.(dll|jar|class|exe|so|dylib)$', rel):
            R['binaries'].append(dict(mod=mid, file=rel))

# ---------- 모드 프로필 ("어떤 모드인가") ----------
for mid in order:
    m, files = avail[mid], mod_files[mid]
    lua = lua_of(files)
    side = collections.Counter(rel.split('/')[2] for rel in lua)
    langs = sorted({re.match(r'media/lua/shared/translate/([a-z_\-]+)/', r).group(1).upper() for r in files
                    if re.match(r'media/lua/shared/translate/([a-z_\-]+)/', r)})
    touched = sorted({t for t, s in R['patches'].items() for x in s if x['mod'] == mid})
    events = sorted({mm.group(1) for (m_, rel), (code, nostr) in scans.items() if m_ == mid for mm in re_events.finditer(nostr)})
    R['profiles'][mid] = dict(
        workshop=m['workshop'], folder=m['folder'], name=m['info'].get('name'), version_dir=m['vname'], version_dir_exists=os.path.isdir(m['vdir']),
        mod_info=os.path.relpath(m['info_path'], m['dir']).replace('\\', '/'), versionMin=m['info'].get('versionmin'),
        versionMax=m['info'].get('versionmax'), require=id_list(m['info'].get('require')),
        incompatible=id_list(m['info'].get('incompatible')), version_folders=sorted(x for x in os.listdir(m['dir']) if ver_int(x) > 0),
        lua=dict(side), scripts=R['scripts'].get(mid, {}).get('kinds', {}), sandbox_options=sum(1 for v in sb.values() if mid in v),
        translations=langs, has_ko='KO' in langs, textures=sum(1 for r in files if r.endswith('.png') and '/textures/' in r),
        maps=sorted({r.split('/')[2] for r in files if r.startswith('media/maps/') and r.count('/') > 2}),
        anims=sum(1 for r in files if r.startswith('media/animsets/') or r.startswith('media/anims_x/')),
        tiledefs=sum(1 for r in files if r.endswith('.tiles') or r.endswith('.pack')),
        binaries=[b['file'] for b in R['binaries'] if b['mod'] == mid],
        vanilla_functions=[dict(target=t, kinds=sorted({x['kind'] for x in R['patches'][t] if x['mod'] == mid})) for t in touched],
        events=events)

R['load_order'] = order
R['stats'] = dict(java_classes=len(classes), exposed_classes=len(exposed), java_events=len(java_events), lua_events=len(lua_events_added),
                  vanilla_lua=len(van_lua), mod_lua=len(scans))
R['patches'] = dict(R['patches'])
json.dump(R, open(os.path.join(OUT, 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- 사람이 읽을 요약 ----------
cand = set(candidates)


def mark(*mods):
    return ' **[후보]**' if cand & set(mods) else ''


L = ['# 정적 분석 결과', '', '게임 %s, 모드 %d개, 후보: %s' % (GV_TEXT, len(order), ', '.join(candidates) or '없음'), '']
if missing:
    L += ['## 찾지 못한 모드(require 포함)', ''] + ['- %s' % x for x in missing] + ['']
L += ['## 실제 로드 순서', '', '| # | Mod ID | 버전 폴더 | require |', '|---|---|---|---|']
for i, mid in enumerate(order, 1):
    p = R['profiles'][mid]
    L.append('| %d | %s%s | %s%s | %s |' % (i, mid, mark(mid), p['version_dir'], '' if p['version_dir_exists'] else ' (없음, common 만)', ', '.join(p['require'])))
L += ['', '## 모드 프로필', '']
for mid in order:
    if cand and mid not in cand:
        continue
    p = R['profiles'][mid]
    L += ['### %s (%s)' % (mid, p['workshop']), '',
          '- 이름: %s, versionMin=%s, versionMax=%s, 버전 폴더 %s → %s 사용' % (p['name'], p['versionMin'], p['versionMax'], p['version_folders'], p['version_dir']),
          '- Lua: %s / 스크립트: %s / 샌드박스 옵션 %d개 / 텍스처 %d / 애니메이션 %d / 타일 %d / 지도 %s' % (
              p['lua'] or '없음', p['scripts'] or '없음', p['sandbox_options'], p['textures'], p['anims'], p['tiledefs'], p['maps'] or '없음'),
          '- 번역: %s (KO %s)' % (', '.join(p['translations']) or '없음', '있음' if p['has_ko'] else '없음'),
          '- 바닐라 함수: %s' % (', '.join('%s(%s)' % (v['target'], '/'.join(v['kinds'])) for v in p['vanilla_functions']) or '없음'),
          '- 이벤트: %s' % (', '.join(p['events']) or '없음')]
    if p['binaries']:
        L.append('- **바이너리 포함**: %s (REA 로 볼 수 있는 유일한 경우)' % ', '.join(p['binaries']))
    L.append('')


def section(title, rows):
    global L
    L += ['## %s (%d)' % (title, len(rows)), ''] + (rows or ['- 없음']) + ['']


section('파일 덮어쓰기: 실제로 지워지는 것', ['- %s: %s → %s%s' % (o['path'], o['earlier'], o['later'], mark(o['earlier'], o['later'])) for o in overrides if not o['harmless']])
section('바닐라 파일을 통째로 바꾸는 것', ['- %s: %s%s' % (o['mod'], o['path'], mark(o['mod'])) for o in vanilla_overrides if not o['harmless']])
section('같은 바닐라 함수를 여러 모드가 고침', ['- `%s`: %s%s' % (s['target'], ', '.join('%s(%s, %s:%d)' % (x['mod'], x['kind'], x['file'].split('/lua/')[-1], x['line']) for x in s['sites']),
                                                                    mark(*[x['mod'] for x in s['sites']])) for s in R['shared_patches']])
section('바닐라 함수를 통째로 교체(replace) — fn_diff.py 로 현재 바닐라와 비교할 것',
        ['- `%s`: %s (%s:%d)%s' % (t, x['mod'], x['file'].split('/lua/')[-1], x['line'], mark(x['mod'])) for t, s in R['patches'].items() for x in s if x['kind'] == 'replace'])
section('한 모드 안에서 같은 전역을 여러 파일이 정의(잔여 파일 의심)', ['- %s: `%s` ← %s (마지막: %s)%s' % (x['mod'], x['global_'], ', '.join(x['files']), x['winner'], mark(x['mod'])) for x in R['subfolder_lua']])
section('감싸려는 함수가 없음', ['- %s %s:%d `%s`%s' % (x['mod'], x['file'], x['line'], x['target'], mark(x['mod'])) for x in R['missing_targets']])
section('없는 이벤트 이름', ['- %s %s:%d %s%s' % (x['mod'], x['file'], x['line'], x['event'], mark(x['mod'])) for x in R['unknown_events']])
section('require 대상 파일 없음(조건문 안인지 확인)', ['- %s %s:%d "%s"%s' % (x['mod'], x['file'], x['line'], x['require'], mark(x['mod'])) for x in R['missing_requires']])
section('instanceof 의 클래스 없음', ['- %s %s:%d %s%s' % (x['mod'], x['file'], x['line'], x['cls'], mark(x['mod'])) for x in R['bad_instanceof']])
um = collections.OrderedDict()
for x in R['unknown_methods']:
    um.setdefault((x['mod'], x['name']), x)
section('jar 에도 Lua 에도 없는 메서드 호출(조건문 안인지 확인)',
        ['- %s `%s` %s:%d%s' % (x['mod'], x['name'], x['file'].split('/lua/')[-1], x['line'], mark(x['mod'])) for x in um.values() if not x['in_java']])
weak = collections.Counter(x['mod'] for x in um.values() if x['in_java'])
L += ['- 참고: jar 에는 있지만 노출 클래스 목록 밖이라 확인만 못 한 메서드 이름 수: %s' % (dict(weak) or '없음'),
      '  (지도 API 처럼 다른 경로로 노출되는 경우가 많다. report.json 의 unknown_methods 에서 in_java=true)', '']
section('UTF-8 바이트를 가정한 문자열 코드(한글 닉네임·한글 문자열이 깨질 수 있음)',
        ['- %s %s:%d%s' % (x['mod'], x['file'].split('/lua/')[-1], x['line'], mark(x['mod'])) for x in R['utf8_byte_code']])
section('스크립트 정의 충돌', ['- %s: %s%s' % (x['defn'], ', '.join(x['mods']), mark(*x['mods'])) for x in R['script_conflicts']])
section('바닐라 스크립트 정의를 덮음', ['- %s: %s%s' % (mid, ', '.join(v['overrides_vanilla']), mark(mid)) for mid, v in R['scripts'].items() if v['overrides_vanilla']])
section('샌드박스 옵션 이름 충돌', ['- %s: %s' % (x['option'], ', '.join(x['mods'])) for x in R['sandbox_conflicts']])
section('mod.info incompatible 에 걸림', ['- %s ↔ %s' % (x['mod'], x['incompatible_with']) for x in R['incompatible_hits']])
section('번역 JSON 오류', ['- %s %s: %s (끝 쉼표만 고치면 읽힘: %s)' % (x['mod'], x['file'], x['error'], x['game_accepts_trailing_comma']) for x in R['json_errors']])
section('KO 번역 키를 나중 모드가 덮음(값이 다른 키 수)', ['- %s: %d' % (k, v) for k, v in R['translation_key_conflicts'].items()])
open(os.path.join(OUT, 'report.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L[:12]))
print('... 전체: %s' % os.path.join(OUT, 'report.md'))
