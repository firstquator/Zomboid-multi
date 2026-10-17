"""플레이 팁 페이지에 쓸 게임 그림을 42.21 게임 파일에서 꺼내 webp 로 저장한다.

    python -I scripts/extract-guide-assets.py "C:\\Program Files (x86)\\Steam\\steamapps\\common\\ProjectZomboid"

- 차량 원형 메뉴·계기판 아이콘: media/texturepacks/UI2.pack
- 정비 화면 차 그림(차체 + 부품 마스크): media/ui/vehicles/mechanic overlay/4door_*.png
- 게임 안내서 그림(Spiffo): media/ui/survival_guide_spiffo/*.png
- 상태 아이콘(무들): media/ui/Moodles/64/*.png

아이템 아이콘은 scripts/extract-items.py 가 web/public/icons/item 에 따로 저장한다.
도트 그림은 무손실, 큰 일러스트는 손실 압축(품질 86)으로 저장한다.
"""

import io
import struct
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web/public/guide"

# 차량 원형 메뉴와 계기판에서 쓰는 텍스처 이름
VEHICLE_UI = [
    "carradialmenu",
    "vehicle_ignitionON",
    "vehicle_ignitionOFF",
    "vehicle_lightsON",
    "vehicle_horn",
    "vehicle_lockdoors",
    "vehicle_repair",
    "vehicle_exit",
    "vehicle_changeseats",
    "vehicle_windowOPEN",
    "vehicle_siren",
    "vehicle_lightbar",
    "vehicle_speakersON",
    "vehicle_temperatureHOT",
    "vehicle_sleep",
    "cardashboard",
    "vehicle_fuelguage",
    "vehicle_spedometer",
    "icon_lowgas_light",
    "icon_enginetrouble_light",
    "icon_headlights_light",
    "icon_ignition_light",
    "ignition_key_on",
    "ignition_hotwired",
    "engine",
    "gas",
]
# 차량 섹션에서 쓰는 아이템 아이콘(Item_ 를 뺀 이름). UI.pack(옛 형식)과 UI2.pack 에 나뉘어 있다.
ITEM_ICONS = ["CarKey", "Crowbar", "Petrol", "JerrycanMilitary", "RubberHose", "CarJack", "LugWrench", "Wrench",
              "Screwdriver", "TirePump", "CarBattery", "CarBatteryCharger", "EngineParts", "MagazineMechanic1",
              "MagazineMechanic2", "MagazineMechanic3", "Generator", "CarTire", "WeldingMask", "BlowTorch",
              # 생활 꿀팁
              "BaseballBat", "Belt", "Hammer", "Whetstone2", "DuctTape", "Glue", "Flashlight2", "Battery",
              "BigHiking_Blue", "AliceBag", "FannyPack", "Bandage", "AlcoholWipes", "Alcohol", "SutureNeedle",
              "Tweezers", "Splint", "BandageDirty", "Antibiotics", "Rag", "Beans", "CanOpener", "Pot",
              "WaterPurificationTablets", "WaterBottle", "Rock", "Matches", "ComicBook", "Magazine", "Plank",
              "Nails", "Sledgehamer", "SheetRope", "Sheet", "Garbagebag", "TentMaterial", "MagazineElectronics02",
              "Cassette3", "Twigs", "BerryBlack", "Egg", "RockSharpened", "AxeStone", "Map", "Pen", "Notebook",
              "LeatherStrips", "Thread"]
# 화면 왼쪽 아이콘 줄 그림(media/ui/Sidebar/64)
SIDEBAR = ["Inventory_On_64", "Heart_On_64", "Carpentry_On_64", "Build_On_64", "Map_On_64", "Search_On_64",
           "AnimalZone_On_64"]
# media/ui/vehicles 의 낱개 그림(주유·기름 빼기·창문 깨기 메뉴 아이콘)
VEHICLE_LOOSE = ["vehicle_add_gas", "vehicle_refuel_from_pump", "vehicle_siphon_gas", "vehicle_smash_window"]
SPIFFO = ["spiffo_vehicle", "spiffo_combat", "spiffo_crafting", "spiffo_farming", "spiffo_food", "spiffo_foraging",
          "spiffo_inventory", "spiffo_movement", "spiffo_multiplayer", "spiffo_character", "spiffo_interactable",
          "spiffo_weather", "spiffo_fishing", "spiffo_ranching", "spiffo_cleaning"]


