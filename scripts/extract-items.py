"""게임 파일에서 아이템 도감 데이터와 아이콘을 뽑아 사이트용 데이터로 만든다.

    python -I scripts/extract-items.py "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"

처음 하는 사람이 아이템을 검색해서 무엇인지, 어디에 쓰는지(제작법), 어디서 구하는지를
알 수 있게 한다. 손으로 옮겨 적으면 패치마다 틀리므로 게임이 쓰는 정의 파일을 그대로 읽는다.

읽는 것 (게임 폴더는 읽기만 한다)
- media/scripts/**/*.txt
    item 블록(아이템), craftRecipe 블록(제작법), entity 의 CraftRecipe 부품(건축),
    xuiSkin 의 entity DisplayName(건축물 영어 이름)
- media/lua/shared/Translate/{KO,EN}/*.json (이름·분류·기술·제작법·용기 이름)
- media/lua/server/Items/*Distribution*.lua, media/lua/server/Vehicles/VehicleDistribution*.lua (나오는 곳)
- media/lua/shared/Foraging/Categories/*.lua (채집으로 얻는 것)
- media/texturepacks/*.pack 과 media 아래 낱개 Item_*.png (아이콘)

쓰는 것
- web/public/data/items-index.json  검색용 (id, 이름, 영문, 분류, 아이콘, 무게, 짧은 요약)
- web/public/data/items-detail.json 나머지 (수치, 제작법, 나오는 곳, 뜻풀이 표)
- web/public/icons/item/<아이콘 이름>.webp (무손실). 같은 아이콘은 한 번만 저장한다.

같은 게임 파일로 다시 돌리면 같은 결과가 나온다(날짜·순서에 따라 바뀌는 값을 넣지 않는다).
아이콘은 The Indie Stone 의 것이며 사이트에 출처를 밝힌다.

확률 계산은 projectzomboid.jar 의 ItemPickerJava.getActualSpawnChance 를 따랐다.
  한 번 굴릴 때 확률(1/10000 단위) = 가중치 × 100 × 루트 배율 (+ 좀비 밀도 보정)
  루트 배율 기본값은 0.6(샌드박스 *LootNew 기본값), 잡동사니(junk) 목록은 가중치 × 1.4, 배율 1.0.
  좀비 밀도 보정과 시간이 지나며 줄어드는 배율은 넣지 않았다. 그래서 '대략'의 확률이다.
"""

import gzip
import io
import json
import math
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DATA = ROOT / "web/public/data"
OUT_ICONS = ROOT / "web/public/icons/item"
ICON_URL = "icons/item"

LOOT_MODIFIER = 0.6  # 샌드박스 루트 설정 기본값 (SandboxOptions *LootNew)
LOOT_TOP = 6  # 아이템마다 남길 '나오는 곳' 개수

# ─────────────────────────────────────────────────────────────
# 사람이 읽는 이름 표. 게임 번역에 없는 것만 여기서 채운다.
# ─────────────────────────────────────────────────────────────

# PerkFactory.init() 에서 기술 id → 번역 키(IGUI_perks_<키>). 목공(Woodwork)은 Carpentry 키를 쓴다.
PERK_KEY = {
    "Combat": "CombatMelee", "Firearm": "CombatFirearms", "Woodwork": "Carpentry",
    "PlantScavenging": "Foraging", "Lightfoot": "Lightfooted", "Sneak": "Sneaking",
}
# 스크립트에 기술 id 대신 다른 이름을 쓴 곳 (책의 SkillTrained 등)
SKILL_ALIAS = {"Carpentry": "Woodwork", "FirstAid": "Doctor", "Foraging": "PlantScavenging"}
# 게임 한국어 번역이 비어 있는 기술
PERK_FALLBACK = {"Tracking": "추적"}

# 무기 Categories → 기술
WEAPON_SKILL = {
    "axe": "Axe", "blunt": "Blunt", "smallblunt": "SmallBlunt", "longblade": "LongBlade",
    "smallblade": "SmallBlade", "spear": "Spear",
}

# projectzomboid.jar 의 AmmoType / ItemKey 에서 확인한 탄약 종류 → 탄약 아이템
AMMO_ITEM = {
    "base:bullets_3030": "Base.3030Bullets", "base:bullets_308": "Base.308Bullets",
    "base:bullets_357": "Base.Bullets357", "base:bullets_38": "Base.Bullets38",
    "base:bullets_44": "Base.Bullets44", "base:bullets_45": "Base.Bullets45",
    "base:bullets_556": "Base.556Bullets", "base:bullets_9mm": "Base.Bullets9mm",
    "base:cap_gun_cap": "Base.CapGunCap", "base:shotgun_shells": "Base.ShotgunShells",
}

# ItemType → 번역 키(IGUI_ItemCat_*). 번역 키가 없는 것은 TYPE_NAMES 로 바로 이름을 준다.
TYPE_CATEGORY = {
    "normal": "Item", "food": "Food", "weapon": "Weapon", "clothing": "Clothing", "container": "Container",
    "drainable": "Drainable", "literature": "Literature", "key": "Key", "alarmclock": "AlarmClock",
    "alarmclockclothing": "AlarmClock", "radio": "Devices", "map": "Cartography", "weaponpart": "WeaponPart",
}
TYPE_NAMES = {"moveable": "바닥에 놓는 물건"}

# 제작법 분류 (IGUI_CraftingCategories_*, IGUI_CraftCategory_* 에 없는 것)
CATEGORY_FALLBACK = {
    "Blacksmithing": "대장일", "Tools": "도구", "Miscellaneous": "기타", "Blade": "칼날",
    "Cookware": "조리 도구", "Armor": "방어구", "Carpentry": "목공", "Welding": "용접",
    "Outdoors": "야외", "Wall Coverings": "벽 마감", "Furniture": "가구",
}

# 제작법 Tags 중 작업대가 필요한 것 (KO 번역이 비어 있어 건축물 한국어 이름을 참고해 정했다)
STATIONS = {
    "PrimitiveForge": "원시적인 대장간", "Forge": "간단한 대장간 이상", "AdvancedForge": "고급 대장간",
    "PrimitiveFurnace": "원시적인 용광로", "Furnace": "간단한 용광로 이상", "AdvancedFurnace": "고급 용광로",
    "KilnSmall": "소형 가마", "KilnLarge": "대형 가마", "DomeKiln": "돔 가마", "WoodCharcoal": "숯 탄화통·숯 굽는 더미",
    "PotteryWheel": "도자기 물레", "PotteryBench": "도예 작업대", "HandPress": "수동 압착기",
    "DryingRackHerb": "약초 건조대", "DryingRackGrain": "곡물 건조대",
    "DryLeatherLarge": "가죽 건조대", "DryLeatherMedium": "가죽 건조대", "DryLeatherSmall": "가죽 건조대",
    "StandingDrillPress": "탁상 드릴", "MetalBandsaw": "금속 띠톱", "Grindstone": "숫돌",
    "Stone_Mill": "돌 방앗간", "Stone_Quern": "맷돌", "SpinningWheel": "물레", "Weaving": "직조기",
    "Heckling": "아마 빗", "Rippling": "아마 탈각대", "Scutching": "아마 줄기 연화대",
    "TanLeather": "무두질 통", "RemoveFlesh": "가죽 처리대", "RemoveFur": "가죽 처리대",
    "ChurnBucket": "버터 교반기", "CoffeeMachine": "커피 머신", "Toaster": "토스터",
    "ChoppingBlock": "장작 패는 받침대", "KeyDuplicator": "열쇠 복사기",
}

# 사람이 이해하기 쉬운 태그 뜻 (도구 역할 위주). 여기 없는 태그는 tags 에만 남는다.
TAG_NAMES = {
    "base:hammer": "망치", "base:ballpeenhammer": "볼핀 해머", "base:clubhammer": "클럽 해머",
    "base:smithinghammer": "대장장이 망치", "base:sledgehammer": "오함마", "base:mallet": "나무 망치",
    "base:hammerstone": "돌망치", "base:stonemaul": "돌 메",
    "base:saw": "톱", "base:smallsaw": "작은 톱", "base:crudesaw": "조잡한 톱", "base:metalsaw": "쇠톱",
    "base:sharpknife": "날카로운 칼", "base:dullknife": "무딘 칼", "base:meatcleaver": "고기 써는 칼",
    "base:scissors": "가위", "base:sewingneedle": "바느질 바늘", "base:knittingneedles": "뜨개바늘",
    "base:awl": "송곳", "base:screwdriver": "드라이버", "base:wrench": "렌치", "base:pipewrench": "파이프 렌치",
    "base:lugwrench": "휠 렌치", "base:pliers": "펜치", "base:visegrips": "바이스 그립",
    "base:metalworkingpliers": "금속 세공용 집게", "base:tongs": "대장간 집게", "base:crudetongs": "조잡한 집게",
    "base:file": "쇠줄", "base:smallfiles": "작은 줄", "base:whetstone": "숫돌",
    "base:drillwood": "목공 드릴", "base:drillwoodpoor": "조잡한 목공 드릴", "base:drillmetal": "금속 드릴",
    "base:metalworkingpunch": "금속 펀치", "base:smallpunch": "작은 펀치",
    "base:metalworkingchisel": "금속 끌", "base:carpentrychisel": "목공 끌", "base:masonschisel": "석공 끌",
    "base:crudechisel": "조잡한 끌", "base:masonstrowel": "석공 흙손", "base:plastertrowel": "미장 흙손",
    "base:sheetmetalsnips": "판금 가위", "base:lightmetalsnips": "경금속 가위", "base:boltcutters": "볼트 커터",
    "base:weldingmask": "용접 마스크", "base:headingtool": "못 머리 성형 도구", "base:knappingtool": "석기 가공 도구",
    "base:fleshingtool": "가죽 손질 도구", "base:claytool": "점토 도구", "base:mortarpestle": "절구와 공이",
    "base:rollingpin": "밀대", "base:mixingutensil": "섞는 도구", "base:spoon": "숟가락", "base:fork": "포크",
    "base:bowl": "그릇", "base:canopener": "캔 따개", "base:bottleopener": "병따개", "base:corkscrew": "코르크 따개",
    "base:pizzacutter": "피자 커터", "base:paintbrush": "페인트 붓", "base:breakfiber": "섬유 두드리개",
    "base:pickaxe": "곡괭이", "base:crowbar": "쇠지렛대", "base:prybar": "지렛대",
    "base:railroadspikepuller": "철도 못 뽑개", "base:tweezers": "핀셋",
    "base:choptree": "나무 베기", "base:cutplant": "풀·작물 베기", "base:digplow": "땅 파기·밭 갈기",
    "base:diggrave": "무덤 파기", "base:digworms": "지렁이 캐기", "base:removebarricade": "바리케이드 뜯기",
    "base:removeglass": "깨진 유리 치우기", "base:removebullet": "몸에 박힌 총알 빼기", "base:removestump": "그루터기 뽑기",
    "base:clearashes": "재 치우기", "base:takedirt": "흙 담기", "base:takedung": "배설물 치우기",
    "base:startfire": "불 붙이기", "base:lighter": "라이터", "base:refillablelighter": "충전식 라이터",
    "base:isfirefuel": "땔감", "base:isfiretinder": "불쏘시개",
    "base:killanimal": "동물 잡기", "base:butcheranimal": "동물 손질", "base:shear": "털 깎기",
    "base:scythe": "큰 낫", "base:handscythe": "낫",
    "base:sharpenable": "날을 갈 수 있음", "base:repairwithtape": "테이프로 수리", "base:repairwithglue": "접착제로 수리",
    "base:repairwithepoxy": "에폭시로 수리",
    "base:flashlight": "손전등", "base:usesbattery": "건전지 사용", "base:gasmask": "방독면", "base:respirator": "호흡기",
    "base:hazmatsuit": "방호복", "base:scba": "공기 호흡기", "base:improvisedgasmask": "즉석 방독면",
    "base:pen": "펜", "base:write": "글쓰기", "base:dice": "주사위", "base:bucket": "양동이",
    "base:carkey": "차 열쇠", "base:buildingkey": "건물 열쇠", "base:keyring": "열쇠고리",
    "base:purifywater": "물 정화", "base:siphongas": "기름 빼기(사이펀)", "base:petrol": "휘발유 통",
    "base:fishingrod": "낚싯대", "base:fishingline": "낚싯줄", "base:fishinghook": "낚싯바늘",
    "base:fishingspear": "작살", "base:fishingnet": "어망", "base:cleanstains": "얼룩 지우기",
    "base:magnifier": "돋보기", "base:compass": "나침반", "base:whistle": "호루라기", "base:megaphone": "확성기",
    "base:optics": "망원경·쌍안경", "base:reusablebandage": "빨아서 다시 쓰는 붕대", "base:canbewashed": "빨 수 있음",
    "base:thread": "실", "base:heavythread": "굵은 실", "base:twine": "노끈", "base:rope": "밧줄",
    "base:tape": "테이프", "base:glue": "접착제", "base:epoxy": "에폭시", "base:charcoal": "숯",
    "base:concrete": "시멘트", "base:log": "통나무", "base:paint": "페인트", "base:wallpaper": "벽지",
    "base:wallpaperpaste": "벽지 풀", "base:garbagebag": "쓰레기봉투", "base:simpleweaponbinding": "무기 묶는 끈",
    "base:binding": "묶는 재료", "base:ammo": "탄약", "base:firearm": "총기", "base:generator": "발전기",
    "base:carbattery": "차 배터리", "base:wholetire": "타이어", "base:cookable": "불에 올려 데울 수 있음",
    "base:cookablemicrowave": "전자레인지에 데울 수 있음", "base:fitstoaster": "토스터에 넣음", "base:herbaltea": "약초차 재료",
    "base:isseed": "씨앗", "base:iscompostable": "퇴비로 씀", "base:fertilizer": "비료", "base:compost": "퇴비",
    "base:holddirt": "흙 담는 그릇", "base:holdcompost": "퇴비 담는 그릇", "base:smokable": "피울 수 있음",
    "base:alcoholicbeverage": "술", "base:glassbottle": "유리병", "base:emptycan": "빈 깡통", "base:tincan": "깡통",
    "base:jar": "유리 단지", "base:ismemento": "기념품", "base:magazine": "잡지", "base:newspaper": "신문",
    "base:hollowbook": "속을 파낼 수 있는 책", "base:sheet": "침대 시트", "base:pillow": "베개",
    "base:tentpeg": "텐트 말뚝", "base:metalpiece": "금속 조각", "base:stone": "돌", "base:glass": "유리",
    "base:lighterfluid": "라이터 기름", "base:sugar": "설탕", "base:flour": "밀가루", "base:egg": "달걀",
    "base:bakingfat": "제빵용 기름", "base:fishmeat": "생선살", "base:uncutfish": "손질 안 한 생선",
    "base:button": "단추", "base:barstock": "금속 막대", "base:barstockhalf": "금속 막대(1/2)",
    "base:barstockquarter": "금속 막대(1/4)", "base:smallsheetmetal": "작은 금속판", "base:wire": "철사",
    "base:aluminum": "알루미늄", "base:limestone": "석회석", "base:gasmaskfilter": "방독면 필터",
    "base:respiratorfilter": "호흡기 필터", "base:vermin": "해충·쥐",
}

