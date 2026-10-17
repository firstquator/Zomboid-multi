// 플레이 팁 페이지의 생활 꿀팁.
//
// 근거: docs/research/tips.md (42.21 게임 파일 + B42 버전이 적힌 웹 자료). 메뉴·상태 이름은 바닐라 KO 표기다.
// 우리 서버는 Hx 통합 번역을 쓰므로 실제 화면 문구는 조금 다를 수 있다.
// 그림 경로는 web/public/guide 아래(scripts/extract-guide-assets.py).

// 단축키 섹션 아래에 붙이는 "알아 두면 좋은 조작"
export const controlTips = [
  { keys: ["M"], text: "짧게 누르면 세계 지도, 0.5초 넘게 누르면 원형 메뉴가 떠서 미니맵을 켜고 끈다. 불빛이 없으면 밤에는 지도를 못 읽는다" },
  { keys: ["E"], text: "창문 앞에서 길게 누르면 넘는다. 깨진 창문은 우클릭 → 「부서진 유리 치우기」를 먼저 한다" },
  { keys: ["1", "8"], range: true, text: "무기나 손전등을 우클릭 → 「부착하기」로 벨트·등에 걸어 두면 숫자 키로 바로 꺼낸다" },
  { keys: ["Shift"], text: "그냥 걸으면 가장 조용하다. 전력질주(Alt) 발소리는 걷기의 두 배, 웅크려 걸으면 절반이다" },
];