def read_pack(path):
    """텍스처 묶음에서 {이름: (페이지 PNG 바이트, x, y, w, h)} 를 만든다.

    새 형식은 "PZPK" 로 시작하고 페이지 PNG 앞에 길이가 있다. 옛 형식은 페이지 수로 시작하고
    PNG 뒤에 DEADBEEF 표식이 붙는다.
    """
    data = path.read_bytes()
    new = data[:4] == b"PZPK"
    if new:
        _, npages = struct.unpack_from("<ii", data, 4)
        pos = 12
    else:
        (npages,) = struct.unpack_from("<i", data, 0)
        pos = 4

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
        if new:
            (size,) = struct.unpack_from("<i", data, pos)
            png = data[pos + 4 : pos + 4 + size]
            pos += 4 + size
        else:
            end = data.index(b"IEND", pos) + 8
            png = data[pos:end]
            pos = end
            if data[pos : pos + 4] == b"\xef\xbe\xad\xde":
                pos += 4
        if png[:4] != b"\x89PNG":
            raise SystemExit(f"페이지 PNG 를 찾지 못했습니다: {path}")
        for name, x, y, w, h in page_entries:
            entries[name] = (png, x, y, w, h)
    return entries


def save(img, dest, lossless=True, max_side=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if max_side and max(img.size) > max_side:
        img = img.copy()
        img.thumbnail((max_side, max_side), Image.LANCZOS)
    if lossless:
        img.save(dest, "WEBP", lossless=True, method=6)
    else:
        img.save(dest, "WEBP", quality=86, method=6)


def main():
    game = Path(sys.argv[1] if len(sys.argv) > 1 else "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid")
    media = game / "media"
    missing = []
    count = 0

    pack = read_pack(media / "texturepacks/UI2.pack")
    pages = {}
    for name in VEHICLE_UI:
        if name not in pack:
            missing.append(name)
            continue
        png, x, y, w, h = pack[name]
        if id(png) not in pages:
            pages[id(png)] = Image.open(io.BytesIO(png)).convert("RGBA")
        save(pages[id(png)].crop((x, y, x + w, y + h)), OUT / "vehicle" / f"{name}.webp")
        count += 1

    pack.update({k: v for k, v in read_pack(media / "texturepacks/UI.pack").items() if k not in pack})
    for name in ITEM_ICONS:
        key = f"Item_{name}"
        if key not in pack:
            missing.append(key)
            continue
        png, x, y, w, h = pack[key]
        if id(png) not in pages:
            pages[id(png)] = Image.open(io.BytesIO(png)).convert("RGBA")
        save(pages[id(png)].crop((x, y, x + w, y + h)), OUT / "item" / f"{name}.webp")
        count += 1

    for name in VEHICLE_LOOSE:
        src = media / "ui/vehicles" / f"{name}.png"
        if not src.exists():
            missing.append(name)
            continue
        save(Image.open(src).convert("RGBA"), OUT / "vehicle" / f"{name}.webp")
        count += 1

    # 정비 화면: 차체 그림과 부품별 흰색 마스크(게임은 상태에 따라 색을 입힌다)
    for src in sorted((media / "ui/vehicles/mechanic overlay").glob("4door_*.png")):
        save(Image.open(src).convert("RGBA"), OUT / "mech" / f"{src.stem}.webp")
        count += 1

    for name in SPIFFO:
        src = media / "ui/survival_guide_spiffo" / f"{name}.png"
        if not src.exists():
            missing.append(name)
            continue
        save(Image.open(src).convert("RGBA"), OUT / "spiffo" / f"{name}.webp", lossless=False, max_side=360)
        count += 1

    for name in SIDEBAR:
        src = media / "ui/Sidebar/64" / f"{name}.png"
        if not src.exists():
            missing.append(name)
            continue
        save(Image.open(src).convert("RGBA"), OUT / "sidebar" / f"{name}.webp")
        count += 1

    moodles = media / "ui/Moodles/64"
    for src in sorted(moodles.glob("*.png")):
        if src.stem.startswith("_Moodles_BGoutline"):
            continue
        save(Image.open(src).convert("RGBA"), OUT / "moodle" / f"{src.stem}.webp")
        count += 1

    total = sum(f.stat().st_size for f in OUT.rglob("*.webp"))
    print(f"그림 {count}개 저장, 합계 {total / 1024:.0f}KB")
    if missing:
        print("찾지 못한 그림:", missing)


if __name__ == "__main__":
    main()