# 요약에 쓰기엔 덜 중요한 태그 (뜻풀이 목록에서도 뒤로 보낸다)
MINOR_TAGS = {
    "base:isfirefuel", "base:isfiretinder", "base:cookable", "base:cookablemicrowave", "base:repairwithtape",
    "base:repairwithglue", "base:repairwithepoxy", "base:sharpenable", "base:canbewashed", "base:ismemento",
    "base:hollowbook", "base:magazine", "base:newspaper", "base:usesbattery", "base:fitstoaster", "base:herbaltea",
    "base:iscompostable", "base:vermin", "base:glass", "base:stone",
}

# 착용 부위 (BodyLocation). _texture 로 끝나는 것은 앞부분으로 찾는다.
BODY_LOCATIONS = {
    "hat": "모자", "fullhat": "머리 전체(헬멧)", "mask": "마스크", "maskeyes": "눈가리개", "maskfull": "전면 마스크",
    "eyes": "눈(안경)", "righteye": "오른쪽 눈", "lefteye": "왼쪽 눈", "ears": "귀", "eartop": "귀 윗부분", "nose": "코",
    "neck": "목", "necklace": "목걸이", "necklace_long": "긴 목걸이", "scarf": "스카프", "gorget": "목 보호대",
    "tshirt": "티셔츠", "shirt": "셔츠", "shortsleeveshirt": "반팔 셔츠", "tanktop": "민소매", "sweater": "스웨터",
    "sweaterhat": "후드 스웨터", "jersey": "저지", "jacket": "재킷", "jacket_bulky": "두꺼운 재킷", "jacket_down": "패딩",
    "jacketsuit": "정장 재킷", "jackethat": "후드 재킷", "jackethat_bulky": "두꺼운 후드 재킷",
    "torsoextra": "상체 덧옷", "torsoextravest": "조끼", "torsoextravestbullet": "방탄조끼", "vest": "조끼",
    "cuirass": "흉갑", "dress": "원피스", "longdress": "긴 원피스", "skirt": "치마", "longskirt": "긴 치마",
    "pants": "바지", "pants_skinny": "딱 붙는 바지", "shortpants": "반바지", "shortsshort": "짧은 반바지",
    "pantsextra": "덧바지", "legs1": "다리", "underwear": "속옷", "underweartop": "속옷 상의",
    "underwearbottom": "속옷 하의", "underwearextra1": "속옷(추가)", "underwearextra2": "속옷(추가)",
    "socks": "양말", "shoes": "신발", "hands": "손(장갑)", "handsleft": "왼손", "handsright": "오른손",
    "leftwrist": "왼쪽 손목", "rightwrist": "오른쪽 손목", "left_ringfinger": "왼손 약지", "right_ringfinger": "오른손 약지",
    "left_middlefinger": "왼손 중지", "right_middlefinger": "오른손 중지", "back": "등(배낭)", "satchel": "어깨에 메는 가방",
    "fannypackfront": "허리 가방(앞)", "fannypackback": "허리 가방(뒤)", "webbing": "웨빙 벨트", "belt": "벨트",
    "beltextra": "벨트(추가)", "ammostrap": "탄띠", "shoulderholster": "어깨 권총집", "ankleholster": "발목 권총집",
    "bellybutton": "배꼽 피어싱", "shoulderpadleft": "왼쪽 어깨 보호대", "shoulderpadright": "오른쪽 어깨 보호대",
    "sportshoulderpad": "스포츠 어깨 보호대", "sportshoulderpadontop": "스포츠 어깨 보호대",
    "elbow_left": "왼쪽 팔꿈치 보호대", "elbow_right": "오른쪽 팔꿈치 보호대",
    "forearm_left": "왼쪽 팔뚝 보호대", "forearm_right": "오른쪽 팔뚝 보호대",
    "thigh_left": "왼쪽 허벅지 보호대", "thigh_right": "오른쪽 허벅지 보호대",
    "knee_left": "왼쪽 무릎 보호대", "knee_right": "오른쪽 무릎 보호대",
    "calf_left": "왼쪽 정강이", "calf_right": "오른쪽 정강이", "gaiter_left": "왼쪽 각반", "gaiter_right": "오른쪽 각반",
    "codpiece": "낭심 보호대", "boilersuit": "멜빵 작업복", "fullsuit": "전신복", "fullsuithead": "전신복(머리 포함)",
    "fulltop": "상의 전체", "torso1legs1": "상하의", "bathrobe": "목욕 가운", "tail": "꼬리",
    "scba": "공기통", "scbanotank": "공기 호흡기", "leftarm": "왼팔", "rightarm": "오른팔",
}

# 채집 구역 (IGUI_SearchMode_Zone_Names_* 한국어가 비어 있는 것)
FORAGE_ZONE_FALLBACK = {
    "BirchForest": "자작나무 숲", "BirchMixForest": "자작나무 혼합림", "OrganicForest": "비옥한 숲",
    "PHForest": "산성 토양 숲", "PHMixForest": "산성 토양 혼합림", "PRForest": "원시림",
    "FarmForest": "관리림", "FarmMixForest": "농지 숲", "ForagingNav": "길가",
}

# 요리 재료로 쓰이는 요리 (EvolvedRecipe). Recipes.json 에 번역이 없는 것만.
EVOLVED_FALLBACK = {
    "Pasta": "파스타", "Rice": "밥", "Pizza": "피자", "PieSweet": "달콤한 파이", "Hotdog": "핫도그",
    "Toast": "토스트", "Bread": "빵", "ConeIcecream": "아이스크림 콘", "ConeIceCream": "아이스크림 콘",
    "AddBaitToChum": "떡밥",
}

# 건축(엔티티) 제작법 중 게임 한국어 번역이 없는 것. 게임처럼 단계(Lvl1~3)는 이름에 넣지 않고 tier 로 따로 둔다.
BUILD_NAMES = {
    "BarrelOven": "금속 드럼통 오븐", "BarricadeMetalBar": "금속 막대 바리케이드", "BarricadeMetalSheet": "금속판 바리케이드",
    "BarricadePlanks": "판자 바리케이드", "BrickDoorFrame": "벽돌 문틀", "BrickFloor": "타일 바닥",
    "ChickenHutch": "닭장", "ChickenHutch2": "닭장 (2)", "Chopping_Block": "장작 패는 받침대",
    "ComposterShoddy": "조잡한 퇴비통", "Cooking_Pit": "요리용 화덕", "Kiln_Large": "대형 가마", "Kiln_Small": "소형 가마",
    "LeanTo_Shelter": "간이 차양 쉼터", "Leather_Shelter": "가죽 쉼터", "LogDoorFrame": "통나무 문틀",
    "LogGate": "넓은 통나무 문", "LogWindowFrame": "통나무 창문틀", "Log_Bench": "통나무 벤치",
    "Log_Stairs": "통나무 계단", "Log_Stool": "통나무 의자", "Log_Table": "통나무 탁자", "MetalDoor": "금속 문",
    "MetalFence": "금속 울타리", "Paint_SignArrowDown": "페인트 표지 (아래 화살표)",
    "Paint_SignArrowLeft": "페인트 표지 (왼쪽 화살표)", "Paint_SignArrowRight": "페인트 표지 (오른쪽 화살표)",
    "Paint_SignArrowUp": "페인트 표지 (위 화살표)", "Paint_SignSkull": "페인트 표지 (해골)", "Paint_Wall": "벽 페인트칠",
    "Paper_Wall": "벽지 바르기", "Plaster_Wall": "벽 미장", "Pottery_Bench": "도예 작업대", "Pottery_Wheel": "도자기 물레",
    "RainCollector": "빗물 받이 상자", "RainCollectorRound": "빗물 받이 통", "RainCollectorRound_Tarp": "방수포 빗물 받이 통",
    "RainCollector_Tarp": "방수포 빗물 받이 상자", "Rugged_Stool": "투박한 의자", "Rugged_Table": "투박한 탁자",
    "Simple_Cooking_Pit": "간단한 요리용 화덕", "Simple_Drying_Rack": "간단한 큰 식물 건조대",
    "Simple_Herb_Drying_Rack": "간단한 약초 건조대", "SkullPoleAntlers": "사슴뿔 장대", "SkullPoleBull": "황소 두개골 장대",
    "SkullPoleCow": "소 두개골 장대", "SkullPoleDeer": "수사슴 두개골 장대", "SkullPoleDeerDoe": "암사슴 두개골 장대",
    "SkullPolePig": "돼지 두개골 장대", "SkullPoleSheep": "양 두개골 장대", "Spinning_Wheel": "물레",
    "Stick_Bookcase": "나뭇가지 책장", "Stick_BookcaseSmall": "나뭇가지 소형 책장", "StoneCairn": "돌무더기",
    "Stone_Cabinet": "돌 수납장", "Stone_Mill": "돌 방앗간", "Stone_Quern": "맷돌", "Tarp_Shelter": "방수포 쉼터",
    "WoodStake": "나무 말뚝", "Wood_Crate": "나무 상자", "Wood_ShelvesDouble": "나무 2단 선반", "Wood_Shelves": "나무 선반",
    "Wood_Table": "나무 탁자", "WoodenPole": "나무 기둥", "WoodenWallFrame": "나무 벽틀", "WoodenWall": "나무 벽",
    "Wooden_Windows": "나무 창문",
}

# ── 나오는 곳 이름 ──
# 분포 목록 이름(예: ToolStoreTools)을 낱말로 쪼개 한국어로 옮긴다. 낱말 하나라도 모르면 원래 이름을 둔다.
# 먼저 아래 통째 번역을 보고, 없으면 여러 낱말 묶음 → 낱말 순서로 찾는다.
PLACE_FULL = {
    "KitchenCounter": "부엌 조리대", "KitchenRandom": "부엌 잡동사니", "KitchenDryFood": "부엌 마른 식품",
    "KitchenCannedFood": "부엌 통조림", "KitchenPots": "부엌 냄비", "KitchenBook": "부엌 요리책",
    "ToolStoreTools": "철물점 공구 진열대", "ToolStoreCarpentry": "철물점 목공 용품", "ToolStoreMisc": "철물점 잡화",
    "ToolStoreFarming": "철물점 농사 용품", "ToolStoreMetalwork": "철물점 금속 공예 용품",
    "GarageTools": "차고 공구", "GarageCarpentry": "차고 목공 용품", "GarageMechanics": "차고 정비 용품",
    "GarageFirearms": "차고 총기", "CrateTools": "공구 상자", "CrateToolsOld": "낡은 공구 상자",
    "MeleeWeapons": "근접 무기 보관함", "MeleeWeapons_Mid": "근접 무기 보관함 (중반)", "MeleeWeapons_Late": "근접 무기 보관함 (후반)",
    "JunkHoard": "쌓아 둔 잡동사니", "CrateRandomJunk": "잡동사니 상자", "RandomFiller": "아무 물건",
    "SurvivalGear": "생존 장비", "Homesteading": "자급자족 용품", "Antiques": "골동품", "Hobbies": "취미 용품",
    "Trapper": "덫 사냥꾼 물건", "Hiker": "등산객 물건", "Hunter": "사냥꾼 물건", "Gifts": "선물",
    "HolidayStuff": "명절 장식", "VacationStuff": "휴가 용품", "Photographer": "사진가 물건",
    "BedroomDresser": "침실 서랍장", "BedroomDresserChild": "아이 침실 서랍장", "BedroomSidetable": "침실 협탁",
    "BedroomSidetableChild": "아이 침실 협탁", "WardrobeChild": "아이 옷장",
    "MedicalStorageDrugs": "의료 창고 약품", "MedicalStorageTools": "의료 창고 도구", "MedicalClinicDrugs": "진료소 약품",
    "PharmacyCosmetics": "약국 화장품", "BathroomCounter": "욕실 수납장", "BathroomCabinet": "욕실 수납장",
    "FridgeGeneric": "냉장고", "FreezerGeneric": "냉동고", "BinGeneric": "쓰레기통",
    "ArmySurplusOutfit": "군용품점 복장", "PoliceEvidence": "경찰 증거물 보관함", "BankDeposit": "은행 대여금고",
    "LostAndFoundItems": "분실물 보관소 물건", "LostAndFoundClothing": "분실물 보관소 옷",
    "NolansDesk": "놀란 중고차 책상", "NolansFilingCabinet": "놀란 중고차 서류함",
    "CarDealerDesk": "자동차 대리점 책상", "CarDealerFilingCabinet": "자동차 대리점 서류함",
    "DrugShackWeapons": "마약 판잣집 무기", "DrugShackTools": "마약 판잣집 공구", "DrugShackMisc": "마약 판잣집 잡화",
    "DrugShackDrugs": "마약 판잣집 마약",
    "Mayor_West_point": "웨스트포인트 시장",
}

