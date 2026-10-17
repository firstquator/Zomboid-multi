"""게임 파일에서 직업·특성 데이터와 아이콘을 뽑아 사이트용 데이터로 만든다.

    python scripts/extract-character.py "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"

캐릭터 만들기 화면의 포인트, 기술 보너스, 함께 못 고르는 특성은 패치마다 바뀐다.
손으로 옮겨 적으면 금방 틀리므로 게임이 쓰는 정의 파일을 그대로 읽는다.

읽는 것
- media/scripts/generated/characters/character_professions.txt, character_traits.txt
- media/lua/shared/Translate/{KO,EN}/UI.json, IG_UI.json (이름·설명·기술 이름)
- media/texturepacks/UI2.pack 과 media/ui/Traits/*.png (아이콘)

쓰는 것
- web/src/data/character.json
- web/public/icons/prof/<id>.webp, web/public/icons/trait/<id>.webp (무손실 webp)

게임 파일은 읽기만 한다. 아이콘은 The Indie Stone 의 것이며 사이트에 출처를 밝힌다.
"""

import io
import json
import re
import struct
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "web/src/data/character.json"
OUT_ICONS = ROOT / "web/public/icons"


def parse_definitions(text, kind):
    """`character_<kind>_definition base:id { Key = Value, ... }` 블록을 사전 목록으로 바꾼다."""
    out = []
    # "out of shape", "very underweight" 처럼 이름에 띄어쓰기가 있는 특성도 있다.
    # 주소 링크에 쓰는 id 는 띄어쓰기를 뺀 값(outofshape)으로 하고, 원래 이름은 raw 에 둔다.
    pattern = re.compile(r"character_" + kind + r"_definition\s+base:([^{\n]+?)\s*\{(.*?)\}", re.S)
    for m in pattern.finditer(text):
        item = {"id": m.group(1).replace(" ", ""), "raw": m.group(1)}
        for line in m.group(2).splitlines():
            line = line.strip().rstrip(",")
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            item[key.strip()] = value.strip()
        out.append(item)
    return out


def split_list(value):
    return [v.strip().replace("base:", "") for v in (value or "").split(";") if v.strip()]


def split_ids(value):
    """특성 id 목록. parse_definitions 와 같이 띄어쓰기를 뺀다."""
    return [v.replace(" ", "") for v in split_list(value)]


def parse_xp(value):
    xp = []
    for part in split_list(value):
        if "=" in part:
            skill, level = part.split("=", 1)
            xp.append({"skill": skill.strip(), "level": int(level)})
    return xp


def read_pack(path):
    """PZPK 텍스처 묶음에서 {아이콘 이름: (페이지 PNG 바이트, x, y, w, h)} 를 만든다."""
    data = path.read_bytes()
    if data[:4] != b"PZPK":
        raise SystemExit(f"PZPK 형식이 아닙니다: {path}")
    _, npages = struct.unpack_from("<ii", data, 4)
    pos = 12

    def rstr():
        nonlocal pos
        (n,) = struct.unpack_from("<i", data, pos)
        pos += 4
        s = data[pos : pos + n].decode("latin1")
        pos += n
        return s

    entries = {}
    for _ in range(npages):
        rstr()  # 페이지 이름
        n, _mask = struct.unpack_from("<ii", data, pos)
        pos += 8
        page_entries = []
        for _ in range(n):
            name = rstr()
            x, y, w, h, *_rest = struct.unpack_from("<8i", data, pos)
            pos += 32
            page_entries.append((name, x, y, w, h))
        (size,) = struct.unpack_from("<i", data, pos)
        png = data[pos + 4 : pos + 4 + size]
        pos += 4 + size
        if png[:4] != b"\x89PNG":
            raise SystemExit("페이지 PNG 를 찾지 못했습니다. 묶음 형식이 바뀌었을 수 있습니다")
        for name, x, y, w, h in page_entries:
            entries[name] = (png, x, y, w, h)
    return entries


def save_webp(img, dest):
    # 도트 아이콘이라 손실 압축을 쓰면 테두리가 번진다. 무손실로 저장해도 PNG 보다 작다.
    img.save(dest, "WEBP", lossless=True, method=6)


def save_icon(pack, loose_dir, names, dest):
    """이름 후보 중 처음 찾은 아이콘을 dest 에 webp 로 저장한다. 찾으면 True."""
    pages = {}
    for name in names:
        loose = loose_dir / f"{name}.png"
        if loose.exists():
            save_webp(Image.open(loose).convert("RGBA"), dest)
            return True
        if name in pack:
            png, x, y, w, h = pack[name]
            if id(png) not in pages:
                pages[id(png)] = Image.open(io.BytesIO(png)).convert("RGBA")
            save_webp(pages[id(png)].crop((x, y, x + w, y + h)), dest)
            return True
    return False


