# 격리 폴더에서 전용 서버와 클라이언트(메인 메뉴까지)를 실제로 띄워 모드 로딩 오류를 본다 (Windows)
#
#   python -I load_test.py --game <PZ 설치 폴더> --content <content/108600> --mods-json data/mods.json
#                          [--add 3812345678[:ModA,ModB]] [--mode both|server|client] [--cache <폴더>]
#
# - 사용자 %USERPROFILE%\Zomboid 와 Steam 은 건드리지 않는다(-nosteam -cachedir=<캐시>\run\...).
# - 바닐라(모드 없음) 실행 결과를 <캐시>\baseline\<게임 버전>\ 에 한 번 만들어 두고, 그와 다른 ERROR/WARN 만 보여 준다.
# - 클라이언트는 창 모드 1280x720·한국어로 게임 창이 잠깐 뜬다. 게임이 켜져 있으면 끄고 돌린다.
import argparse, json, os, re, shutil, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument('--game', required=True)
ap.add_argument('--content', required=True)
ap.add_argument('--mods-json', required=True)
ap.add_argument('--add', action='append', default=[])
ap.add_argument('--mode', choices=['both', 'server', 'client'], default='both')
ap.add_argument('--cache', default=os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'zomboid-modcheck'))
ap.add_argument('--timeout', type=int, default=900)
ap.add_argument('--rebuild-baseline', action='store_true')
args = ap.parse_args()

GAME = os.path.realpath(args.game)
CACHE = os.path.realpath(args.cache)
if '~' in CACHE:
    # 42.21 은 8.3 짧은 경로에서 AnimSets 체크섬을 못 맞춰 서버 초기화가 멈춘다(실제로 겪음)
    sys.exit('캐시 경로에 8.3 짧은 이름(~)이 있다: %s' % CACHE)


def read_text(p):
    return open(p, 'rb').read().decode('utf-8', 'replace').lstrip('\ufeff')


def version_dir_name(mod_dir, gv):
    def vi(name):
        parts = name.split('.')
        try:
            nums = [int(x) for x in parts[:2]]
        except ValueError:
            return 0
        return nums[0] * 1000 + (min(nums[1], 999) if len(nums) > 1 else 0)
    best_name, best = '42.0', 42000
    for name in sorted(os.listdir(mod_dir)):
        v = vi(name)
        if best <= v <= gv:
            best_name, best = name, v
    return best_name


GV_TEXT = read_text(os.path.join(os.path.expanduser('~'), 'Zomboid', 'version.txt')).split()[0] \
    if os.path.isfile(os.path.join(os.path.expanduser('~'), 'Zomboid', 'version.txt')) else 'unknown'
mv = re.match(r'(\d+)\.(\d+)', GV_TEXT)
GV = int(mv.group(1)) * 1000 + int(mv.group(2)) if mv else 42999

# ---------- 모드 목록 ----------
avail, by_ws = {}, {}
for wid in os.listdir(args.content):
    root = os.path.join(args.content, wid, 'mods')
    if not os.path.isdir(root):
        continue
    for folder in os.listdir(root):
        mdir = os.path.join(root, folder)
        vn = version_dir_name(mdir, GV)
        for mi in (os.path.join(mdir, vn, 'mod.info'), os.path.join(mdir, 'common', 'mod.info')):
            if os.path.isfile(mi):
                info = dict(l.split('=', 1) for l in read_text(mi).splitlines() if '=' in l)
                info = {k.strip().lower(): v.strip() for k, v in info.items()}
                mid = info.get('id', folder)
                avail[mid] = dict(dir=mdir, require=[x.strip().lstrip('\\') for x in info.get('require', '').split(',') if x.strip().lstrip('\\')])
                by_ws.setdefault(wid, []).append(mid)
                break

pack = json.load(open(args.mods_json, encoding='utf-8'))
mods = [i for m in sorted(pack['mods'], key=lambda m: m['loadOrder']) for i in m['modIds']]
for a in args.add:
    wid, _, ids = a.partition(':')
    ids = [x for x in ids.split(',') if x] or by_ws.get(wid, [])
    if len(ids) != 1 and ':' not in a:
        sys.exit('창작마당 %s 의 Mod ID 를 골라야 한다: %s' % (wid, by_ws.get(wid)))
    mods += [x for x in ids if x not in mods]