PLACE_PHRASES = {
    "Tool Store": "철물점", "Gun Store": "총포상", "Army Surplus": "군용품점", "Living Room": "거실",
    "Break Room": "휴게실", "Filing Cabinet": "서류함", "Serving Tray": "서빙 쟁반", "Serving Trays": "서빙 쟁반",
    "Lost And Found": "분실물 보관소", "Wild West": "서부 시대", "West Point": "웨스트포인트", "Pawn Shop": "전당포",
    "Car Dealer": "자동차 대리점", "Car Supply": "자동차 용품점", "Strip Club": "스트립 클럽",
    "Department Store": "백화점", "Ice Cream": "아이스크림", "Sci Fi": "공상과학", "Blue Collar": "육체노동",
    "Rail Yard": "철도 기지", "Bell Peppers": "피망", "Sweet Potatoes": "고구마", "Spring Rolls": "춘권",
    "Refried Beans": "리프라이드 빈", "Tato Dots": "감자볼", "C Ds": "CD", "Compact Discs": "CD",
    "Trailer Park": "트레일러 공원", "Fire Station": "소방서", "Fire Dept": "소방서", "Post Office": "우체국",
    "Music School": "음악 학교", "Bowling Alley": "볼링장", "Jays Chicken": "제이스 치킨", "Pizza Whirled": "피자 월드",
    "Pile O Crepe": "파일 오 크레페", "Sleeping Bags": "침낭", "Cyber Cafe": "PC방", "Deep Fry": "튀김",
    "Garden Store": "원예점", "Electronic Store": "전자제품점", "Clothing Stores": "옷가게", "Clothing Store": "옷가게",
    "Clothing Storage": "옷가게 창고", "Comic Store": "만화 가게", "Art Store": "화방", "Sport Store": "스포츠 용품점",
    "Sports Store": "스포츠 용품점", "Camping Store": "캠핑 용품점", "Fishing Store": "낚시 용품점",
    "Candy Store": "사탕 가게", "Gift Store": "기념품점", "Music Store": "악기점", "Liquor Store": "주류 판매점",
    "Outdoor Supply": "아웃도어 용품점", "Pet Shop": "반려동물 가게", "Jewelry Store": "보석 가게",
    "Glasses Store": "안경점", "Toy Store": "장난감 가게", "Knife Store": "칼 가게", "Movie Rental": "비디오 대여점",
    "Drug Shack": "마약 판잣집", "Drug Lab": "마약 제조실", "Plank Stash": "마룻바닥 은닉처",
    "Hospital Room": "병실", "Waiting Room": "대기실", "Laundry Load": "세탁물", "Kitchen Counter": "부엌 조리대",
    "Gas 2 Go": "가스투고", "Mass Gen Fac": "매스젠팩", "Matt Hass": "맷 해스", "Metal Welder": "용접공",
    "Construction Worker": "건설 노동자", "Prison Guard": "교도관", "Pack Rat": "수집광", "Bad Teens": "불량 청소년",
    "Step Van": "배달 밴", "Pick Up Truck Lights": "경광등 픽업트럭", "Van Seats": "승합차", "Airport Shuttle": "공항 셔틀",
    "Airport Catering": "공항 기내식", "Marine Bites": "마린 바이츠", "Imported Beer": "수입 맥주",
    "Craft Supplies": "공예 용품", "Mobile Library": "이동 도서관", "Glove Box": "글러브박스", "Truck Bed": "짐칸",
    "Seat Front": "앞좌석", "Seat Rear": "뒷좌석", "Knox Distillery": "녹스 양조장", "K Y Transit": "켄터키 운송",
    "KY Transit": "켄터키 운송", "Army Light": "군용 경트럭", "Army Heavy": "군용 대형 트럭", "Police SWAT": "특수기동대",
    "Police State": "주 경찰", "Police Sheriff": "보안관", "Police Detective": "형사", "Book Store": "서점",
    "Hot Dog": "핫도그", "Hospital Patient": "입원 환자", "Office Worker": "회사원", "Club Goer": "클럽 손님",
    "Honor Student": "우등생", "Poker Dealer": "포커 딜러", "Baseball Player": "야구 선수", "Guitar Guy": "기타 치는 사람",
    "Air port Security": "공항 보안 요원", "Airport Security": "공항 보안 요원", "Ambulance Driver": "구급차 운전사",
    "Fireman Full Suit": "방화복 소방관", "Exterminator Suited": "해충 방제원", "Private Militia": "사설 민병대",
    "Bounty Hunter": "현상금 사냥꾼", "Store Counter": "가게 계산대", "Grocery Storage": "식료품점 창고",
    "Side Table": "협탁", "Sheet Metal": "금속판", "House Electronics": "가전제품", "Non Fiction": "논픽션",
    "Fountain Cups": "음료 컵", "Graham Crackers": "그레이엄 크래커", "Ice Hockey": "아이스하키",
    "Mc Coy": "맥코이 벌목", "Mc Coys": "맥코이 벌목", "Army Camo": "군 위장복", "Security Tarmac": "활주로 보안 요원",
}

PLACE_WORDS = """
Crate=상자 Crates=상자 Store=가게 Stores=가게 Shop=가게 Kitchen=부엌 Storage=창고 University=대학 Tools=공구 Tool=공구
Library=도서관 Desk=책상 Fridge=냉장고 Serving=서빙 Tray=쟁반 Trays=쟁반 Clothing=옷 Clothes=옷 Shelf=선반 Shelves=선반
Bookstore=서점 Counter=카운터 Counters=카운터 Cabinet=수납장 Car=자동차 Factory=공장 Freezer=냉동고 Safehouse=생존자 은신처
Produce=농산물 Army=군 Outfit=복장 Outfits=복장 Filing=서류 Lockers=사물함 Locker=사물함 Room=방 Gigamart=기가마트
Butcher=정육점 Office=사무실 Medical=의료 Books=책 Book=책 Music=음악 Liquor=술 Sport=스포츠 Sports=스포츠 West=서부
Police=경찰 Misc=잡화 Laundry=세탁 Chairs=의자 Chair=의자 Gun=총 Guns=총기 Sauce=소스 Rack=진열대 Modern=현대식
Food=음식 Wild=야생 Baking=제빵 Spiffos=스피포 Spiffo=스피포 Bags=가방 Bag=가방 Stand=가판대 Literature=읽을거리
Bakery=빵집 Bin=쓰레기통 Generic=일반 Surplus=잉여품 Bar=바 Camping=캠핑 Normal=일반 Grocery=식료품점 Magazine=잡지
Magazines=잡지 Knife=칼 Knives=칼 Mechanic=정비소 Mechanics=정비 Art=미술 Stove=스토브 Empty=빈 Bedroom=침실
Classy=고급 School=학교 Cafe=카페 Display=진열 Weapons=무기 Weapon=무기 BBQ=바비큐 Fancy=고급 Golf=골프 Drug=마약
Drugs=마약 Wardrobe=옷장 Living=생활 Prison=교도소 Supplies=용품 Supply=용품 Hospital=병원 Jays=제이스 Fish=생선
Gas=주유소 Comic=만화 Comics=만화 Table=탁자 Tables=탁자 Jewelry=보석 Electronic=전자제품 Electronics=전자제품
Cleaning=청소 Sushi=스시 Medieval=중세 Anthropology=인류학 Cutlery=식기 Snacks=과자 History=역사 Bottles=병 Bottle=병
Cafeteria=구내식당 Metal=금속 Lab=실험실 Laboratory=실험실 Load=세탁물 Ranger=산림 경비대 Cases=진열장 Case=케이스
Paper=종이 Leather=가죽 Bathroom=욕실 Blue=파란 Cinema=영화 Science=과학 Western=서부 Brakes=브레이크
Suspension=서스펜션 Chips=감자칩 Random=잡다한 House=집 Garage=차고 Armor=방어구 Gym=체육관 Pizza=피자 Tobacco=담배
Backstage=무대 뒤 Dresser=서랍장 Dressers=서랍장 Redneck=시골 Beer=맥주 Fire=소방 Computer=컴퓨터 Computers=컴퓨터
Fiction=소설 Legal=법률 Cans=캔 Burger=버거 Muffler=머플러 Mufflers=머플러 Tires=타이어 Workshop=작업장 Chinese=중식
Classroom=교실 Wooden=나무 Derelict=폐가 Accessories=액세서리 Acessories=액세서리 Meat=고기 Side=곁 Sidetable=협탁
Post=우체국 Band=밴드 Motel=모텔 Business=경영 Farming=농사 Philosophy=철학 Politics=정치 Boxing=권투 Brewery=양조장
Chicken=치킨 Drinks=음료 Boots=부츠 Worker=노동자 Comfy=푹신한 Canned=통조림 Fabric=천 White=흰 Red=빨간 Salon=미용실
Vegetables=채소 Vegetable=채소 Veg=채소 Home=가정 Italian=이탈리안 Mexican=멕시칸 Pawn=전당포 Plank=판자 Stash=은닉처
Fried=튀김 Theatre=극장 Bunker=벙커 Ammunition=탄약 Ammo=탄약 Footwear=신발 Water=물 Pottery=도예 Glasses=안경
Rich=부유층 Crepe=크레페 Blacksmith=대장간 Blacksmithing=대장일 Fashion=패션 General=일반 Occult=오컬트 Religion=종교
Bowling=볼링 Gloves=장갑 Spices=향신료 Mix=혼합 Mixed=혼합 Gear=장비 Carpentry=목공 Jackets=재킷 Woman=여성
Soda=탄산음료 Black=검은 Plastic=플라스틱 Dark=어두운 Fishing=낚시 Oven=오븐 Paint=페인트 Junk=잡동사니 Wine=와인
Dog=개 Shack=판잣집 Potatoes=감자 Special=특별 Janitor=관리인 Jerky=육포 Lingerie=란제리 Whiskey=위스키
Seafood=해산물 Wire=철사 Arena=경기장 Hangar=격납고 Boxes=상자 Box=상자 Headwear=모자 Other=기타 Others=기타
Merch=굿즈 Practice=연습 Instruments=악기 Baseball=야구 Charcoal=숯 Propane=프로판 Child=아이 Childs=아이 Kids=아이
Garden=정원 Gardening=원예 Biography=전기 Crime=범죄 Fantasy=판타지 Reference=참고서 Military=군사 New=새
Personal=개인 Shoes=신발 Break=휴게 Dining=식당 Fruit=과일 Fruits=과일 Camera=카메라 Lighting=조명 Candy=사탕
Windows=창호 Catfish=메기 Secondary=중등 Clock=시계 Repair=수리 Watches=손목시계 Closet=벽장 Equipment=용품
All=전체 Shirts=셔츠 Formal=정장 Pants=바지 Underwear=속옷 Cortman=코트먼 Brown=갈색 Low=낮은 Buns=번
Hotdog=핫도그 Hotdogs=핫도그 Sinks=싱크대 Dishes=접시 Dish=접시 Denim=데님 Weights=운동기구 Cups=컵 Balls=공
Green=초록 Grey=회색 Large=큰 Round=둥근 Maps=지도 Pipes=파이프 Metalwork=금속 공예 Napkins=냅킨 Newspapers=신문
Newspaper=신문 Tailoring=재봉 Toys=장난감 Daycare=어린이집 Fry=튀김 Diner=식당 Firearm=총기 Firearms=총기
Hoarder=저장강박자 Hoard=더미 Hunter=사냥꾼 Hunting=사냥 Gift=선물 Gifts=선물 Pots=냄비 Grill=그릴 Towels=수건
Rings=반지 Wedding=웨딩 Juice=주스 Handles=손잡이 Blades=칼날 Mayor=시장 Point=포인트 Clinic=진료소 Melee=근접
Morgue=영안실 Nolans=놀란 중고차 Outdoor=아웃도어 Outdoors=야외 Studio=스튜디오 Restaurant=식당 Security=경비
Shrimp=새우 SWAT=특수기동대 Welding=용접 Ambulance=구급차 Driver=운전 Backpacks=배낭 Pie=파이 Pool=수영장 Bats=배트
Bat=배트 Cooking=요리 Crafts=공예 Hobbies=취미 Horror=공포 Literary=문학 Age=시대 Romance=로맨스 Thriller=스릴러
Travel=여행 Helmets=헬멧 Chops=촙 Coffee=커피 Tea=차 Legwear=하의 Batteries=건전지 Dealer=딜러 Carpenter=목수
Carving=조각 Chef=요리사 Man=남성 Construction=공사장 Rattan=등나무 Old=낡은 Film=필름 Tomato=토마토
Chocolate=초콜릿 Cigarettes=담배 Clay=점토 Cream=크림 Crackers=크래커 Eggs=달걀 Egg=달걀 Fitness=운동 Generator=발전기
Gravy=그레이비 Industrial=산업 Stone=돌 Stones=돌 Linens=리넨 Long=긴 Oil=기름 Pet=반려동물 Popcorn=팝콘 Purple=보라
Rice=쌀 Sugar=설탕 Taco=타코 TV=TV Tapes=테이프 Wall=벽 Department=백화점 VIP=VIP Lounge=라운지 Doctor=의사
Dryer=건조기 Money=돈 Radio=라디오 Electrician=전기 기사 Farmer=농부 Fireman=소방관 Fisherman=어부 Farm=농장
Trailer=트레일러 Park=공원 Gardener=정원사 Combo=모음 Toiletries=세면도구 Cards=카드 Breakfast=아침 식사
Cosmetics=화장품 Cosmetic=화장품 Dry=건조 Lettuce=양상추 Shotguns=산탄총 Stuff=물건 Chemicals=화학 약품 Gold=금
Knapping=석기 Cleaver=식칼 Suits=정장 Mannequin=마네킹 Mannequins=마네킹 Electric=전기 Nurse=간호사
Optometrist=안경원 Pharmacy=약국 Captain=서장 State=주 Cell=감방 Intake=입소 Loose=낱개 Rotten=썩은 Traps=덫
Fireplace=벽난로 Dumplings=만두 Oysters=굴 Pancakes=팬케이크 Sewing=바느질 Smoking=흡연 Cigars=시가 Spa=스파
Engineering=공학 English=영문학 Glassmaking=유리 공예 Math=수학 Nature=자연 Therapy=치료 Bottling=병입 Barber=이발소
Sheriff=보안관 Antiques=골동품 Antique=골동품 Cots=간이침대 Pen=펜 Rigging=장비 Bread=빵 Cake=케이크 Doughnuts=도넛
Bank=은행 Deposit=금고 Darts=다트 Barn=헛간 Meds=약 Dumpster=대형 쓰레기통 Station=서 Molds=거푸집
Automotive=자동차 Textbook=교과서 Stationery=문구 Pins=핀 Memorabilia=기념품 Hops=홉 Burglar=강도 Smoked=훈제
Mugs=머그컵 Sandwiches=샌드위치 Tents=텐트 Lightbars=경광등 Carnival=축제 Prizes=경품 Materials=재료
Changeroom=탈의실 Chemistry=화학 Church=교회 Poor=가난한 Winter=겨울 Dress=드레스 Dresses=드레스 Eyewear=안경
Holsters=권총집 Jeans=청바지 Jumpers=스웨터 Overshirts=덧셔츠 Socks=양말 Summer=여름 Cobbler=구둣방 Dice=주사위
Games=게임 Control=통제실 Animal=동물 Feed=사료 Baseballs=야구공 Basketballs=농구공 Bibles=성경 Bible=성경
Desert=사막 Butter=버터 Package=포장 Spoiled=상한 Canning=통조림 만들기 Cereal=시리얼 Chest=상자 Bricks=벽돌
Cocoa=코코아 Powder=가루 Coke=콜라 Condiments=조미료 Cones=콘 Cornflour=옥수수 가루 Concrete=시멘트 Costume=의상
Tin=깡통 Espresso=에스프레소 Machine=기계 Cotton=면 Toilets=화장실 Toilet=화장실 Flour=밀가루 Fertilizer=비료
Flint=부싯돌 Nodules=덩어리 Folding=접이식 Footballs=미식축구공 Clubs=클럽 Gravel=자갈 Gum=껌 Heavy=대형
Chains=사슬 Hotsauce=핫소스 Humanitarian=구호 Dye=염료 Light=조명 Lights=조명 Limestone=석회석 Crushed=부순
Stick=막대 Lumber=목재 Macaroni=마카로니 Maple=메이플 Syrup=시럽 Marinara=마리나라 Marshmallows=마시멜로
Masonry=석공 Bars=막대 Oak=참나무 Olive=올리브 Orange=오렌지 Pancake=팬케이크 Pasta=파스타 Peanuts=땅콩
Photos=사진 Plaster=석고 Vinegar=식초 Sand=모래 Seaweed=김 Sheet=판 Sheets=시트 Skeleton=해골 Small=작은
Soccer=축구 Soysauce=간장 Blocks=블록 Sunflower=해바라기 Seeds=씨앗 Shells=산탄 Paste=풀 Tortilla=토르티야
Wide=넓은 VHS=비디오테이프 Finish=마감재 Wallpaper=벽지 Simple=간단한 Stools=의자 Yeast=효모 Yellow=노란
Wallets=지갑 Dispenser=디스펜서 Cultist=사이비 교도 Party=파티 Squatter=무단 거주자 Back=뒤 Dishwasher=식기세척기
Bones=뼈 Appliances=가전제품 HAM=아마추어 무선 Phones=전화기 Engineer=기술자 Bait=미끼 Trainer=트레이너
Gourmet=고급 식품 Forest=숲 Fossoil=포소일 Frozen=냉동 Furniture=가구 Emergency=비상 Bathing=목욕 Bedding=침구
Crisps=감자칩 Goods=용품 Housewares=생활용품 Lightbulb=전구 Glass=유리 Body=바디 Mags=탄창 Pistols=권총
Rifles=소총 Mats=매트 Sweatbands=땀밴드 Hiker=등산객 Holiday=명절 Homesteading=자급자족 Toppings=토핑
Improvised=급조 Jackies=재키 Jeweler=보석상 Gems=보석 Navel=배꼽 Silver=은 Wrist=손목 Jockey=기수 Judge=판사
Microwave=전자레인지 Leatherworking=가죽 공예 Bras=브래지어 Brandy=브랜디 Gin=진 Rum=럼 Scotch=스카치 Tequila=테킬라
Vodka=보드카 Remote=리모컨 Logging=벌목 Items=물건 Adult=성인 Brochure=소책자 Paperback=문고본 Safe=금고
Wheels=바퀴 Alchemy=연금술 Japan=일본 Movie=영화 Rental=대여점 Bass=베이스 Brass=금관악기 Drums=드럼 Guitar=기타
Speaker=스피커 Stringed=현악기 Secretary=비서 Stressed=바쁜 Drawers=서랍 Photographer=사진가 Cheese=치즈
Plumbing=배관 Evidence=증거물 File=파일 Parcels=소포 Guard=경비 Armory=무기고 Objects=물건 Riot=진압
Apples=사과 Broccoli=브로콜리 Cabbages=양배추 Carrots=당근 Cauliflower=콜리플라워 Cherry=체리 Corn=옥수수
Eggplant=가지 Grapes=포도 Greenpeas=완두콩 Kale=케일 Leeks=대파 Onions=양파 Onion=양파 Peaches=복숭아 Pears=배
Radishes=무 Strawberries=딸기 Tomatoes=토마토 Watermelons=수박 Components=부품 Spikes=스파이크 Filler=채움
Rec=오락 Menus=메뉴판 Booze=술 Washer=세탁기 Haircare=헤어 제품 Bad=불량 Seasonal=계절 Biscuits=비스킷
Burgers=버거 Burritos=부리토 Nuggets=너겟 Wings=윙 Cornbread=옥수수빵 Fingers=핑거 Fries=감자튀김 Ham=햄
Lobster=랍스터 Maki=마키 Steam=찜 Mussels=홍합 Noodle=국수 Soup=수프 Omelettes=오믈렛 Onigiri=주먹밥
Perogies=피로그 Potato=감자 Pork=돼지고기 Salmon=연어 Sausage=소시지 Scrambled=스크램블 Steak=스테이크
Tofu=두부 Waffles=와플 Badminton=배드민턴 Football=미식축구 Hockey=하키 Padding=보호대 Tennis=테니스
Sneakers=운동화 Paddles=패들 Racquets=라켓 Sticks=스틱 Straws=빨대 Prop=소품 Survival=생존 Testing=시험
Chew=씹는 Cigarillos=시가릴로 Stock=재고 Ingots=주괴 Saw=톱 Keymaking=열쇠 제작 Trapper=덫 사냥꾼
Electrical=전기 Pioneer=개척 시대 Vacation=휴가 Waiting=대기 Decor=장식 Fuel=연료 Full=가득 Souveniers=기념품
Wood=나무 Barbed=가시 Basic=기본 Woodcraft=목공예 Dude=남자 Zippee=지피 마켓 Survivalist=생존주의자
Agent=요원 Bandit=약탈자 Biker=폭주족 Bob=밥 Camper=캠핑족 Classy=고급 Cook=요리사 Dean=학장 Detective=형사
Duke=듀크 Evacuee=피난민 Foreman=작업반장 Frank=프랭크 Hemingway=헤밍웨이 Gaudy=화려한 Ghillie=길리슈트
Golfer=골퍼 Goth=고스족 Groucho=코주부 Grunge=그런지 Hobbo=노숙자 Hobbyist=취미 생활자 Inmate=수감자
Khaki=카키 Jackie=재키 Jaye=제이 Joan=조앤 John=존 Kate=케이트 Kirsty=커스티 Kormick=코믹 McCoys=맥코이
Mob=조직원 Naked=알몸 Veil=베일 Nolan=놀란 Pharmacist=약사 Priest=신부 Punk=펑크족 Raider=약탈자
Redneck=시골 사람 Rev=목사 Peter=피터 Watts=와츠 Rocker=로커 Sanitation=환경미화원 Sir=서 Twiggy=트위기
Stripper=스트리퍼 Student=학생 Teacher=교사 Thunder=썬더 Tourist=관광객 Trader=상인 Trucker=트럭 운전사
Varsity=대학 대표 선수 Waiter=웨이터 Woodcut=나무꾼 Bathrobe=목욕 가운 Backpacker=배낭 여행자 Patient=환자
Rangers=레인저스 Z=Z KY=켄터키 Lawman=보안관 Boss=두목 Outlaw=무법자 Costume=의상 Cook=요리사 Generic=일반
Taco=타코 Del=델 Pancho=판초 Market=마켓 Gas2Go=가스투고 Pile=파일 Crepe=크레페 Thunder=썬더
Glove=글러브 GloveBox=글러브박스 Truck=트럭 Bed=짐칸 Seat=좌석 Trunk=트렁크 Standard=일반 Luxury=고급차
Groceries=식료품 Postal=우편 Transit=운송 Distillery=양조장 Heralds=헤럴드 신문 Dancer=댄서 Rancher=목장주
Plumber=배관공 Courier=택배 Catering=케이터링 Drinker=술꾼 Adventurer=모험가 Eggs=달걀 Exterminator=해충 방제
Mason=석공 Plonkies=플롱키스 Airport=공항 Van=밴 Genuine=지뉴인 Locksmith=열쇠공 Florist=꽃집 Painter=페인트공
Taxi=택시 McCoy=맥코이 Mechanic=정비공 NNN=NNN 방송 Front=앞 Rear=뒤 Glass=유리 Cache=은닉처 Camo=위장복 Tarmac=활주로 Ground=다진 고기
"""

