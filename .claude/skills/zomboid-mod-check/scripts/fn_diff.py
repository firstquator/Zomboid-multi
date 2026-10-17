# 모드가 통째로 바꾼 함수를 현재 바닐라 함수와 비교한다(문자열·getText·공백·주석은 뺀다)
#
#   python -I fn_diff.py <바닐라 lua 파일> <모드 lua 파일> "ISFoo:bar" ["ISFoo.baz" ...]
#
# 차이가 문자열뿐이면 번역용 복사본이고, 구조가 다르면 바닐라가 바뀐 뒤 모드가 옛 동작을 되살리는지 본다.
import difflib, re, sys


def extract(path, name):
    src = open(path, encoding='utf-8', errors='replace').read()
    esc = re.escape(name).replace(r'\:', r'[.:]').replace(r'\.', r'[.:]')
    m = re.search(r'^\s*function\s+' + esc + r'\s*\(', src, re.M) or re.search(r'^\s*' + esc + r'\s*=\s*function\s*\(', src, re.M)
    if not m:
        return None
    out, depth = [], 0
    for ln in src[m.start():].splitlines():
        code = re.sub(r'--.*', '', re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', 'S', ln))
        depth += len(re.findall(r'\b(function|if|do)\b', code)) - len(re.findall(r'\bend\b', code))
        out.append(ln)
        if depth <= 0 and len(out) > 1:
            break
    return out


def normalize(lines):
    res = []
    for ln in lines:
        ln = re.sub(r'--.*', '', ln)
        ln = re.sub(r'getText(?:OrNull)?\s*\(\s*"[^"]*"\s*(,[^)]*)?\)', 'TXT', ln)
        ln = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', 'S', ln)
        ln = re.sub(r'\s+', ' ', ln).strip().rstrip(';')
        ln = re.sub(r'\s*([=,()\[\]{}+\-*/<>~]|\.\.)\s*', r'\1', ln)
        if ln:
            res.append(ln)
    return res


van, mod = sys.argv[1], sys.argv[2]
for name in sys.argv[3:]:
    a, b = extract(van, name), extract(mod, name)
    if a is None or b is None:
        print('##', name, '찾지 못함:', '바닐라' if a is None else '', '모드' if b is None else '')
        continue
    d = [x for x in difflib.unified_diff(normalize(a), normalize(b), 'vanilla', 'mod', n=0, lineterm='')]
    changed = [x for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---')]
    print('## %s  바닐라 %d줄 / 모드 %d줄 / 다른 줄 %d' % (name, len(a), len(b), len(changed)))
    for x in d[2:60]:
        print('   ', x[:200])