need, todo = [], list(mods)
while todo:
    x = todo.pop(0)
    if x in need:
        continue
    if x not in avail:
        sys.exit('모드 %s 를 %s 에서 찾지 못했다(require 포함). fetch_mods.py 로 받는다.' % (x, args.content))
    need.append(x)
    todo += avail[x]['require']


# ---------- 실행 도구 ----------
def prepare_home(home, mod_ids):
    if os.path.isdir(home):
        shutil.rmtree(home)
    os.makedirs(os.path.join(home, 'mods'))
    for x in mod_ids:
        src = avail[x]['dir']
        dst = os.path.join(home, 'mods', os.path.basename(src))
        if not os.path.isdir(dst):
            shutil.copytree(src, dst)


def kill_tree(p):
    subprocess.run(['taskkill', '/T', '/F', '/PID', str(p.pid)], capture_output=True)


def wait_for(log, ok_pat, bad_pat, proc, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if os.path.isfile(log):
            txt = read_text(log)
            if re.search(ok_pat, txt):
                return 'ok'
            m = re.search(bad_pat, txt)
            if m:
                return 'fatal: ' + m.group(0)
        if proc.poll() is not None:
            return 'exited(%s)' % proc.returncode
        time.sleep(2)
    return 'timeout'


def run_server(home, mod_ids):
    prepare_home(home, mod_ids)
    os.makedirs(os.path.join(home, 'Server'))
    open(os.path.join(home, 'Server', 'modcheck.ini'), 'w', encoding='utf-8').write(
        'Mods=%s\nWorkshopItems=\nMap=Muldraugh, KY\nPVP=false\nPublic=false\nPauseEmpty=true\nDefaultPort=16361\nUDPPort=16362\n' % ';'.join(mod_ids))
    java = os.path.join(GAME, 'jre64', 'bin', 'java.exe')
    cmd = [java, '--enable-native-access=ALL-UNNAMED', '--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED', '-XX:+UseZGC',
           '-XX:-CreateCoredumpOnCrash', '-XX:-OmitStackTraceInFastThrow', '-Xmx3072m', '-Djava.awt.headless=true',
           '-Djava.library.path=./natives/;./natives/win64/;./', '-cp', './;projectzomboid.jar', 'zombie.network.GameServer',
           '-nosteam', '-cachedir=' + home, '-servername', 'modcheck', '-adminpassword', 'modcheck']
    out = open(os.path.join(home, 'stdout.txt'), 'w', encoding='utf-8')
    p = subprocess.Popen(cmd, cwd=GAME, stdin=subprocess.PIPE, stdout=out, stderr=subprocess.STDOUT)
    st = wait_for(os.path.join(home, 'server-console.txt'), r'\*\*\* SERVER STARTED \*\*\*',
                  r'GameServer\.(main|doMinimumInit)> Exception thrown|couldn\'t find "[^"]+"', p, args.timeout)
    try:
        p.stdin.write(b'quit\n'); p.stdin.flush()
        p.wait(60)
    except Exception:
        pass
    kill_tree(p)
    return st, os.path.join(home, 'server-console.txt')


def run_client(home, mod_ids):
    prepare_home(home, mod_ids)
    user_opts = os.path.join(os.path.expanduser('~'), 'Zomboid', 'options.ini')
    opts = read_text(user_opts) if os.path.isfile(user_opts) else 'version=8\n'
    for k, v in (('fullScreen', 'false'), ('borderless', 'false'), ('width', '1280'), ('height', '720'), ('language', 'KO')):
        opts = re.sub(r'(?m)^%s=.*$' % k, '%s=%s' % (k, v), opts) if re.search(r'(?m)^%s=' % k, opts) else opts + '%s=%s\n' % (k, v)
    open(os.path.join(home, 'options.ini'), 'w', encoding='utf-8').write(opts)
    open(os.path.join(home, 'mods', 'default.txt'), 'w', encoding='utf-8', newline='\n').write(
        'VERSION = 1,\n\nmods\n{\n' + ''.join('    mod = %s,\n' % x for x in mod_ids) + '}\n\nmaps\n{\n}\n')
    open(os.path.join(home, 'mods', 'reset-mods-42_00.txt'), 'w', encoding='utf-8').write(
        'If this file does not exist, default.txt will be reset to empty (no mods active).')
    p = subprocess.Popen([os.path.join(GAME, 'ProjectZomboid64.exe'), '-nosteam', '-cachedir=' + home], cwd=GAME,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    st = wait_for(os.path.join(home, 'console.txt'), r'STATE: exit zombie\.gameStates\.TISLogoState', r'(?!)', p, args.timeout)
    if st == 'ok':
        time.sleep(20)  # 메인 메뉴 진입 때 도는 Lua(OnMainMenuEnter 등)까지 기다린다
    kill_tree(p)
    return st, os.path.join(home, 'console.txt')


def norm_lines(path, home):
    out = []
    lines = read_text(path).splitlines() if os.path.isfile(path) else []
    for i, ln in enumerate(lines):
        if not re.match(r'^(ERROR|WARN)', ln):
            continue
        n = ln.replace(home, '<HOME>').replace(home.replace('\\', '/'), '<HOME>')
        n = re.sub(r'f:\d+( st:[\d,]+)?', '', n)
        n = re.sub(r'\d{6,}', '', n)
        n = re.sub(r'\s+', ' ', n)[:220]
        out.append((n, i, lines[i:i + 5]))
    return out, lines


KNOWN_HARMLESS = [
    (r'AdvancedAnimator\$1\.visitFileFailed', '모드에 AnimSets/actiongroups 폴더가 없다는 알림(모든 모드 공통)'),
]


def compare(kind, run_log, run_home, base_log, base_home):
    base = {n for n, _, _ in norm_lines(base_log, base_home)[0]}
    run, lines = norm_lines(run_log, run_home)
    new, harmless = {}, {}
    for n, i, ctx in run:
        if n in base:
            continue
        tag = next((why for pat, why in KNOWN_HARMLESS if re.search(pat, n)), None)
        (harmless if tag else new).setdefault(n, dict(count=0, first_line=i + 1, context=ctx, why=tag))
        (harmless if tag else new)[n]['count'] += 1
    lua_logs = [l for l in lines if l.startswith('LOG  : Lua')]
    return dict(kind=kind, log=run_log, stack_traces=sum(1 for l in lines if 'STACK TRACE' in l), new=new,
                harmless={k: dict(count=v['count'], why=v['why']) for k, v in harmless.items()}, lua_log_tail=lua_logs[-25:])


# ---------- 실행 ----------
base_dir = os.path.join(CACHE, 'baseline', GV_TEXT)
run_dir = os.path.join(CACHE, 'run')
result = dict(game_version=GV_TEXT, mods=need, runs=[])
kinds = ['server', 'client'] if args.mode == 'both' else [args.mode]
for kind in kinds:
    runner = run_server if kind == 'server' else run_client
    bhome = os.path.join(base_dir, kind)
    blog = os.path.join(bhome, 'server-console.txt' if kind == 'server' else 'console.txt')
    if args.rebuild_baseline or not os.path.isfile(blog):
        print('[%s] 바닐라 기준선 실행 ...' % kind, flush=True)
        st, _ = runner(bhome, [])
        print('[%s] 기준선: %s' % (kind, st), flush=True)
    print('[%s] 모드 %d개로 실행 ...' % (kind, len(need)), flush=True)
    st, log = runner(os.path.join(run_dir, kind), need)
    c = compare(kind, log, os.path.join(run_dir, kind), blog, bhome)
    c['status'] = st
    result['runs'].append(c)
    print('[%s] 상태: %s, 스택 트레이스 %d, 새 오류·경고 %d종, 알려진 무해 %d종' % (kind, st, c['stack_traces'], len(c['new']), len(c['harmless'])))
    for n, v in list(c['new'].items())[:40]:
        print('   x%d  %s' % (v['count'], n))
        for ctx in v['context'][1:4]:
            print('          ', ctx[:200])
json.dump(result, open(os.path.join(CACHE, 'load_test_result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('결과: %s' % os.path.join(CACHE, 'load_test_result.json'))
sys.exit(0 if all(r['status'] == 'ok' and not r['new'] for r in result['runs']) else 1)