PLACE_WORD = {}
_last = None
for _w in PLACE_WORDS.split():
    if "=" in _w:
        _last, _v = _w.split("=", 1)
        PLACE_WORD[_last] = _v
    elif _last:  # 뜻에 띄어쓰기가 있으면 앞 낱말 뜻에 이어 붙인다 (예: Ranger=산림 경비대)
        PLACE_WORD[_last] += " " + _w
# 앞에 오면 맨 뒤로 보내는 낱말 (CrateLumber → 목재 상자, BinFireStation → 소방서 쓰레기통)
PLACE_HEAD_TO_END = {"Crate", "Crates", "Bin", "Locker", "Lockers", "Fridge", "Freezer", "Wardrobe", "Closet", "Dresser"}
PLACE_SUFFIX = {"Early": "(초반)", "Mid": "(중반)", "Late": "(후반)"}
# 맨 끝에 오면 괄호로 빼는 꾸밈말 (BedroomDresserClassy → 침실 서랍장 (고급))
PLACE_QUALIFIER = {
    "Classy": "고급", "Generic": "일반", "Rich": "부유층", "Poor": "가난한 집", "Fancy": "고급", "Random": "잡동사니",
    "Redneck": "시골", "Child": "아이", "Childs": "아이", "Kids": "아이", "Bad": "불량", "Special": "특별",
}

# Distributions 의 방 이름 (방에 바로 아이템이 적힌 곳만)
ROOM_NAMES = {
    "all": "", "BombCache1": "폭발물 은닉처", "BoozeCache1": "술 은닉처", "Carpenter": "목수의 집",
    "Chef": "요리사의 집", "Farmer": "농부의 집", "FoodCache1": "음식 은닉처", "GunCache1": "총기 은닉처",
    "GunCache2": "총기 은닉처", "MedicalCache1": "의료품 은닉처", "Nurse": "간호사의 집",
    "ShotgunCache1": "산탄총 은닉처", "ShotgunCache2": "산탄총 은닉처", "SurvivorCache1": "생존자 은닉처",
    "SurvivorCache2": "생존자 은닉처", "SurvivorCacheBigBuilding": "큰 건물 생존자 은닉처", "ToolsCache1": "공구 은닉처",
    "beergarden": "비어가든", "derelict": "폐가", "drugshack": "마약 판잣집", "grocery": "식료품점",
    "grocerystorage": "식료품점 창고", "motelroom": "모텔 방", "motelroomoccupied": "투숙 중인 모텔 방",
    "pizzakitchen": "피자집 부엌", "pizzawhirled": "피자 월드",
}
# 용기 이름 (IGUI_ContainerTitle_* 에 없는 것)
CONTAINER_NAMES = {
    "inventorymale": "좀비 시체 (남자)", "inventoryfemale": "좀비 시체 (여자)", "cardboardbox": "종이 상자",
    "dishescabinet": "그릇장", "dumpster": "대형 쓰레기통", "militarycrate": "군용 상자", "militarylocker": "군용 사물함",
    "plankstash": "마룻바닥 은닉처", "restaurantdisplay": "식당 진열장", "shelter": "대피소", "tent": "텐트",
    "toolcabinet": "공구함", "trough": "여물통", "composter": "퇴비통", "coffin": "관", "doghouse": "개집",
    "brazier": "화로", "newspaper_dispatch": "신문 가판대", "newspaper_herald": "신문 가판대",
    "newspaper_knews": "신문 가판대", "newspaper_times": "신문 가판대", "other": "기타 용기", "logs": "통나무 더미",
    "clothingdryerbasic": "의류 건조기", "dishwasher": "식기세척기", "barbecuepropane": "프로판 바비큐",
    "body": "주인 시체", "BombBox": "폭발물 상자", "BoozeBox": "술 상자", "ToolsBox": "공구 상자",
    "Bag_DuffelBagTINT": "더플백",
}

# 제외 기준
DEBUG_NAME = re.compile(r"debug|^test|dev_item|dummy", re.I)
HIDDEN_CATEGORIES = {"Hidden", "ZedDmg", "Wound", "MaleBody"}

# ─────────────────────────────────────────────────────────────
# 스크립트 해석
# ─────────────────────────────────────────────────────────────


def new_node(kind, name):
    return {"kind": kind, "name": name, "props": {}, "pairs": [], "lines": [], "children": []}


def add_statement(node, body):
    body = body.strip().rstrip(",").strip()
    if not body:
        return
    if "=" in body and not re.match(r"^(item|fluid|energy|-fluid|\+fluid)\s", body):
        key, value = body.split("=", 1)
        key, value = key.strip(), value.strip().rstrip(",").strip()
        node["props"][key] = value
        node["pairs"].append((key, value))
    else:
        node["lines"].append(body)


