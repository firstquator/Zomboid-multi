# 창작마당 모드를 SteamCMD 로 받고(익명), 창작마당 정보를 함께 저장한다
#
#   python -I fetch_mods.py [--pack data/mods.json] [--cache <폴더>] 3812345678 3898765432 ...
#
# --pack 을 주면 mods.json 의 모든 아이템도 같이 최신으로 받는다(팩 전체와 대조하려면 필요하다).
# 캐시 기본값: %LOCALAPPDATA%\zomboid-modcheck  (짧은 8.3 경로 SANGHY~1 같은 것을 쓰면 게임이 파일을 못 찾는다)
#   steamcmd\       SteamCMD (없으면 Valve CDN 에서 받는다)
#   ws\steamapps\workshop\content\108600\<번호>\   받은 모드 (신뢰하지 않는 데이터. 안에서 아무것도 실행하지 않는다)
#   meta\<번호>.json  창작마당 API 정보 + Required items
import argparse, io, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, zipfile

ap = argparse.ArgumentParser()
ap.add_argument('ids', nargs='*')
ap.add_argument('--pack')
ap.add_argument('--cache', default=os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'zomboid-modcheck'))
ap.add_argument('--skip-download', action='store_true', help='창작마당 정보만 갱신')
args = ap.parse_args()

cache = os.path.realpath(args.cache)
if '~' in cache:
    sys.exit('캐시 경로에 8.3 짧은 이름(~)이 있다: %s  긴 경로를 넘긴다.' % cache)
ids = list(dict.fromkeys(args.ids + ([m['workshopId'] for m in json.load(open(args.pack, encoding='utf-8'))['mods']] if args.pack else [])))
if not ids:
    sys.exit('받을 창작마당 번호가 없다.')
for i in ids:
    if not re.fullmatch(r'\d{6,12}', i):
        sys.exit('창작마당 번호가 아니다: %s' % i)
os.makedirs(os.path.join(cache, 'meta'), exist_ok=True)


def post(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def get(url, tries=4):
    """steamcommunity.com 은 연달아 읽으면 429 를 준다. 기다렸다 다시 시도한다."""
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as ex:
            if ex.code != 429 or n == tries - 1:
                raise
            time.sleep(15 * (n + 1))


# ---------- 창작마당 정보 ----------
data = {'itemcount': len(ids)}
data.update({'publishedfileids[%d]' % i: x for i, x in enumerate(ids)})
details = post('https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/', data)['response']['publishedfiledetails']
for d in details:
    wid = d['publishedfileid']
    meta = dict(workshopId=wid, ok=d.get('result') == 1, title=d.get('title'), visibility=d.get('visibility'), banned=d.get('banned'),
                created=time.strftime('%Y-%m-%d', time.gmtime(d.get('time_created', 0))),
                updated=time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(d.get('time_updated', 0))),
                subscriptions=d.get('subscriptions'), lifetime_subscriptions=d.get('lifetime_subscriptions'),
                favorited=d.get('favorited'), size=d.get('file_size'), tags=[t['tag'] for t in d.get('tags', [])],
                modIdLines=[x.strip() for x in re.findall(r'Mod\s*ID\s*:\s*([^\r\n\[<]+)', d.get('description', ''), re.I)],
                description=d.get('description', ''), requiredItems=[])
    try:
        html = get('https://steamcommunity.com/sharedfiles/filedetails/?id=' + wid)
        meta['requiredItems'] = [dict(id=a, name=b) for a, b in
                                 re.findall(r'filedetails/\?id=(\d+)"[^>]*>\s*<div class="requiredItem">\s*([^<]*?)\s*</div>', html)]
        time.sleep(1.5)
    except Exception as ex:
        meta['requiredItems'] = None
        meta['requiredItems_error'] = str(ex)
    json.dump(meta, open(os.path.join(cache, 'meta', wid + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    req_txt = ('확인 실패(%s)' % meta['requiredItems_error']) if meta['requiredItems'] is None else (
        ['%s %s' % (r['id'], r['name']) for r in meta['requiredItems']] or '없음')
    print('%s  %s\n    업데이트 %s, 구독 %s(누적 %s), 태그 %s\n    Mod ID 줄 %s, Required %s' % (
        wid, meta['title'], meta['updated'], meta['subscriptions'], meta['lifetime_subscriptions'], meta['tags'],
        meta['modIdLines'], req_txt))

if args.skip_download:
    sys.exit(0)

# ---------- SteamCMD ----------
sc_dir = os.path.join(cache, 'steamcmd')
sc = os.path.join(sc_dir, 'steamcmd.exe')
if not os.path.isfile(sc):
    os.makedirs(sc_dir, exist_ok=True)
    print('SteamCMD 받는 중 ...')
    with urllib.request.urlopen('https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip', timeout=120) as r:
        zipfile.ZipFile(io.BytesIO(r.read())).extractall(sc_dir)
ws = os.path.join(cache, 'ws')
os.makedirs(ws, exist_ok=True)
cmd = [sc, '+force_install_dir', ws, '+login', 'anonymous']
for i in ids:
    cmd += ['+workshop_download_item', '108600', i, 'validate']
cmd += ['+quit']
p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
log = p.stdout + p.stderr
open(os.path.join(cache, 'steamcmd-last.log'), 'w', encoding='utf-8').write(log)
ok = re.findall(r'Success\. Downloaded item (\d+)', log)
bad = [i for i in ids if i not in ok]
print('받음 %d개 → %s' % (len(ok), os.path.join(ws, 'steamapps', 'workshop', 'content', '108600')))
if bad:
    print('실패: %s (SteamCMD 로그: %s)' % (bad, os.path.join(cache, 'steamcmd-last.log')))
    for line in log.splitlines():
        if 'ERROR' in line or 'Failure' in line:
            print('   ', line.strip())
    sys.exit(1)