export const tipTopics = [
  {
    id: "combat",
    label: "전투",
    spiffo: "spiffo_combat",
    lede: "한 마리씩, 문간에서, 지치기 전에 물러나는 게 기본이다.",
    tips: [
      {
        title: "한 마리는 밀치고 밟는다",
        keys: ["Space"],
        icons: ["item/BaseballBat"],
        text: "혼자 오는 좀비는 Space 로 밀쳐 넘어뜨리고 머리 쪽에서 밟는다. 무기가 닳지 않는다. 근처에 다른 좀비가 있으면 밟는 사이 물리니 한 마리일 때만.",
      },
      {
        title: "「지침」이 뜨면 물러난다",
        icons: ["moodle/Status_DifficultyBreathing", "moodle/Status_HeavyLoad"],
        text: "휘두를 때마다 지구력이 준다. 오른쪽에 「지침」 무들이 뜨면 공격이 확 약해지니 뒤로 빠져 앉아서 쉰다. 짐이 무거우면 회복이 느리다.",
      },
      {
        title: "무기는 닳는다",
        keys: ["R"],
        icons: ["item/Whetstone2", "item/DuctTape", "item/Glue"],
        text: "무기는 맞힐 때마다 상하고 0이 되면 부서진다. 여분을 하나 더 차고, 제작창에서 테이프·접착제로 고친다. 날 무기는 숫돌을 갖고 무기를 든 채 R 로 간다.",
      },
      {
        title: "여러 마리는 줄 세운다",
        icons: ["vehicle/vehicle_exit"],
        text: "여러 방향에서 잡히면 끌려 넘어져 바로 죽을 수 있다. 문간·울타리처럼 한 줄로만 오는 곳으로 끌고 가서 하나씩 친다. 등 뒤가 가장 위험하다.",
      },
      {
        title: "문은 닫고, 창문 앞엔 서 있지 않는다",
        keys: ["E"],
        text: "좀비는 문을 못 연다(두드려 부순다). 들어간 건물의 문은 닫는다. 창문을 막 넘은 좀비는 몸을 날려 넘어뜨리니 한 발 떨어져서 친다.",
      },
      {
        title: "소리가 좀비를 부른다",
        keys: ["Q"],
        icons: ["item/Hammer"],
        text: "망치질은 20칸, 총은 60~200칸까지 들린다. Q 를 짧게 누르면 외친다. 6~9일째 낮에 헬기가 지나가며 좀비를 끌고 다니니 그날은 실내에 있는다.",
      },
    ],
  },
  {
    id: "loot",
    label: "루팅·이동",
    spiffo: "spiffo_inventory",
    lede: "B42는 실내가 어둡다. 손전등과 가방이 먼저다.",
    tips: [
      {
        title: "손전등은 허리에",
        keys: ["F"],
        icons: ["item/Flashlight2", "item/Battery"],
        text: "B42는 불 꺼진 집과 밤이 훨씬 어둡다. 손전등을 단축 칸에 걸어 두고 F 로 켠다. 상식적인 상호작용 모드로 허리띠에도 단다. 건전지 여분을 챙긴다.",
        mod: "상식적인 상호작용",
      },
      {
        title: "집 하나 터는 순서",
        icons: ["item/Map"],
        text: "빠져나갈 길을 두 개 정하고, 문을 열면 한 걸음 물러나 안을 본다. 들어가면 문을 닫고 방을 하나씩 확인한다. 누워 있는 좀비 중엔 죽은 척하는 것도 있다.",
      },
      {
        title: "주변 상자는 한 번에",
        icons: ["sidebar/Inventory_On_64"],
        text: "루팅 창 오른쪽의 「주변」 버튼을 누르면 근처 상자·시체·바닥 물건이 한 목록에 모인다. 이 버튼을 Shift+클릭하면 늘 이 목록으로 열린다.",
        mod: "주변 상자 한 번에 보기",
      },
      {
        title: "초반에 빨리 턴다",
        text: "날이 갈수록 이미 털린 건물이 늘어나 90일째엔 최대 25%가 된다. 털린 집은 문이나 창이 부서져 있다. 가까운 집부터 빨리 턴다.",
      },
      {
        title: "가방은 여러 개 멘다",
        icons: ["item/BigHiking_Blue", "item/AliceBag", "item/FannyPack"],
        text: "B42는 등 가방, 어깨 가방, 허리 가방 앞·뒤를 한꺼번에 멘다. 가방 안 물건은 무게가 준다(군용 배낭 85%). 손에 든 가방은 공격을 느리게 하니 쫓기면 버린다.",
      },
      {
        title: "읽을 책만 챙긴다",
        icons: ["item/Magazine"],
        text: "책·잡지 아이콘의 「?」는 안 읽은 것, 「!」는 읽다 만 것이다. 우리 서버는 기술 서적을 거의 바로 읽으니 그 자리에서 읽는다.",
        mod: "읽은 책 표시",
      },
    ],
  },
  {
    id: "health",
    label: "건강",
    spiffo: "spiffo_food",
    lede: "다치면 H. 괄호 안에 할 일이 적혀 있다.",
    tips: [
      {
        title: "치료법은 괄호 안에",
        keys: ["H"],
        icons: ["item/Bandage", "item/Alcohol", "item/SutureNeedle", "item/Tweezers", "item/Splint"],
        text: "상태창에서 다친 부위 옆 괄호를 본다. 「긁힌 상처 [소독, 붕대]」, 「깊은 상처 [봉합]」, 「뼈가 부러짐 [소독, 부목]」. 유리·총알이 박히면 핀셋으로 먼저 뺀다.",
      },
      {
        title: "붕대는 갈고 빨아 쓴다",
        icons: ["item/BandageDirty", "item/Rag", "item/Antibiotics"],
        text: "「붕대가 오염됨」이 뜨면 새 붕대로 간다. 그대로 두면 상처가 「세균 감염 됨」(좀비 감염과 다름)이 된다. 더러운 붕대는 「붕대 씻기」 후 소독해서 다시 쓴다.",
      },
      {
        title: "좀비 감염인지 구별하기",
        icons: ["moodle/Mood_Nauseous", "moodle/Mood_Ill", "moodle/Mood_NoxiousSmell"],
        text: "물리면 100%, 찢어지면 25%, 긁히면 7% 확률로 감염되고 치료법은 없다. 감기는 콧물 무들, 식중독은 상한 음식 뒤, 시체 냄새는 자리를 뜨면 낫는다.",
      },
      {
        title: "음식 상태를 본다",
        icons: ["item/Beans", "item/CanOpener"],
        text: "음식은 신선한 → 신선하지 않은 → 상한 순서로 변한다. 냉장고는 5배 느리게 상하게 한다. 통조림은 따기 전엔 안 상하니 오래 둘 식량으로 남긴다.",
      },
      {
        title: "단수 뒤 물은 끓인다",
        icons: ["item/Pot", "item/WaterPurificationTablets", "item/WaterBottle"],
        text: "단수는 0~30일 사이에 예고 없이 온다. 그 뒤 강·빗물은 「오염된 물」이라 끓이거나 정수 알약(1알에 1L)을 쓴다. 조금만 섞여도 통 전체가 오염된다.",
      },
      {
        title: "지루함은 미리 푼다",
        icons: ["moodle/Mood_Bored", "item/ComicBook"],
        text: "같은 일만 하면 지루함이 쌓이고 우울해져 행동이 느려진다. 책·만화·잡지를 읽고, TV를 보고, 같이 하는 사람과 이야기한다.",
      },
    ],
  },
  {
    id: "base",
    label: "기지",
    spiffo: "spiffo_crafting",
    lede: "드나드는 곳이 적고 넓은 창고가 있는 곳이 좋다.",
    tips: [
      {
        title: "바리케이드는 안에서",
        icons: ["item/Hammer", "item/Plank", "item/Nails"],
        text: "망치와 판자를 들고 창문을 우클릭 → 「바리케이드 설치 (판자)」. 판자 1장에 못 2개, 한 면에 4장까지. 서 있는 쪽 면에 붙으니 안에서 친다.",
      },
      {
        title: "계단을 부수고 밧줄로",
        icons: ["item/Sledgehamer", "item/SheetRope", "item/Sheet"],
        text: "2층을 기지로 쓰면 대형 망치로 계단을 「철거하기」하고, 창문에 「천 밧줄 설치」로 오르내린다. 좀비는 밧줄을 못 탄다. 밧줄을 먼저 걸고 시험한 뒤 계단을 부순다.",
      },
      {
        title: "빗물받이로 물 걱정 덜기",
        icons: ["item/Garbagebag", "item/TentMaterial", "item/Plank"],
        text: "목공 3이면 빗물받이 상자(400L), 목공 5면 통(600L)을 건축 창 「실외」에서 짓는다. 지붕 없는 곳에 두고, 받은 물은 끓여 마신다.",
      },
      {
        title: "발전기는 실내 금지",
        icons: ["item/Generator", "item/MagazineElectronics02"],
        text: "건물 안에서 돌리면 유독 가스가 차서 죽을 수 있다. 바깥에 두면 20칸, 위아래 3층까지 전기가 간다. 연결하려면 「잡지: 발전기 사용법」이나 전기공학 3이 필요하다.",
      },
      {
        title: "시체는 치운다",
        icons: ["moodle/Mood_NoxiousSmell", "item/Rock"],
        text: "기지 근처에 시체가 쌓이면 냄새로 병이 난다. 「시체 들기」로 멀리 옮기거나 돌 3개로 지은 모닥불에 태운다.",
      },
      {
        title: "상자에 이름 붙이기",
        icons: ["sidebar/Inventory_On_64"],
        text: "기지 상자는 누구나 연다. 상자 버튼을 우클릭 → 「이름 바꾸기」로 음식·의료·공구라고 붙이고, 모드의 「수정」으로 아이콘과 색까지 바꾸면 서로 찾기 쉽다.",
        mod: "보관함 이름표",
      },
    ],
  },
  {
    id: "new",
    label: "B42 새 기능",
    spiffo: "spiffo_foraging",
    lede: "제작, 채집, 동물, 석기. 처음 하는 사람이 알면 좋은 것만.",
    tips: [
      {
        title: "제작은 B, 건축은 왼쪽 망치 버튼",
        keys: ["B"],
        icons: ["sidebar/Carpentry_On_64", "sidebar/Build_On_64"],
        text: "B 로 제작창을 열면 분류별 제작법과 재료가 보인다. 벽·가구·빗물받이 같은 건축물은 화면 왼쪽 아이콘 줄의 건축 버튼으로 연다.",
      },
      {
        title: "제작법은 배워야 한다",
        icons: ["item/MagazineElectronics02", "item/Magazine"],
        text: "제작법 약 970개 중 380개쯤은 배워야 쓴다. 잡지를 읽거나, 기술 레벨이 오르거나, 물건을 우클릭 → 「제작법 연구하기」로 배운다. 잡지는 사람마다 따로 읽는다.",
      },
      {
        title: "TV·비디오는 3레벨까지",
        icons: ["item/Cassette3"],
        text: "TV 교양 프로그램과 비디오테이프로 기술을 올릴 수 있지만 3레벨이 되면 멈춘다. 초반에 조금 올리는 용도다.",
      },
      {
        title: "채집은 End 키",
        keys: ["End"],
        icons: ["sidebar/Search_On_64", "item/Twigs", "item/BerryBlack"],
        text: "End 로 탐색 모드를 켜면 걷는 동안 먹을거리·나뭇가지·돌이 보인다. 어두우면 거의 못 찾으니 손전등을 든다. 버섯은 생김새로 독을 못 가린다.",
      },
      {
        title: "동물은 닭부터",
        keys: ["V"],
        icons: ["item/Egg", "sidebar/AnimalZone_On_64"],
        text: "가축은 목장·농장에서 나온다. 동물 옆에서 V 를 누르면 동물 메뉴가 뜬다. 닭은 들어서 가방에 넣을 수 있고 암탉은 하루 한 알을 낳는다.",
      },
      {
        title: "도구가 없으면 돌로",
        icons: ["item/RockSharpened", "item/AxeStone"],
        text: "부싯돌 덩어리를 돌 망치로 쳐서 「날카로운 부싯돌 조각」을 만들고, 나뭇가지와 묶을 것을 더해 「조잡한 돌 도끼」를 만든다. 물건관리 1이면 된다.",
      },
    ],
  },
  {
    id: "multi",
    label: "같이 할 때",
    spiffo: "spiffo_multiplayer",
    lede: "지도로 서로 찾고, 역할을 나누고, 호스트는 마지막에 나간다.",
    tips: [
      {
        title: "지도에서 친구 찾기",
        keys: ["M"],
        icons: ["item/Map", "item/Pen"],
        text: "우리 서버는 지도와 미니맵에 모든 사람이 보인다. 지도의 「기호」로 기지·위험 지역에 표시하고 「공유하기」를 「전체 공개」로 바꾸면 다 같이 본다. 펜이 필요하다.",
      },
      {
        title: "채팅은 /all 로 전체",
        keys: ["T"],
        text: "그냥 치면 근처 사람에게만 간다. /all 은 모두에게, /w 이름 은 귓속말이다. 한글은 윈도우를 영문으로 둔 채 \\ 로 한/영을 바꾼다.",
        mod: "한글 채팅 입력 개선",
      },
      {
        title: "역할을 나눈다",
        icons: ["item/Hammer", "item/Bandage", "item/Pot"],
        text: "의료·목공·요리·전기·채집처럼 담당을 나누면 빨리 자리 잡는다. 기술 서적은 읽어도 없어지지 않으니 한 권을 돌려 읽는다. 벽은 목공 레벨이 높은 사람이 지어야 튼튼하다.",
      },
      {
        title: "죽으면 내 시체를 찾아간다",
        icons: ["moodle/Mood_Zombified"],
        text: "죽으면 짐은 시체에 남고 자동으로 치워지지 않는다. 감염된 채 죽었다면 곧 좀비로 일어나니 친구와 같이 가서 처리하고 짐을 되찾는다. 사망 알림이 없으니 직접 알린다.",
      },
      {
        title: "스킬 보존 일지 쓰기",
        icons: ["item/Notebook", "item/Glue", "item/LeatherStrips", "item/Thread", "item/Pen"],
        text: "공책 + 접착제 + 가죽 조각 3 + 실로 만들고, 우클릭 → 「저널에 전사」로 기록한다(펜 필요). 가죽 조각은 가죽 장갑·재킷을 「옷 찢기」. 일지는 기지 상자에 둔다.",
        mod: "스킬 보존 일지",
      },
      {
        title: "호스트는 마지막에 나간다",
        keys: ["Esc"],
        text: "아무도 없으면 서버 시간이 멈춘다. 호스트가 나가면 서버가 저장하고 꺼지니, 다른 사람이 다 나간 뒤 안전한 실내에서 Esc → 나가기로 나간다.",
      },
    ],
  },
];