def parse_script(text):
    """좀보이드 스크립트(.txt)를 블록 트리로 바꾼다. 블록 = {kind, name, props, pairs, lines, children}."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    root = new_node("root", "")
    stack = [root]
    header = None  # 블록 이름일 수도 있는 앞줄 (다음 줄이 { 이면 블록)

    def flush_header():
        nonlocal header
        if header is not None:
            add_statement(stack[-1], header)
            header = None

    for raw in text.splitlines():
        line = raw.split("//", 1)[0].strip()
        while line:
            if line[0] == "{":
                kind, _, name = (header or "").partition(" ")
                node = new_node(kind.strip(), name.strip())
                stack[-1]["children"].append(node)
                stack.append(node)
                header = None
                line = line[1:].strip()
                continue
            if line[0] == "}":
                flush_header()
                if len(stack) > 1:
                    stack.pop()
                line = line[1:].lstrip(",").strip()
                continue
            cut = min([i for i in (line.find("{"), line.find("}")) if i >= 0], default=len(line))
            body, line = line[:cut].strip(), line[cut:]
            flush_header()
            if line.startswith("{") or (not body.endswith(",") and "=" not in body and len(body.split()) <= 2):
                header = body  # 다음에 { 가 오면 블록 이름이 된다
            else:
                add_statement(stack[-1], body)
    flush_header()
    return root


def split_list(value, sep=";"):
    return [v.strip() for v in (value or "").split(sep) if v.strip()]


def full_id(name):
    name = name.strip()
    return name if "." in name else f"Base.{name}"


def num(value):
    """스크립트 숫자 → int/float. 숫자가 아니면 None."""
    if value is None:
        return None
    try:
        f = float(str(value).strip().rstrip("fF"))
    except ValueError:
        return None
    if f != f:  # NaN
        return None
    return int(f) if f.is_integer() else round(f, 4)


def truthy(value):
    return str(value or "").strip().lower() == "true"


# ─────────────────────────────────────────────────────────────
# Lua 분포 표 해석 (표 생성자만 읽는 작은 해석기)
# ─────────────────────────────────────────────────────────────

LUA_TOKEN = re.compile(
    r"""
    (?P<ws>\s+)
  | (?P<lcomment>--\[(?P<eq>=*)\[.*?\](?P=eq)\])
  | (?P<comment>--[^\n]*)
  | (?P<lstr>\[(?P<eq2>=*)\[.*?\](?P=eq2)\])
  | (?P<str>"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')
  | (?P<num>\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\.\d+)
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
  | (?P<op>==|~=|<=|>=|\.\.\.|\.\.|[{}\[\]=,;()<>+\-*/#:.%^])
""",
    re.S | re.X,
)


class LuaRef(str):
    """다른 표를 가리키는 이름 (예: ClutterTables.BinJunk)"""


def lua_tokens(text):
    out = []
    pos = 0
    while pos < len(text):
        m = LUA_TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"Lua 토큰 해석 실패: {text[pos:pos + 40]!r}")
        pos = m.end()
        if m.group("ws") is not None or m.group("comment") is not None or m.group("lcomment") is not None:
            continue
        if m.group("str") is not None:
            v = m.group("str")[1:-1]
            if "\\" in v:
                v = re.sub(r"\\(.)", lambda x: {"n": "\n", "t": "\t"}.get(x.group(1), x.group(1)), v)
            out.append(("str", v))
        elif m.group("lstr") is not None:
            out.append(("str", re.sub(r"^\[=*\[|\]=*\]$", "", m.group("lstr"))))
        elif m.group("num") is not None:
            out.append(("num", float(m.group("num"))))
        elif m.group("name") is not None:
            out.append(("name", m.group("name")))
        else:
            out.append(("op", m.group("op")))
    out.append(("eof", None))
    return out


def lua_value(toks, i):
    kind, v = toks[i]
    if (kind, v) == ("op", "-") and toks[i + 1][0] == "num":
        return -toks[i + 1][1], i + 2
    if (kind, v) == ("op", "{"):
        return lua_table(toks, i)
    if kind in ("str", "num"):
        return v, i + 1
    if kind == "name":
        if v in ("true", "false"):
            return v == "true", i + 1
        if v == "nil":
            return None, i + 1
        if v == "function":
            raise ValueError("함수 값은 읽지 않는다")
        if toks[i + 1] == ("name", "or"):  # `A or {}` 는 앞 이름만 본다
            _, j = lua_value(toks, i + 2)
            return LuaRef(v), j
        if toks[i + 1][0] == "op" and toks[i + 1][1] in ("(", "["):
            raise ValueError("함수 호출·색인은 읽지 않는다")
        return LuaRef(v), i + 1
    raise ValueError(f"Lua 값 해석 실패: {toks[i:i + 4]}")


def lua_table(toks, i):
    i += 1
    arr, d = [], {}
    while toks[i] != ("op", "}"):
        kind, v = toks[i]
        if kind == "name" and toks[i + 1] == ("op", "="):
            d[v], i = lua_value(toks, i + 2)
        elif (kind, v) == ("op", "["):
            key, i = lua_value(toks, i + 1)
            if toks[i] != ("op", "]") or toks[i + 1] != ("op", "="):
                raise ValueError("[키] = 값 형식이 아니다")
            d[key], i = lua_value(toks, i + 2)
        else:
            val, i = lua_value(toks, i)
            arr.append(val)
        if toks[i] in (("op", ","), ("op", ";")):
            i += 1
        elif toks[i] != ("op", "}"):
            raise ValueError(f"표 구분자가 없다: {toks[i:i + 4]}")
    i += 1
    if arr and d:
        d["__array"] = arr
        return d, i
    return (arr if arr else d), i


def lua_assignments(text):
    """최상위 `이름 = 값` 대입문을 {이름: 값} 으로 모은다. 함수·반복문 안은 건너뛴다."""
    toks = lua_tokens(text)
    env = {}
    depth = 0
    i = 0
    while i < len(toks) - 1:
        kind, v = toks[i]
        if kind == "name" and v in ("function", "if", "for", "while", "repeat"):
            depth += 1
        elif kind == "name" and v in ("end", "until"):
            depth -= 1
        elif depth == 0 and kind == "name" and toks[i + 1] == ("op", "=") and toks[i - 1] != ("op", ","):
            try:
                val, j = lua_value(toks, i + 2)
            except (ValueError, IndexError):
                i += 1
                continue
            env[v] = val
            i = j
            continue
        i += 1
    return env


def lua_all_tables(text):
    """파일 안의 모든 표 생성자를 (가능한 것만) 읽는다. 채집 정의처럼 함수 안에 있는 표를 찾을 때 쓴다."""
    toks = lua_tokens(text)
    for i, tok in enumerate(toks):
        if tok == ("op", "{"):
            try:
                val, _ = lua_table(toks, i)
            except (ValueError, IndexError):
                continue
            yield val


# ─────────────────────────────────────────────────────────────
# 텍스처 묶음 (.pack) 과 아이콘
# ─────────────────────────────────────────────────────────────


def read_pack(path):
    """텍스처 묶음에서 {이름: (페이지 PNG 바이트, x, y, w, h, ox, oy, fw, fh)} 를 만든다.

    새 형식은 PZPK 헤더 뒤에 PNG 길이가 있고, 옛 형식은 페이지 수로 시작하며 PNG 뒤에 DEADBEEF 가 붙는다.
    x, y, w, h 는 페이지 안 잘린 그림 자리, ox, oy 는 원래 그림 안에서의 위치, fw, fh 는 원래 크기다.
    """
    data = path.read_bytes()
    view = memoryview(data)  # 큰 타일 묶음도 PNG 를 복사하지 않고 가리키기만 한다
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
            rect = struct.unpack_from("<8i", data, pos)
            pos += 32
            page_entries.append((name, rect))
        if new:
            (size,) = struct.unpack_from("<i", data, pos)
            png = view[pos + 4 : pos + 4 + size]
            pos += 4 + size
        else:
            end = data.index(b"IEND", pos) + 8
            png = view[pos:end]
            pos = end
            if data[pos : pos + 4] == b"\xef\xbe\xad\xde":
                pos += 4
        if png[:4] != b"\x89PNG":
            raise SystemExit(f"페이지 PNG 를 찾지 못했습니다. 묶음 형식이 바뀌었을 수 있습니다: {path}")
        for name, rect in page_entries:
            entries.setdefault(name, (png, *rect))
    return entries


class IconSource:
    """Item_<아이콘> 그림을 묶음과 낱개 PNG 에서 찾는다. 앞에 둔 묶음이 우선이다."""

    PACKS = ["UI2.pack", "UI.pack", "ApComUI.pack", "RadioIcons.pack", "IconsMoveables.pack"]

    def __init__(self, media):
        self.entries = {}
        for name in self.PACKS:
            path = media / "texturepacks" / name
            if path.exists():
                for key, val in read_pack(path).items():
                    self.entries.setdefault(key, val)
        self.loose = {}
        for png in sorted(media.rglob("Item_*.png")):
            self.loose.setdefault(png.stem, png)
        self.lower = {}
        for key in list(self.entries) + list(self.loose):
            self.lower.setdefault(key.lower(), key)
        self.pages = {}
        self.media = media
        self.tiles = None

    def find_tile(self, sprite):
        """아이콘이 default 인 Moveable 은 게임도 바닥 타일 그림을 줄여 보여 준다. 그 타일을 찾는다."""
        if self.tiles is None:
            self.tiles = {}
            for name in ("Tiles1x.pack", "Tiles2x.pack"):
                path = self.media / "texturepacks" / name
                if path.exists():
                    for key, val in read_pack(path).items():
                        self.tiles.setdefault(key, val)
        return f"tile:{sprite}" if sprite in self.tiles else None

    def find(self, names):
        for name in names:
            for key in (name, self.lower.get(name.lower())):
                if key and (key in self.entries or key in self.loose):
                    return key
        return None

    def image(self, key):
        if key.startswith("tile:"):
            png, x, y, w, h, *_ = self.tiles[key[5:]]
            if id(png) not in self.pages:
                self.pages[id(png)] = Image.open(io.BytesIO(png)).convert("RGBA")
            crop = self.pages[id(png)].crop((x, y, x + w, y + h))
            crop = crop.crop(crop.getbbox() or (0, 0, w, h))
            crop.thumbnail((32, 32), Image.LANCZOS)
            canvas = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
            canvas.paste(crop, ((32 - crop.width) // 2, (32 - crop.height) // 2))
            return canvas
        if key in self.entries:
            png, x, y, w, h, ox, oy, fw, fh = self.entries[key]
            if id(png) not in self.pages:
                self.pages[id(png)] = Image.open(io.BytesIO(png)).convert("RGBA")
            crop = self.pages[id(png)].crop((x, y, x + w, y + h))
            # 묶음은 투명한 테두리를 잘라 두므로 원래 크기(대개 32×32) 판에 제자리로 붙인다
            canvas = Image.new("RGBA", (max(fw, ox + w), max(fh, oy + h)), (0, 0, 0, 0))
            canvas.paste(crop, (ox, oy))
            return canvas
        return Image.open(self.loose[key]).convert("RGBA")


def webp_bytes(img):
    # 도트 아이콘이라 손실 압축을 쓰면 테두리가 번진다. 무손실로 저장해도 PNG 보다 작다.
    buf = io.BytesIO()
    img.save(buf, "WEBP", lossless=True, method=6)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────
# 이름 붙이기
# ─────────────────────────────────────────────────────────────


def camel_tokens(name):
    out = []
    for part in re.split(r"[_\s]+", name):
        out += re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+|[A-Z]+", part)
    return out


def compose_words(toks):
    """낱말 목록 → 한국어 낱말 목록. 모르는 낱말이 있으면 None."""
    if not toks:
        return None
    toks = list(toks)
    head_to_end = toks.pop(0) if len(toks) > 1 and toks[0] in PLACE_HEAD_TO_END else None
    words = []
    i = 0
    while i < len(toks):
        for size in (4, 3, 2):
            phrase = " ".join(toks[i : i + size])
            if len(toks) - i >= size and phrase in PLACE_PHRASES:
                words.append(PLACE_PHRASES[phrase])
                i += size
                break
        else:
            if toks[i] not in PLACE_WORD:
                return None
            words.append(PLACE_WORD[toks[i]])
            i += 1
    if head_to_end:
        words.append(PLACE_WORD[head_to_end])
    # 같은 낱말이 잇달아 나오면 하나로 (예: 상자 상자 → 상자)
    return [w for k, w in enumerate(words) if k == 0 or w != words[k - 1]]


def compose_place(name):
    """CamelCase 목록 이름을 낱말 표로 한국어로 옮긴다. 모르는 낱말이 있으면 None.

    UniversityDesk_Occult → 대학 책상 (오컬트), BedroomDresserClassy → 침실 서랍장 (고급),
    MeleeWeapons_Late → 근접 무기 보관함 (후반) 처럼 꾸밈말은 괄호로 뒤에 붙인다.
    """
    if name in PLACE_FULL:
        return PLACE_FULL[name]
    parts = [x for x in name.split("_") if x]
    if not parts:
        return None
    toks = camel_tokens(parts[0])
    suffix, extras = [], []
    while len(toks) > 1 and (toks[-1] in PLACE_SUFFIX or toks[-1].isdigit()):
        t = toks.pop()
        suffix.insert(0, PLACE_SUFFIX.get(t, t))
    if len(toks) > 1 and toks[-1] in PLACE_QUALIFIER:
        extras.append(PLACE_QUALIFIER[toks.pop()])
    words = compose_words(toks)
    if words is None:
        return None
    for part in parts[1:]:
        if part in PLACE_SUFFIX or part.isdigit():
            suffix.append(PLACE_SUFFIX.get(part, part))
            continue
        sub = camel_tokens(part)
        tail = []
        while len(sub) > 1 and sub[-1].isdigit():
            tail.insert(0, sub.pop())
        w = compose_words(sub)
        if w is None:
            return None
        extras.append(" ".join(w + tail))
    text = " ".join(words)
    if extras:
        text += " (" + ", ".join(extras) + ")"
    return " ".join([text] + suffix).strip() or None


# ─────────────────────────────────────────────────────────────
# 본체
# ─────────────────────────────────────────────────────────────


class Extractor:
    def __init__(self, game):
        self.game = game
        self.media = game / "media"
        self.tr_dir = self.media / "lua/shared/Translate"
        self.ko = {}
        self.en = {}
        for lang, store in (("KO", self.ko), ("EN", self.en)):
            for f in sorted((self.tr_dir / lang).glob("*.json")):
                try:
                    store[f.stem] = json.loads(f.read_text(encoding="utf-8-sig"))
                except json.JSONDecodeError:
                    store[f.stem] = {}
        self.ui_ko = {**self.ko.get("UI", {}), **self.ko.get("IG_UI", {})}
        self.ui_en = {**self.en.get("UI", {}), **self.en.get("IG_UI", {})}
        self.skills = {}
        self.excluded = defaultdict(list)
        self.notes = []
        self._place_cache = {}

    # ── 번역 ──
    def t(self, table, key):
        """KO 번역 → EN 번역 → 없으면 빈 문자열."""
        return (self.ko.get(table, {}).get(key) or self.en.get(table, {}).get(key) or "").strip()

    def ui(self, key):
        return (self.ui_ko.get(key) or self.ui_en.get(key) or "").strip()

    def skill_id(self, raw):
        return SKILL_ALIAS.get(raw, raw)

    def skill_name(self, raw):
        sid = self.skill_id(raw)
        if sid not in self.skills:
            key = PERK_KEY.get(sid, sid)
            self.skills[sid] = (self.ui_ko.get(f"IGUI_perks_{key}") or "").strip() or PERK_FALLBACK.get(sid) or (
                self.ui_en.get(f"IGUI_perks_{key}") or sid
            ).strip()
        return self.skills[sid]

    def skill_levels(self, value):
        out = []
        for part in split_list(value):
            if ":" in part:
                sid, level = part.split(":", 1)
                out.append({"skill": self.skill_id(sid.strip()), "name": self.skill_name(sid.strip()), "level": num(level)})
        return out

    def category_name(self, key):
        return self.ui(f"IGUI_ItemCat_{key}") or key

    def recipe_category(self, key):
        if not key:
            return ""
        for k in (f"IGUI_CraftingCategories_{key}", f"IGUI_CraftCategory_{key}"):
            if (self.ui_ko.get(k) or "").strip():
                return self.ui_ko[k].strip()
        return CATEGORY_FALLBACK.get(key) or self.ui(f"IGUI_CraftingCategories_{key}") or key

    def tooltip(self, key):
        text = self.t("Tooltip", key) if key else ""
        text = re.sub(r"<br>|<BR>|<LINE>", " ", text)
        text = re.sub(r"<[^>]*>", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def fluid_name(self, fid):
        return self.t("Fluids", f"Fluid_Name_{fid}") or fid

    # ── 1. 스크립트 읽기 ──
    def load_scripts(self):
        self.item_nodes = {}  # id → (블록, 파일)
        self.recipe_nodes = []  # (이름, 블록, 파일)
        self.entities = []  # (이름, 블록)
        self.skins = {}  # xuiSkin entity 이름 → DisplayName
        for f in sorted((self.media / "scripts").rglob("*.txt")):
            rel = f.relative_to(self.media / "scripts").as_posix()
            if rel.startswith(("generated/sounds/", "generated/vehicles/", "generated/models", "generated/animations")):
                continue
            root = parse_script(f.read_text(encoding="utf-8", errors="replace"))
            for mod in root["children"]:
                if mod["kind"] != "module":
                    continue
                module = mod["name"] or "Base"
                for node in mod["children"]:
                    if node["kind"] == "item":
                        self.item_nodes.setdefault(f"{module}.{node['name']}", (node, rel))
                    elif node["kind"] == "craftRecipe":
                        self.recipe_nodes.append((node["name"], node, rel))
                    elif node["kind"] == "entity":
                        self.entities.append((node["name"], node))
                    elif node["kind"] == "xuiSkin":
                        for sub in node["children"]:
                            if sub["kind"] == "entity":
                                self.skins.setdefault(sub["name"], sub["props"].get("DisplayName", ""))

    # ── 2. 아이템 고르기 ──
    def select_items(self):
        names_ko = self.ko.get("ItemName", {})
        names_en = self.en.get("ItemName", {})
        self.items = {}
        for fid in sorted(self.item_nodes):
            node, rel = self.item_nodes[fid]
            p = node["props"]
            itype = p.get("ItemType", "").replace("base:", "")
            name_en = (names_en.get(fid) or "").strip()
            reason = None
            name_ko = (names_ko.get(fid) or "").strip()
            if itype == "moveable" and (
                p.get("DisplayCategory") == "Furniture"
                or node["name"].startswith("Mov_")
                or not re.search("[가-힣]", name_ko)
            ):
                # 가구·화분처럼 바닥에 놓인 타일을 집어 든 것. 생가죽·광석·텐트·침낭처럼
                # 들고 다니며 쓰는 Moveable 은 남긴다(제작 재료라 빠지면 제작법이 끊긴다).
                reason = "moveable"
            elif truthy(p.get("hidden")):
                reason = "hidden"
            elif p.get("DisplayCategory") in HIDDEN_CATEGORIES:
                reason = "hiddenCategory"
            elif (
                "TEMPORARY_TESTING" in rel
                or DEBUG_NAME.search(node["name"])
                or re.search(r"placeholder|not spawn|debug", name_en, re.I)
            ):
                reason = "debug"
            elif itype == "animal":
                reason = "internal"
            elif not (names_ko.get(fid) or name_en):
                reason = "noName"
            if reason:
                self.excluded[reason].append(fid)
                continue
            self.items[fid] = node

    # ── 3. 제작법 ──
    def parse_io_line(self, line, mappers):
        """제작법 inputs/outputs 한 줄을 읽는다."""
        m = re.match(r"(item|-fluid|\+fluid|fluid|energy)\s+(\S+)\s*(.*)$", line)
        if not m:
            return None
        kind, count, rest = m.groups()
        out = {}
        vm = re.match(r"variable\[(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)\]", count)
        if vm:
            out["n"], out["max"] = num(vm.group(1)), num(vm.group(2))
        else:
            out["n"] = num(count)
        groups = dict()
        for prefix, body in re.findall(r"(\w*)\[([^\]]*)\]", rest):
            groups.setdefault(prefix, body)
        mode = re.search(r"mode:(\w+)", rest)
        if kind == "item":
            if "" in groups:
                # "2:Base.BurlapPiece" 는 그 아이템 하나를 2개로 쳐 준다는 뜻이다. 아이템 id 만 남긴다.
                ids = [full_id(re.sub(r"^\d+:", "", x)) for x in split_list(groups[""]) if x != "*"]
                if ids:
                    out["items"] = ids
                elif "*" in groups[""]:
                    out["any"] = True
            if "tags" in groups:
                out["tags"] = [t.lower() for t in split_list(groups["tags"])]
            mapper = re.search(r"mapper:(\w+)", rest)
            if mapper and mapper.group(1) in mappers:
                out["items"] = mappers[mapper.group(1)]
            elif not out.get("items") and not out.get("tags"):
                # outputs: "item 3 Base.Plank"
                plain = re.findall(r"(?<![\w\[:.])((?:\w+\.)?[A-Za-z_][\w]*)(?![\w\]:])", re.sub(r"\w*\[[^\]]*\]|mode:\w+|mapper:\w+", "", rest))
                plain = [x for x in plain if x not in ("overlayMapper",)]
                if plain:
                    out["items"] = [full_id(plain[0])]
            if mode and mode.group(1) == "keep":
                out["keep"] = True
        else:
            if "" in groups:
                out["fluids"] = [{"id": f, "name": self.fluid_name(f)} for f in split_list(groups[""])]
            if "categories" in groups:
                out["fluidCategories"] = split_list(groups["categories"])
            if kind == "energy":
                out["energy"] = True
        return out

    def read_mappers(self, node):
        mappers = {}
        for child in node["children"]:
            if child["kind"] == "itemMapper":
                outs = []
                for key, value in child["pairs"]:
                    target = value if key == "default" else key
                    for x in split_list(target):
                        fid = full_id(x)
                        if fid not in outs:
                            outs.append(fid)
                mappers[child["name"]] = outs
        return mappers

    def recipe_from_node(self, node, kind):
        p = node["props"]
        mappers = self.read_mappers(node)
        inputs, outputs = [], []
        for child in node["children"]:
            if child["kind"] in ("inputs", "outputs"):
                for line in child["lines"]:
                    parsed = self.parse_io_line(line, mappers)
                    if parsed:
                        (inputs if child["kind"] == "inputs" else outputs).append(parsed)
        for o in outputs:
            o.pop("keep", None)
        tags = split_list(p.get("Tags"))
        rec = {
            "name": "",
            "nameEn": "",
            "kind": kind,
            "category": p.get("category", ""),
            "categoryName": self.recipe_category(p.get("category", "")),
            "time": num(p.get("time")),
            "skills": self.skill_levels(p.get("SkillRequired")),
            "xp": [{"skill": s["skill"], "name": s["name"], "amount": s["level"]} for s in self.skill_levels(p.get("xpAward"))],
            "stations": [{"tag": t, "name": STATIONS[t]} for t in tags if t in STATIONS],
            "needsLearning": truthy(p.get("NeedToBeLearn")),
            "autoLearn": self.skill_levels(p.get("AutoLearnAll")) + self.skill_levels(p.get("AutoLearnAny")),
            "inputs": inputs,
            "outputs": outputs,
        }
        if p.get("Tooltip"):
            desc = self.tooltip(p.get("Tooltip"))
            if desc:
                rec["desc"] = desc
        if p.get("OnCreate"):
            rec["scripted"] = True  # 결과 일부를 Lua 코드가 만든다 (여기 outputs 에 다 안 나올 수 있다)
        return rec

    def build_recipes(self):
        self.recipes = {}
        self.meta_recipes = defaultdict(list)  # MetaRecipe(묶음 이름) → 그 묶음에 든 제작법
        for rid, node, rel in self.recipe_nodes:
            if rid in self.recipes:
                continue
            if node["props"].get("MetaRecipe"):
                self.meta_recipes[node["props"]["MetaRecipe"].lower()].append(rid)
            rec = self.recipe_from_node(node, "craft")
            rec["name"] = self.t("Recipes", rid) or rid
            rec["nameEn"] = self.en.get("Recipes", {}).get(rid) or rid
            self.recipes[rid] = rec
        for ename, node in self.entities:
            comp = next((c for c in node["children"] if c["kind"] == "component" and c["name"] == "CraftRecipe"), None)
            if not comp or comp["props"].get("category") == "Debug":
                continue
            style = next(
                (c["props"].get("entityStyle") for c in node["children"] if c["kind"] == "component" and c["name"] == "UiConfig"),
                None,
            )
            display_en = self.skins.get(style or "", "") or self.en.get("Recipes", {}).get(ename) or ename
            rid = ename if ename not in self.recipes else f"build:{ename}"
            rec = self.recipe_from_node(comp, "build")
            base = re.sub(r"_?Lvl(\d)$", "", ename)
            rec["name"] = (self.ko.get("Recipes", {}).get(ename) or "").strip() or BUILD_NAMES.get(base) or BUILD_NAMES.get(ename) or display_en
            rec["nameEn"] = display_en
            tier = re.search(r"Lvl(\d)$", ename)
            if tier:
                rec["tier"] = int(tier.group(1))
            self.recipes[rid] = rec

    # ── 4. 연결 ──
    def link(self):
        self.tag_items = defaultdict(list)
        for fid, node in self.items.items():
            for tag in split_list(node["props"].get("Tags")):
                self.tag_items[tag.lower()].append(fid)
        self.links = defaultdict(lambda: defaultdict(set))
        for rid, rec in self.recipes.items():
            for inp in rec["inputs"]:
                for fid in self.resolve(inp):
                    self.links[fid]["tool" if inp.get("keep") else "uses"].add(rid)
            for out in rec["outputs"]:
                for fid in out.get("items", []):
                    if fid in self.items:
                        self.links[fid]["made"].add(rid)
        # 책이 가르쳐 주는 제작법, 연구로 배우는 제작법.
        # 이름이 제작법 id 이거나, 여러 제작법을 묶은 MetaRecipe 이름(base:makemagazinearmor 등)이다.
        # 둘 다 아니면 제작법이 아닌 '지식'(씨앗 봉투의 재배 정보, 차량 정비 기초 등)이다.
        lower_ids = {rid.lower(): rid for rid in self.recipes}
        self.knowledge = defaultdict(list)
        unknown = set()
        for fid, node in self.items.items():
            for key, link in (("LearnedRecipes", "teaches"), ("Researchablerecipes", "research")):
                for name in split_list(node["props"].get(key)):
                    rid = name if name in self.recipes else lower_ids.get(name.lower())
                    rids = [rid] if rid else self.meta_recipes.get(name.lower(), [])
                    for r in rids:
                        self.links[fid][link].add(r)
                        self.recipes[r].setdefault("taughtBy" if link == "teaches" else "researchFrom", []).append(fid)
                    if not rids and link == "teaches":
                        label = self.t("Recipes", name)
                        if label and label not in self.knowledge[fid]:
                            self.knowledge[fid].append(label)
                        elif not label:
                            unknown.add(name)
                    elif not rids:
                        unknown.add(name)
        if unknown:
            self.notes.append(f"책·연구 항목에 적혔지만 제작법도 번역도 없는 이름 {len(unknown)}개: {sorted(unknown)[:8]}")
        for rec in self.recipes.values():
            for key in ("taughtBy", "researchFrom"):
                if key in rec:
                    rec[key] = sorted(set(rec[key]))

    def resolve(self, inp):
        """제작법 재료 한 칸에 들어갈 수 있는 (도감에 있는) 아이템들."""
        found = [fid for fid in inp.get("items", []) if fid in self.items]
        for tag in inp.get("tags", []):
            found += self.tag_items.get(tag, [])
        return sorted(set(found))

    # ── 5. 나오는 곳 ──
    def load_loot(self):
        server = self.media / "lua/server"
        files = sorted((server / "Items").glob("Distribution_*.lua"))
        files += [server / "Items/ProceduralDistributions.lua", server / "Items/Distributions.lua"]
        files += sorted((server / "Vehicles").glob("VehicleDistribution*.lua"))
        env, per_file = {}, {}
        for f in files:
            if not f.exists():
                continue
            e = lua_assignments(f.read_text(encoding="utf-8", errors="replace"))
            per_file[f.name] = e
            env.update({k: v for k, v in e.items() if k != "distributionTable"})

        def deref(v):
            for _ in range(10):
                if not isinstance(v, LuaRef):
                    return v
                v = env.get(str(v))
            return v

        def no_chance(items, rolls, junk):
            """한 번 채울 때 이 목록에서 아이템별로 하나도 안 나올 확률."""
            miss = defaultdict(lambda: 1.0)
            items = deref(items)
            if not isinstance(items, list):
                return {}
            for k in range(0, len(items) - 1, 2):
                name, weight = items[k], items[k + 1]
                if not isinstance(name, str) or not isinstance(weight, float):
                    continue
                if junk:
                    p = weight * 1.4 * 100 * 1.0 / 10000
                else:
                    p = weight * 100 * LOOT_MODIFIER / 10000
                miss[full_id(name)] *= 1 - min(1.0, p)
            rolls = max(1, int(rolls or 1))
            return {k: v**rolls for k, v in miss.items()}

        self.loot = defaultdict(list)  # 아이템 → [(확률, 곳)]

        def add_source(key, table):
            table = deref(table)
            if not isinstance(table, dict):
                return
            miss = defaultdict(lambda: 1.0)
            for fid, v in no_chance(table.get("items"), table.get("rolls"), False).items():
                miss[fid] *= v
            junk = deref(table.get("junk"))
            if isinstance(junk, dict):
                for fid, v in no_chance(junk.get("items"), junk.get("rolls"), True).items():
                    miss[fid] *= v
            for fid, v in miss.items():
                if v < 1.0:
                    self.loot[fid].append((1.0 - v, key))

        self.loot_keys = {}
        self.list_rooms = defaultdict(set)  # 분포 목록 → 그 목록을 쓰는 방 종류
        proc = deref(env.get("ProceduralDistributions.list")) or {}
        for name, table in proc.items():
            add_source(name, table)
            self.loot_keys[name] = ("proc", name)
        dist = per_file.get("Distributions.lua", {}).get("distributionTable", {})
        for room, val in dist.items():
            val = deref(val)
            if not isinstance(val, dict):
                continue
            if "items" in val or "rolls" in val:  # 가방 안에 든 것
                key = f"bag:{room}"
                add_source(key, val)
                self.loot_keys[key] = ("bag", room)
                continue
            for cont, c in val.items():
                c = deref(c)
                if not isinstance(c, dict):
                    continue
                for pl in deref(c.get("procList")) or []:
                    if isinstance(pl, dict) and isinstance(pl.get("name"), str):
                        self.list_rooms[pl["name"]].add(room)
                if c.get("items") is not None:
                    key = f"room:{room}.{cont}"
                    add_source(key, c)
                    self.loot_keys[key] = ("room", (room, cont))
        for name, val in env.items():
            if name.startswith("VehicleDistributions.") and isinstance(deref(val), dict) and "items" in deref(val):
                short = name.split(".", 1)[1]
                key = f"car:{short}"
                add_source(key, val)
                self.loot_keys[key] = ("car", short)
        self.notes.append(f"분포 목록 {len(proc)}개, 방·용기 {sum(1 for k in self.loot_keys if k.startswith('room:'))}개, "
                          f"가방 {sum(1 for k in self.loot_keys if k.startswith('bag:'))}개, 차량 {sum(1 for k in self.loot_keys if k.startswith('car:'))}개를 읽음")

    def loot_score(self, chance, key):
        return chance * (1 + math.log(1 + len(self.list_rooms.get(key, ()))))

    def place_label(self, key):
        """화면에 보일 곳 이름. 한국어로 못 옮기면 원래 이름."""
        if key not in self._place_cache:
            self._place_cache[key] = self.place_name(key) or key.split(":", 1)[-1]
        return self._place_cache[key]

    def place_name(self, key):
        kind, val = self.loot_keys.get(key, ("proc", key))
        if kind == "proc":
            return compose_place(val)
        if kind == "bag":
            bag = self.t("ItemName", full_id(val))
            return f"{bag} 안" if bag else None
        if kind == "car":
            name = compose_place(val)
            return f"차량 · {name}" if name else None
        room, cont = val
        if cont.startswith("Outfit_"):
            outfit = compose_place(cont[len("Outfit_"):])
            return f"좀비 시체 · {outfit} 복장" if outfit else None
        cname = CONTAINER_NAMES.get(cont) or self.ui(f"IGUI_ContainerTitle_{cont}")
        rname = ROOM_NAMES.get(room)
        if not cname or rname is None:
            return None
        return f"{rname} {cname}".strip()

    def load_forage(self):
        self.forage = {}
        folder = self.media / "lua/shared/Foraging/Categories"
        for f in sorted(folder.glob("*.lua")) if folder.exists() else []:
            for table in lua_all_tables(f.read_text(encoding="utf-8", errors="replace")):
                if not isinstance(table, dict):
                    continue
                itype, zones = table.get("type"), table.get("zones")
                if not isinstance(itype, str) or not isinstance(zones, dict) or not itype.startswith("Base."):
                    continue
                cur = self.forage.setdefault(itype, {"skill": None, "zones": {}})
                skill = table.get("skill")
                if isinstance(skill, float):
                    cur["skill"] = int(skill) if cur["skill"] is None else min(cur["skill"], int(skill))
                for z, w in zones.items():
                    if isinstance(w, float) and w > 0:
                        cur["zones"][z] = max(cur["zones"].get(z, 0), w)

    def zone_name(self, z):
        return (self.ui_ko.get(f"IGUI_SearchMode_Zone_Names_{z}") or "").strip() or FORAGE_ZONE_FALLBACK.get(z) or (
            self.ui_en.get(f"IGUI_SearchMode_Zone_Names_{z}") or z
        )

    # ── 6. 아이템 한 개 ──
    def item_name(self, fid):
        return self.t("ItemName", fid) or fid.split(".", 1)[1]

    def ref(self, fid):
        return {"id": fid, "name": self.item_name(fid)}

    def item_record(self, fid, node, icon):
        p = node["props"]
        itype = p.get("ItemType", "").replace("base:", "")
        cat = p.get("DisplayCategory", "")
        tags = [t.lower() for t in split_list(p.get("Tags"))]
        rec = {
            "id": fid,
            "name": self.item_name(fid),
            "nameEn": (self.en.get("ItemName", {}).get(fid) or "").strip() or fid.split(".", 1)[1],
            "category": {"key": cat, "name": self.category_name(cat)},
            "type": itype,
            "typeName": TYPE_NAMES.get(itype) or self.category_name(TYPE_CATEGORY.get(itype, itype)),
            "weight": num(p.get("Weight", "1")),
            "icon": icon,
            "tags": tags,
            "roles": [{"tag": t, "name": TAG_NAMES[t]} for t in sorted(
                (t for t in tags if t in TAG_NAMES), key=lambda t: (t in MINOR_TAGS, tags.index(t))
            )],
        }
        tip = self.tooltip(p.get("Tooltip"))
        if tip:
            rec["tooltip"] = tip
        if itype == "weapon":
            rec["weapon"] = self.weapon_info(p)
        if itype == "food":
            rec["food"] = self.food_info(p)
        if itype in ("clothing", "alarmclockclothing") or p.get("BodyLocation"):
            wear = self.wear_info(p)
            if wear:
                rec["wear"] = wear
        if itype == "container" or p.get("Capacity"):
            bag = self.bag_info(p)
            if bag:
                rec["bag"] = bag
        if itype == "literature":
            book = self.book_info(p)
            if book:
                rec["book"] = book
        extra = self.misc_info(p, node)
        rec.update(extra)
        return rec

    def weapon_info(self, p):
        cats = [c.replace("base:", "") for c in split_list(p.get("Categories"))]
        firearm = p.get("SubCategory") == "Firearm" or truthy(p.get("IsAimedFirearm"))
        skill = "Aiming" if firearm else next((WEAPON_SKILL[c] for c in cats if c in WEAPON_SKILL), None)
        w = {
            "skill": skill,
            "skillName": self.skill_name(skill) if skill else "맨손·기타",
            "improvised": "improvised" in cats,
            "firearm": firearm,
            "minDamage": num(p.get("MinDamage")),
            "maxDamage": num(p.get("MaxDamage")),
            "minRange": num(p.get("MinRange")),
            "maxRange": num(p.get("MaxRange")),
            "baseSpeed": num(p.get("BaseSpeed", "1")),
            "swingTime": num(p.get("MinimumSwingtime")),
            "critChance": num(p.get("CriticalChance")),
            "critMultiplier": num(p.get("CritDmgMultiplier")),
            "maxHit": num(p.get("MaxHitcount")),
            "condition": num(p.get("ConditionMax")),
            "conditionLowerOneIn": num(p.get("ConditionLowerChanceOneIn")),
            "twoHanded": truthy(p.get("TwoHandWeapon")) or truthy(p.get("RequiresEquippedBothHands")),
            "doorDamage": num(p.get("DoorDamage")),
            "treeDamage": num(p.get("TreeDamage")),
            "knockdown": num(p.get("KnockdownMod")),
            "sharpness": num(p.get("Sharpness")),
            "headCondition": num(p.get("HeadCondition")),
        }
        if firearm:
            ammo = AMMO_ITEM.get(p.get("AmmoType", ""))
            w.update({
                "ammo": self.ref(ammo) if ammo else None,
                "magazine": self.ref(full_id(p["MagazineType"])) if p.get("MagazineType") else None,
                "capacity": num(p.get("MaxAmmo") or p.get("ClipSize")),
                "hitChance": num(p.get("HitChance")),
                "aimingTime": num(p.get("Aimingtime")),
                "reloadTime": num(p.get("Reloadtime")),
                "recoilDelay": num(p.get("RecoilDelay")),
                "soundRadius": num(p.get("SoundRadius")),
                "projectiles": num(p.get("Projectilecount")),
                "jamChance": num(p.get("JamGunChance")),
            })
        return {k: v for k, v in w.items() if v is not None and v is not False}

    def food_info(self, p):
        evolved = []
        for part in split_list(p.get("EvolvedRecipe")):
            name = part.split(":", 1)[0].strip()
            label = self.t("Recipes", name) or EVOLVED_FALLBACK.get(name) or name
            if label not in evolved:
                evolved.append(label)
        f = {
            "hunger": num(p.get("HungerChange")),
            "thirst": num(p.get("ThirstChange")),
            "unhappy": num(p.get("UnhappyChange")),
            "boredom": num(p.get("BoredomChange")),
            "stress": num(p.get("StressChange")),
            "fatigue": num(p.get("fatigueChange")),
            "endurance": num(p.get("enduranceChange")),
            "calories": num(p.get("Calories")),
            "carbs": num(p.get("Carbohydrates")),
            "fat": num(p.get("Lipids")),
            "protein": num(p.get("Proteins")),
            "daysFresh": num(p.get("DaysFresh")),
            "daysRotten": num(p.get("DaysTotallyRotten")),
            "cookable": truthy(p.get("IsCookable")),
            "minutesToCook": num(p.get("MinutesToCook")),
            "minutesToBurn": num(p.get("MinutesToBurn")),
            "dangerousRaw": truthy(p.get("DangerousUncooked")),
            "mustOpen": truthy(p.get("CantEat")),
            "openWith": self.recipes[p["OpeningRecipe"]]["name"] if p.get("OpeningRecipe") in getattr(self, "recipes", {}) else None,
            "canned": truthy(p.get("CannedFood")),
            "packaged": truthy(p.get("Packaged")),
            "spice": truthy(p.get("Spice")),
            "foodType": p.get("FoodType"),
            "alcoholic": truthy(p.get("Alcoholic")),
            "poison": num(p.get("PoisonPower")),
            "sickness": num(p.get("FoodSicknessChange")),
            "goodHot": truthy(p.get("GoodHot")),
            "badCold": truthy(p.get("BadCold")),
            "cantBeFrozen": truthy(p.get("CantBeFrozen")),
            "evolved": evolved or None,
            "replaceOnUse": self.ref(full_id(p["ReplaceOnUse"])) if p.get("ReplaceOnUse") else None,
        }
        return {k: v for k, v in f.items() if v not in (None, False, "")}

    def location_name(self, loc):
        loc = loc.replace("base:", "")
        base = re.sub(r"_?texture$", "", loc)
        return BODY_LOCATIONS.get(loc) or BODY_LOCATIONS.get(base) or loc

    def wear_info(self, p):
        loc = p.get("BodyLocation", "")
        w = {
            "slot": loc.replace("base:", "") or None,
            "slotName": self.location_name(loc) if loc else None,
            "bite": num(p.get("BiteDefense")),
            "scratch": num(p.get("ScratchDefense")),
            "bullet": num(p.get("BulletDefense")),
            "insulation": num(p.get("Insulation")),
            "wind": num(p.get("WindResistance")),
            "water": num(p.get("WaterResistance")),
            "runSpeed": num(p.get("RunSpeedModifier")),
            "combatSpeed": num(p.get("CombatSpeedModifier")),
            "discomfort": num(p.get("DiscomfortModifier")),
            "condition": num(p.get("ConditionMax")),
            "fabric": p.get("FabricType"),
            "canHaveHoles": None if p.get("CanHaveHoles") is None else truthy(p.get("CanHaveHoles")),
        }
        # 모자 뒤로 쓰기·두건 묶기처럼 바꿔 입으면 되는 다른 모양 (ClothingItemExtra)
        variants = [full_id(x) for x in split_list(p.get("ClothingItemExtra"))]
        if variants:
            w["variants"] = [self.ref(v) for v in variants if v in self.items]
        return {k: v for k, v in w.items() if v not in (None, [])}

    def bag_info(self, p):
        b = {
            "capacity": num(p.get("Capacity")),
            "weightReduction": num(p.get("WeightReduction")),
            "slot": p.get("CanBeEquipped", "").replace("base:", "") or None,
            "runSpeed": num(p.get("RunSpeedModifier")),
            "maxItemSize": num(p.get("MaxItemSize")),
        }
        if b["slot"]:
            b["slotName"] = self.location_name(b["slot"])
        b = {k: v for k, v in b.items() if v is not None}
        return b if "capacity" in b else None

    def book_info(self, p):
        b = {}
        if p.get("SkillTrained"):
            lo = num(p.get("LvlSkillTrained")) or 1
            n = num(p.get("NumLevelsTrained")) or 1
            b.update({
                "skill": self.skill_id(p["SkillTrained"]),
                "skillName": self.skill_name(p["SkillTrained"]),
                "levels": [lo, lo + n - 1],
            })
        for key, field in (("NumberOfPages", "pages"), ("BoredomChange", "boredom"), ("UnhappyChange", "unhappy"),
                           ("StressChange", "stress")):
            if num(p.get(key)) is not None:
                b[field] = num(p.get(key))
        return b or None

    def misc_info(self, p, node):
        out = {}
        if p.get("UseDelta") and num(p.get("UseDelta")):
            out["uses"] = max(1, round(1 / num(p["UseDelta"])))
        if p.get("LightDistance") or p.get("LightStrength"):
            out["light"] = {k: v for k, v in {
                "distance": num(p.get("LightDistance")),
                "strength": num(p.get("LightStrength")),
                "cone": truthy(p.get("TorchCone")) or None,
            }.items() if v is not None}
        med = {k: v for k, v in {
            "bandage": num(p.get("BandagePower")) if truthy(p.get("CanBandage")) else None,
            "disinfect": num(p.get("AlcoholPower")),
            "infection": num(p.get("ReduceInfectionPower")),
            "pain": num(p.get("painReduction")),
            "flu": num(p.get("fluReduction")),
        }.items() if v is not None}
        if med:
            out["medical"] = med
        for child in node["children"]:
            if child["kind"] == "component" and child["name"] == "FluidContainer":
                contents = []
                for sub in child["children"]:
                    if sub["kind"] == "Fluids":
                        for line in sub["lines"] + [f"{k} = {v}" for k, v in sub["pairs"]]:
                            m = re.match(r"fluid\s*=\s*(\w+)", line)
                            if m and m.group(1) not in [c["id"] for c in contents]:
                                contents.append({"id": m.group(1), "name": self.fluid_name(m.group(1))})
                fluid = {"capacity": num(child["props"].get("Capacity"))}
                if contents:
                    fluid["contents"] = contents
                if truthy(child["props"].get("PickRandomFluid")):
                    fluid["randomContent"] = True
                out["fluid"] = fluid
        if p.get("ReplaceOnUse") and p.get("ItemType") != "base:food":
            out["becomes"] = self.ref(full_id(p["ReplaceOnUse"]))
        if num(p.get("TransmitRange")):
            out["radio"] = {"range": num(p.get("TransmitRange")), "twoWay": truthy(p.get("TwoWay"))}
        return out

    def summary(self, rec):
        """검색 목록에 한 줄로 보일 짧은 요약."""
        parts = []
        main_roles = [r["name"] for r in rec["roles"] if r["tag"] not in MINOR_TAGS]
        w = rec.get("weapon")
        # 펜·숟가락처럼 무기로도 쥘 수 있을 뿐인 물건은 무기 수치보다 쓰임새를 먼저 보인다
        weak_weapon = w and not w.get("firearm") and (not w.get("skill") or (w.get("maxDamage") or 0) < 0.3)
        if w and not weak_weapon:
            if w.get("firearm"):
                parts.append("총")
                if w.get("ammo"):
                    parts.append(w["ammo"]["name"])
                if w.get("capacity"):
                    parts.append(f"장탄 {w['capacity']}")
            else:
                parts.append(f"{w['skillName']} 무기")
                if w.get("maxDamage") is not None:
                    lo, hi = w.get("minDamage", 0), w["maxDamage"]
                    parts.append(f"피해 {hi}" if lo == hi else f"피해 {lo}–{hi}")
                if w.get("twoHanded"):
                    parts.append("양손")
        elif "food" in rec:
            f = rec["food"]
            if f.get("hunger"):
                parts.append(f"배고픔 {f['hunger']:+g}")
            if f.get("thirst"):
                parts.append(f"갈증 {f['thirst']:+g}")
            if f.get("calories"):
                parts.append(f"{f['calories']:g}kcal")
            if f.get("mustOpen"):
                parts.append("따서 먹음")
            elif f.get("dangerousRaw"):
                parts.append("익혀 먹어야 함")
            if f.get("daysFresh"):
                parts.append(f"{f['daysFresh']}일 신선")
        elif "bag" in rec and rec["bag"].get("capacity"):
            b = rec["bag"]
            parts.append(f"용량 {b['capacity']}")
            if b.get("weightReduction"):
                parts.append(f"무게 {b['weightReduction']}% 줄임")
            if b.get("slotName"):
                parts.append(b["slotName"])
        elif "wear" in rec:
            wr = rec["wear"]
            if wr.get("slotName"):
                parts.append(wr["slotName"])
            if wr.get("bite") or wr.get("scratch"):
                parts.append(f"물림 {wr.get('bite', 0):g} · 긁힘 {wr.get('scratch', 0):g}")
            elif wr.get("insulation"):
                parts.append(f"보온 {wr['insulation']:g}")
        elif "book" in rec:
            b = rec["book"]
            if b.get("skill"):
                parts.append(f"{b['skillName']} {b['levels'][0]}–{b['levels'][1]}레벨 책")
            else:
                for key, label in (("boredom", "지루함"), ("unhappy", "불행"), ("stress", "스트레스")):
                    if b.get(key):
                        parts.append(f"{label} {b[key]:+g}")
        elif "medical" in rec:
            m = rec["medical"]
            labels = {"bandage": "상처에 감음", "disinfect": "소독", "infection": "감염 억제", "pain": "통증 완화", "flu": "감기 완화"}
            parts.append(", ".join(labels[k] for k in m))
            if m.get("bandage"):
                parts.append(f"효과 {m['bandage']:g}")
        elif main_roles and not rec.get("fluid", {}).get("contents"):
            parts.append(", ".join(main_roles[:3]))
        elif rec.get("radio"):
            parts.append(f"무전 범위 {rec['radio']['range']}")
        elif rec.get("fluid"):
            fl = rec["fluid"]
            what = fl["contents"][0]["name"] if fl.get("contents") and not fl.get("randomContent") else "액체"
            parts.append(f"{what} {fl.get('capacity', '')}L 담는 용기".replace(" L", "L"))
        elif rec.get("light"):
            parts.append(f"빛 범위 {rec['light'].get('distance', '?')}")
        teaches = rec.get("recipes", {}).get("teaches")
        if teaches:
            parts.append(f"제작법 {len(teaches)}개를 배움")
        knows = rec.get("knowledge")
        if knows and not teaches:
            parts.append(f"읽으면 알게 됨: {knows[0]}" + (f" 외 {len(knows) - 1}가지" if len(knows) > 1 else ""))
        if not parts and main_roles:
            parts.append(", ".join(main_roles[:3]))
        if not parts and rec.get("tooltip"):
            parts.append(rec["tooltip"][:40])
        if not parts:
            used = len(set(rec.get("recipes", {}).get("uses", [])) | set(rec.get("recipes", {}).get("tool", [])))
            if used:
                parts.append(f"{rec['category']['name']} · 제작법 {used}개에 쓰임")
            elif rec["roles"]:
                parts.append(", ".join(r["name"] for r in rec["roles"][:3]))
            else:
                parts.append(rec["category"]["name"])
        return " · ".join(str(x) for x in parts)

    # ── 7. 전체 ──
    def run(self):
        print("스크립트 읽는 중...")
        self.load_scripts()
        self.select_items()
        self.build_recipes()
        self.link()
        print("분포 표 읽는 중...")
        self.load_loot()
        self.load_forage()
        print("아이콘 찾는 중...")
        icons = IconSource(self.media)

        icon_files = {}  # 아이콘 이름 → 파일 이름
        used_lower = {}
        records = []
        missing_icon = []
        for fid, node in self.items.items():
            p = node["props"]
            icon_name = (p.get("Icon") or (split_list(p.get("IconsForTexture")) or [""])[0]).strip()
            candidates = []
            if icon_name and icon_name.lower() != "default":
                candidates += [f"Item_{icon_name}", icon_name]
            candidates.append(f"Item_{node['name']}")
            key = icons.find(candidates)
            if not key and p.get("WorldObjectSprite"):
                key = icons.find_tile(p["WorldObjectSprite"].strip())
            icon_url = None
            if key:
                stem = key[5:] if key.startswith(("Item_", "tile:")) else key
                stem = re.sub(r"[^A-Za-z0-9_.-]", "_", stem)
                if key not in icon_files:
                    # 대소문자만 다른 이름은 Windows 에서 같은 파일이 되므로 뒤에 번호를 붙인다
                    fname = stem
                    k = 2
                    while fname.lower() in used_lower and used_lower[fname.lower()] != key:
                        fname = f"{stem}_{k}"
                        k += 1
                    used_lower[fname.lower()] = key
                    icon_files[key] = fname
                icon_url = f"{ICON_URL}/{icon_files[key]}.webp"
            else:
                missing_icon.append(fid)
            records.append(self.item_record(fid, node, icon_url))

        # 제작법 목록 붙이기
        for rec in records:
            links = self.links.get(rec["id"], {})
            r = {k: sorted(links[k]) for k in ("made", "uses", "tool", "teaches", "research") if links.get(k)}
            if r:
                rec["recipes"] = r
            if self.knowledge.get(rec["id"]):
                rec["knowledge"] = self.knowledge[rec["id"]]
            src = self.loot.get(rec["id"], [])
            if src:
                # 확률이 높고, 그 목록을 쓰는 방 종류가 많은(=흔히 보이는) 곳을 먼저 둔다.
                # 이름이 같은 곳(예: 구급상자 두 종류)은 한 번만 남긴다.
                ranked = sorted(src, key=lambda x: (-self.loot_score(*x), x[1]))
                picked, seen = [], set()
                for c, key in ranked:
                    label = self.place_label(key)
                    if label in seen:
                        continue
                    seen.add(label)
                    picked.append([key, round(c * 100, 1) if c >= 0.001 else max(0.01, round(c * 100, 2))])
                    if len(picked) == LOOT_TOP:
                        break
                rec["loot"] = picked
                rec["lootCount"] = len(src)
            fg = self.forage.get(rec["id"])
            if fg and fg["zones"]:
                zones = sorted(fg["zones"].items(), key=lambda x: (-x[1], x[0]))
                rec["forage"] = {
                    "skill": fg["skill"] or 0,
                    "zones": [{"zone": z, "name": self.zone_name(z), "weight": num(w)} for z, w in zones],
                }
            rec["summary"] = self.summary(rec)

        records.sort(key=lambda r: (r["category"]["key"], r["name"], r["id"]))

        # 아이콘 파일
        OUT_ICONS.mkdir(parents=True, exist_ok=True)
        written = set()
        for key, fname in sorted(icon_files.items(), key=lambda x: x[1]):
            dest = OUT_ICONS / f"{fname}.webp"
            data = webp_bytes(icons.image(key))
            if not dest.exists() or dest.read_bytes() != data:
                dest.write_bytes(data)
            written.add(dest.name)
        for old in OUT_ICONS.glob("*.webp"):
            if old.name not in written:
                old.unlink()

        return records, missing_icon, icon_files

    def write(self, records):
        version = ""
        vfile = Path.home() / "Zomboid/version.txt"
        if vfile.exists():
            version = vfile.read_text(encoding="utf-8").split()[0]

        used_recipes = sorted({rid for r in records for ids in r.get("recipes", {}).values() for rid in ids})
        recipes = {rid: self.recipes[rid] for rid in sorted(self.recipes)}
        used_tags = sorted({t for rec in recipes.values() for inp in rec["inputs"] for t in inp.get("tags", [])})
        kept = {r["id"] for r in records}
        tag_items = {t: sorted(fid for fid in self.tag_items.get(t, []) if fid in kept) for t in used_tags}
        place_keys = sorted({src[0] for r in records for src in r.get("loot", [])})
        places = {key: self.place_label(key) for key in place_keys}
        translated = sum(1 for key in place_keys if self.place_name(key))
        categories = {}
        for r in records:
            categories[r["category"]["key"]] = r["category"]["name"]

        meta = {
            "build": version,
            "lootNote": (
                f"나오는 곳의 숫자는 그 목록으로 채워진 용기 하나를 열었을 때 1개 이상 나올 대략의 확률(%)이다. "
                f"샌드박스 루트 설정 기본값({LOOT_MODIFIER}) 기준이며, 좀비 밀도 보정과 시간에 따른 감소는 넣지 않았다. "
                f"순서는 확률에 (1 + ln(1 + 그 목록을 쓰는 방 종류 수))를 곱한 값이 큰 것부터라서, 흔히 보이는 곳이 앞에 온다."
            ),
        }
        index = {
            **meta,
            "categories": dict(sorted(categories.items())),
            "items": [
                {
                    "id": r["id"], "name": r["name"], "nameEn": r["nameEn"], "category": r["category"]["key"],
                    "icon": r["icon"], "weight": r["weight"], "summary": r["summary"],
                }
                for r in records
            ],
        }
        detail = {
            **meta,
            "skills": dict(sorted(self.skills.items())),
            "tagNames": dict(sorted(TAG_NAMES.items())),
            "tagItems": tag_items,
            "places": places,
            "recipes": recipes,
            "items": {r["id"]: {k: v for k, v in r.items() if k not in ("summary",)} for r in records},
        }
        OUT_DATA.mkdir(parents=True, exist_ok=True)
        sizes = {}
        for name, obj in (("items-index.json", index), ("items-detail.json", detail)):
            data = (json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
            (OUT_DATA / name).write_bytes(data)
            sizes[name] = (len(data), len(gzip.compress(data, 9, mtime=0)))
        return sizes, translated, len(place_keys), len(used_recipes)


def main():
    game = Path(sys.argv[1] if len(sys.argv) > 1 else "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid")
    if not (game / "media/scripts").exists():
        raise SystemExit(f"게임 폴더가 아닙니다: {game}")
    ex = Extractor(game)
    records, missing_icon, icon_files = ex.run()
    sizes, translated, place_total, used_recipes = ex.write(records)

    by_cat = defaultdict(int)
    for r in records:
        by_cat[f"{r['category']['name']} ({r['category']['key']})"] += 1
    total_icon = sum(f.stat().st_size for f in OUT_ICONS.glob("*.webp"))
    print(f"아이템 {len(records)}개 (스크립트 {len(ex.item_nodes)}개 중)")
    for reason, ids in sorted(ex.excluded.items()):
        print(f"  뺀 것 {reason}: {len(ids)}개")
    print(f"제작법 {len(ex.recipes)}개 (아이템과 이어진 것 {used_recipes}개)")
    print(f"아이콘 {len(icon_files)}개, {total_icon / 1024:.0f}KB, 아이콘 없는 아이템 {len(missing_icon)}개: {missing_icon[:20]}")
    print(f"나오는 곳 이름 {place_total}개 중 한국어로 옮긴 것 {translated}개")
    for name, (raw, gz) in sizes.items():
        print(f"{name}: {raw / 1024:.0f}KB (gzip {gz / 1024:.0f}KB)")
    for note in ex.notes:
        print("참고:", note)
    print("분류별:")
    for k, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {k}: {n}")


if __name__ == "__main__":
    main()
