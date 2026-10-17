# 모드마다 EN 번역 키가 최종 KO 에서 채워지는 비율과 %1 자리표시 불일치
#
#   python -I ko_cover.py --report <mod_analyze 의 report.json> --game <PZ 설치 폴더> --content <content/108600>
#
# 게임과 같은 순서(바닐라 → 로드 순서대로 모드, 빈 값이 아니면 나중 값이 이김)로 합친다.
# 근거: zombie.core.Translator.tryFillMapFromFile / tryFillMapFromMods
import argparse, collections, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument('--report', required=True)
ap.add_argument('--game', required=True)
ap.add_argument('--content', required=True)
args = ap.parse_args()
R = json.load(open(args.report, encoding='utf-8'))


def load_json(p):
    t = open(p, encoding='utf-8-sig', errors='replace').read()
    try:
        return json.loads(t)
    except Exception:
        return json.loads(re.sub(r',\s*([}\]])', r'\1', t))  # 게임(비엄격 org.json)은 끝 쉼표를 받아 준다


def tr_files(root, lang):
    d = os.path.join(root, 'media', 'lua', 'shared', 'Translate', lang)
    return {f[:-5]: os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith('.json')} if os.path.isdir(d) else {}


def roots(mid):
    p = R['profiles'][mid]
    base = os.path.join(args.content, p['workshop'], 'mods', p['folder'])
    return [os.path.join(base, 'common'), os.path.join(base, p['version_dir'])]


final = {'KO': collections.defaultdict(dict), 'EN': collections.defaultdict(dict)}
owner_en = collections.defaultdict(set)
for lang in ('EN', 'KO'):
    for f, p in tr_files(args.game, lang).items():
        final[lang][f].update(load_json(p))
    for mid in R['load_order']:
        for root in roots(mid):
            for f, p in tr_files(root, lang).items():
                try:
                    data = load_json(p)
                except Exception as ex:
                    print('JSON 실패', mid, p, ex)
                    continue
                for k, v in data.items():
                    if k not in final[lang][f] or str(v) != '':
                        final[lang][f][k] = v
                    if lang == 'EN':
                        owner_en[(f, k)].add(mid)

ph = re.compile(r'%\d')
per = collections.defaultdict(lambda: [0, 0, []])
mismatch = []
for (f, k), mods in owner_en.items():
    ko, en = final['KO'][f].get(k), final['EN'][f].get(k)
    for mid in mods:
        per[mid][0] += 1
        if ko is not None and ko != en:
            per[mid][1] += 1
        else:
            per[mid][2].append('%s:%s' % (f, k))
    if ko is not None and en is not None and sorted(ph.findall(str(ko))) != sorted(ph.findall(str(en))):
        mismatch.append((sorted(mods), f, k, str(en)[:60], str(ko)[:60]))

print('| 모드 | KO 로 채워짐 | 빠진 키 예 |')
print('|---|---|---|')
for mid in R['load_order']:
    if mid in per:
        tot, ok, miss = per[mid]
        print('| %s | %d/%d | %s |' % (mid, ok, tot, ', '.join(miss[:3])))
    else:
        print('| %s | EN 번역 키 없음 (하드코딩이거나 번역 전용 모드) | |' % mid)
print('\n%%1 자리표시 개수가 EN 과 다른 KO: %d' % len(mismatch))
for m in mismatch[:30]:
    print('  ', m)