def main():
    game = Path(sys.argv[1] if len(sys.argv) > 1 else "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid")
    media = game / "media"
    chars = media / "scripts/generated/characters"
    professions = parse_definitions((chars / "character_professions.txt").read_text(encoding="utf-8"), "profession")
    traits = parse_definitions((chars / "character_traits.txt").read_text(encoding="utf-8"), "trait")

    def load(lang, name):
        return json.loads((media / f"lua/shared/Translate/{lang}/{name}").read_text(encoding="utf-8"))

    ko = {**load("KO", "UI.json"), **load("KO", "IG_UI.json")}
    en = {**load("EN", "UI.json"), **load("EN", "IG_UI.json")}

    def text(key):
        return (ko.get(key) or en.get(key) or "").strip() if key else ""

    pack = read_pack(media / "texturepacks/UI2.pack")
    loose = media / "ui/Traits"
    (OUT_ICONS / "prof").mkdir(parents=True, exist_ok=True)
    (OUT_ICONS / "trait").mkdir(parents=True, exist_ok=True)

    skills = {}
    # 정의 파일의 기술 이름과 번역 키 이름이 다른 것들
    perk_key = {"Lightfoot": "Lightfooted", "Sneak": "Sneaking", "PlantScavenging": "Foraging"}

    # 게임 한국어 번역이 비어 있는 기술(B42 에 새로 생긴 추적)
    perk_fallback = {"Tracking": "추적"}

    def skill_name(sid):
        if sid not in skills:
            skills[sid] = text(f"IGUI_perks_{perk_key.get(sid, sid)}") or perk_fallback.get(sid, sid)
        return skills[sid]

    out_prof = []
    for p in professions:
        icon = p.get("IconPathName", "")
        has_icon = save_icon(pack, loose, [icon], OUT_ICONS / "prof" / f"{p['id']}.webp") if icon else False
        xp = parse_xp(p.get("XPBoosts"))
        for x in xp:
            x["name"] = skill_name(x["skill"])
        out_prof.append(
            {
                "id": p["id"],
                "name": text(p.get("UIName")),
                "nameEn": en.get(p.get("UIName", ""), p["id"]),
                "cost": int(p.get("Cost", 0)),
                "desc": text(p.get("UIDescription")),
                "xp": xp,
                "granted": split_ids(p.get("GrantedTraits")),
                "recipes": len(split_list(p.get("GrantedRecipes"))),
                "icon": f"icons/prof/{p['id']}.webp" if has_icon else None,
            }
        )

    out_traits = []
    for t in traits:
        if t.get("DisabledInMultiplayer", "false") == "true":
            continue
        tid = t["id"]
        has_icon = save_icon(pack, loose, [f"trait_{t['raw']}", f"trait_{tid}", f"trait_{tid.lower()}"], OUT_ICONS / "trait" / f"{tid}.webp")
        xp = parse_xp(t.get("XPBoosts"))
        for x in xp:
            x["name"] = skill_name(x["skill"])
        out_traits.append(
            {
                "id": tid,
                "name": text(t.get("UIName")),
                "nameEn": en.get(t.get("UIName", ""), tid),
                "cost": int(t.get("Cost", 0)),
                "desc": text(t.get("UIDescription")),
                "exclusive": split_ids(t.get("MutuallyExclusiveTraits")),
                "xp": xp,
                "recipes": len(split_list(t.get("GrantedRecipes"))),
                "professionOnly": t.get("IsProfessionTrait", "false") == "true",
                "icon": f"icons/trait/{tid}.webp" if has_icon else None,
            }
        )

    version = ""
    vfile = Path.home() / "Zomboid/version.txt"
    if vfile.exists():
        version = vfile.read_text(encoding="utf-8").split()[0]

    out_prof.sort(key=lambda p: (-p["cost"], p["name"]))
    out_traits.sort(key=lambda t: (t["cost"] < 0, -abs(t["cost"]), t["name"]))
    OUT_JSON.write_text(
        json.dumps(
            {"build": version, "professions": out_prof, "traits": out_traits, "skills": skills},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    missing = [p["id"] for p in out_prof if not p["icon"]] + [t["id"] for t in out_traits if not t["icon"]]
    print(f"직업 {len(out_prof)}개, 특성 {len(out_traits)}개 (멀티에서 꺼진 특성 제외), 아이콘 없음: {missing or '없음'}")


if __name__ == "__main__":
    main()
