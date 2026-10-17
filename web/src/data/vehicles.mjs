// 플레이 팁 페이지의 차량 섹션.
//
// 근거: docs/research/vehicles.md (42.21 게임 파일 · 디컴파일한 코드). 메뉴 이름은 KO/ContextMenu.json,
// 계기판 이름은 KO/Tooltip.json 의 Tooltip_Dashboard_* 그대로다.
// 확률은 우리 서버(Apocalypse 프리셋 값) 기준이다.
// 그림 경로는 web/public/guide 아래(scripts/extract-guide-assets.py 가 게임 파일에서 꺼낸다).

// 차 타고 시동 걸기
export const startSteps = [
  {
    icon: "item/CarKey",
    title: "열쇠부터 찾기",
    text: "열쇠는 꽂혀 있거나 글러브박스, 근처 집의 서랍·옷장·조리대, 근처 좀비 몸에서 나온다. 계산대에서도 가끔 나온다.",
    note: "배선을 따기 전에 차 안과 주변부터 뒤진다",
  },
  {
    icon: "vehicle/vehicle_smash_window",
    title: "잠긴 차는 창문으로",
    text: "차 옆에서 V → 「창문 부수기」. 깨진 창문 옆 문은 열쇠 없이 열린다. 맨손이면 유리에 베이니 무기를 들고 깬다.",
    note: "운전석 말고 조수석·뒷자리 창을 깬다. 상식적인 상호작용 모드로 쇠지렛대를 써서 문을 딸 수도 있다",
  },
  {
    icon: "vehicle/ignition_key_on",
    title: "운전석에서 시동",
    keys: ["N"],
    text: "열쇠를 갖고 있거나 꽂혀 있으면 N 으로 시동이 걸린다. 배터리가 10% 아래면 안 걸린다.",
    note: "시동을 끄면 열쇠가 저절로 가방에 들어온다",
  },
  {
    icon: "vehicle/ignition_hotwired",
    title: "열쇠가 없으면 배선 따기",
    keys: ["V"],
    text: "운전석에서 V → 「배선 따기」. 전기공학 1 + 차량정비 2, 또는 좀도둑 직업이어야 한다. 실패해도 다시 하면 된다.",
    note: "성공률은 엔진 상태와 전기공학 레벨로 정해진다. 배선을 딴 차는 누구나 시동을 건다",
  },
];

// 경보: 시작 단계 옆에 경고로 보여 준다
export const alarm = {
  title: "도난 경보 조심",
  text: "잠긴 차 일부(약 8%)에는 경보가 달려 있다. 열쇠 없이 처음 문을 열거나 창문을 깨면 반드시 울린다. 약 50초 동안 150칸 안의 좀비가 몰려오고, 끄는 방법은 없다. 한 번 울린 차는 다시 안 울린다.",
};

// 차량 메뉴(V). 차 안(운전석)과 차 밖에서 뜨는 것이 다르다.
export const radial = {
  inside: [
    { icon: "vehicle/vehicle_ignitionON", label: "시동 걸기 · 끄기" },
    { icon: "vehicle/ignition_hotwired", label: "배선 따기", note: "열쇠가 없을 때" },
    { icon: "vehicle/vehicle_lightsON", label: "전조등" },
    { icon: "vehicle/vehicle_temperatureHOT", label: "히터/에어컨" },
    { icon: "vehicle/vehicle_horn", label: "경적 울리기" },
    { icon: "vehicle/vehicle_lockdoors", label: "모든 문 잠그기" },
    { icon: "vehicle/vehicle_speakersON", label: "장치 조작하기", note: "라디오. 앞좌석만" },
    { icon: "vehicle/vehicle_changeseats", label: "좌석 이동" },
    { icon: "vehicle/vehicle_repair", label: "차량 정비", note: "차를 세워야 열린다" },
    { icon: "vehicle/vehicle_exit", label: "내리기", note: "달리는 차에서는 못 내린다" },
  ],
  outside: [
    { icon: "vehicle/vehicle_repair", label: "차량 정비" },
    { icon: "vehicle/vehicle_refuel_from_pump", label: "주유기로 연료 넣기", note: "주유기 옆, 전기 필요" },
    { icon: "vehicle/vehicle_add_gas", label: "기름 넣기", note: "기름이 든 통" },
    { icon: "vehicle/vehicle_siphon_gas", label: "기름 빼기", note: "고무 호스 필요" },
    { icon: "vehicle/vehicle_smash_window", label: "창문 부수기" },
    { icon: "item/Crowbar", label: "쇠지렛대로 문 따기", note: "상식적인 상호작용 모드", mod: true },
  ],
};

// 계기판 그림(cardashboard, 442×90) 위의 설명 위치. x, y 는 그림 기준 %.
export const dashboardSpots = [
  { x: 20.4, y: 26, label: "엔진 상태", text: "색으로 엔진 상태를 보여 준다. 주황이나 빨강이면 정비가 필요하다" },
  { x: 27.4, y: 26, label: "배터리", text: "배터리가 약하면 색이 바뀐다. 10% 아래면 시동이 안 걸린다" },
  { x: 34.4, y: 25, label: "바깥 기온", text: "지금 바깥 온도" },
  { x: 11.8, y: 56, label: "현재 기어", text: "기어는 자동이다. 기어를 바꾸는 키는 없다" },
  { x: 27.1, y: 80, label: "회전계", text: "엔진 회전수. 높을수록 소리가 멀리 퍼진다" },
  { x: 50, y: 43, label: "연료 게이지", text: "15% 아래로 내려가면 경고가 켜진다. 화살표는 주유구가 있는 쪽" },
  { x: 72, y: 80, label: "속도계", text: "지금 속도(MPH)" },
  { x: 66, y: 26, label: "문 잠금", text: "눌러서 모든 문을 잠그고 푼다" },
  { x: 72, y: 26, label: "전조등", text: "눌러서 켜고 끈다. 키는 F" },
  { x: 77.4, y: 26, label: "히터", text: "눌러서 온도를 맞춘다. 키는 O. 시동이 켜져 있어야 한다" },
  { x: 81.9, y: 26, label: "트렁크", text: "트렁크 잠김·열림 표시" },
  { x: 89, y: 62, label: "열쇠 구멍", text: "눌러서 시동을 건다(N 과 같다). 배선을 땄으면 전선 그림이 보인다" },
];

// 기름
export const fuelWays = [
  {
    icons: ["vehicle/vehicle_refuel_from_pump"],
    title: "주유소에서",
    menu: "주유기로 연료 넣기",
    text: "시동을 끄고 주유구를 주유기 2칸 안에 댄다. 전기가 들어와야 주유기가 돈다.",
  },
  {
    icons: ["item/Petrol", "item/JerrycanMilitary"],
    title: "기름통으로",
    menu: "기름 넣기",
    text: "기름이 든 통을 가방에 넣고 차 옆에서 V. 기름통 10L, 제리캔 20L. 기름이 든 아무 액체 용기나 된다.",
  },
  {
    icons: ["vehicle/vehicle_siphon_gas", "item/RubberHose"],
    title: "다른 차에서 빼기",
    menu: "기름 빼기",
    text: "고무 호스와 빈 통을 갖고 시동이 꺼진 차 옆에서 V. 호스는 가방 속에 있어도 된다.",
  },
];
export const powerCut = {
  icons: ["item/Generator"],
  title: "단전 뒤엔 발전기",
  text: "전기는 게임 시작 14~30일 사이에 끊긴다. 그 뒤로는 주유기 옆에 발전기를 놓고 기름을 채워 연결해야 주유기가 돈다. 발전기 소리에도 좀비가 오니 쓸 때만 켠다.",
};

// 차종 비교. 무게가 1000 에 가까울수록 연비가 좋다(Vehicles.lua). 트렁크·소음은 차 파일 값.
export const carStats = [
  { name: "랭 4000", mass: 950, note: "연비 가장 좋음" },
  { name: "올-터레인", mass: 1000, trunk: 85, loud: 100 },
  { name: "D6 (픽업)", mass: 1030, trunk: 110, loud: 110 },
  { name: "랜처", mass: 900, trunk: 40, loud: 90 },
  { name: "세리스 웨건", mass: 900, trunk: 60, loud: 80 },
  { name: "스텝 승합차", mass: 1160, trunk: 160, loud: 100 },
  { name: "불드라이버", mass: 1104, trunk: 130, loud: 120 },
  { name: "다트", mass: 650, trunk: 40, loud: 55, note: "연비 가장 나쁨" },
];

// 정비 화면의 부품. masks 는 web/public/guide/mech/4door_<이름>.webp (흰색 마스크).
// tools 는 guide/item 아이콘. level 은 차량정비 레벨(일반 차 기준), know 는 차종 정비 지식 필요 여부.
export const mechParts = [
  { id: "wheel", label: "타이어", masks: ["wheel_front_left", "wheel_front_right", "wheel_rear_left", "wheel_rear_right"], tools: ["CarJack", "LugWrench"], level: 1, know: false, note: "공기는 정비 화면에서 우클릭 → 「공기압 넣기」(타이어 펌프 필요)", nokey: true },
  { id: "brake", label: "브레이크", masks: ["brake_front_left", "brake_front_right", "brake_rear_left", "brake_rear_right"], tools: ["CarJack", "Wrench"], level: 3, know: true, note: "타이어를 먼저 뺀다", nokey: true },
  { id: "suspension", label: "서스펜션", masks: ["suspension_front_left", "suspension_front_right", "suspension_rear_left", "suspension_rear_right"], tools: ["CarJack", "Wrench"], level: 3, know: true, note: "타이어를 먼저 뺀다", nokey: true },
  { id: "battery", label: "배터리", masks: ["battery"], tools: ["Screwdriver"], level: 0, know: false, note: "시동을 끄고 뗀다. 다 닳으면 차량 배터리 충전기(전기 필요)로 채운다" },
  { id: "engine", label: "엔진", masks: ["engine"], tools: ["EngineParts", "Wrench"], level: 4, know: false, note: "예비 엔진 부품으로 수리한다. 필요 레벨은 일반 4, 대형 5, 스포츠 6" },
  { id: "hood", label: "후드", masks: ["hood"], tools: ["Wrench"], level: 3, know: true, note: "후드가 깨지면 좀비를 칠 때 엔진이 상한다" },
  { id: "trunk", label: "트렁크 문", masks: ["trunk"], tools: ["Wrench"], level: 3, know: true },
  { id: "door", label: "문", masks: ["door_front_left", "door_front_right", "door_rear_left", "door_rear_right"], tools: ["Wrench"], level: 4, know: true, note: "창문을 먼저 뺀다" },
  { id: "window", label: "옆 창문", masks: ["window_front_left", "window_front_right", "window_rear_left", "window_rear_right"], tools: ["Screwdriver"], level: 3, know: true },
  { id: "windshield", label: "앞·뒤 유리", masks: ["window_windshield", "window_rear_windshield"], tools: ["Screwdriver"], level: 5, know: true },
  { id: "headlight", label: "전조등", masks: ["headlight_left", "headlight_right"], tools: ["Screwdriver"], level: 0, know: false },
  { id: "muffler", label: "머플러", masks: ["muffler"], tools: ["Wrench"], level: 5, know: true, note: "없거나 망가지면 엔진 소리가 2배가 된다", nokey: true },
  { id: "gastank", label: "연료 탱크", masks: ["gastank"], tools: ["Screwdriver", "Wrench"], level: 5, know: true, note: "비어 있어야 뗀다" },
];
export const toolNames = {
  CarJack: "잭",
  LugWrench: "십자 휠 렌치",
  Wrench: "렌치",
  Screwdriver: "스크류드라이버",
  EngineParts: "예비 엔진 부품",
};
export const mechOpen = [
  { keys: ["U"], text: "차를 세우고 U (차 안이나 옆)" },
  { keys: ["V"], text: "V → 「차량 정비」" },
  { keys: ["E"], text: "후드 앞에서 E" },
];
// 차종별 정비 지식 잡지
export const mechBooks = [
  { icon: "item/MagazineMechanic1", type: "일반 차", name: "라이네스 표준 차량 설명서", cars: "다트, 니알라, 세리스 웨건, 랜처, 경찰차" },
  { icon: "item/MagazineMechanic2", type: "대형 차", name: "라이네스 상용 차량 설명서", cars: "올-터레인, D6, 불드라이버, 밴, 스텝 승합차" },
  { icon: "item/MagazineMechanic3", type: "스포츠 차", name: "라이네스 고성능 차량 설명서", cars: "코세트, 랭 4000, 대시 엘리트" },
];

// 운전할 때 주의
export const driveNotes = [
  { icon: "vehicle/engine", title: "차는 시끄럽다", text: "엔진 소리, 경적(150칸), 경보(150칸), 사이렌(100칸)이 좀비를 부른다. 경적은 꼭 필요할 때만." },
  { icon: "vehicle/icon_enginetrouble_light", title: "좀비를 치면 차가 상한다", text: "후드가 먼저 상하고, 후드가 깨지면 엔진이 상한다. 후진으로 치면 트렁크·연료 탱크가 상한다." },
  { icon: "vehicle/vehicle_exit", title: "세게 부딪히면 모두 다친다", text: "탄 사람 모두 다치고, 크게 부딪히면 골절이나 유리 박힘까지 생긴다. 차로 친구를 쳐도 피해는 없다." },
  { icon: "vehicle/vehicle_lockdoors", title: "짐은 트렁크에", text: "트렁크는 차 뒤에서 연다. 글러브박스는 앞좌석, 좌석에도 짐을 둔다. 트렁크 문이 없으면 급커브에서 짐이 떨어진다." },
  { icon: "vehicle/vehicle_temperatureHOT", title: "히터와 배터리", text: "시동을 켜 두면 배터리가 찬다. 시동을 끈 채 전조등·라디오를 켜 두면 닳는다." },
  { icon: "vehicle/vehicle_changeseats", title: "트레일러 끌기", text: "트레일러를 차 뒤 6칸 안에 대고 내려서 V → 「연결하기」. 도구는 필요 없다. 차로 다른 차도 끈다." },
];

// 같이 탈 때
export const together = [
  "운전은 한 명(운전석)이 하고, 나머지는 빈자리에 탄다. Z 로 자리를 바꾼다",
  "경적은 운전자만 울린다. 동승자가 Q 를 누르면 외친다",
  "차 주인 개념이 없다. 열쇠를 가진 사람이나 배선 딴 차는 누구나 몬다",
  "열쇠는 하나뿐이다. 글러브박스에 두거나 「설정 → 접근성 설정 → 열쇠 꽂은 채 내리기」를 켜서 같이 쓴다",
  "같이 다닐 땐 차 한 대로. 기름도 소음도 반으로 준다",
];

// 커뮤니티 꿀팁 중 게임 파일과 맞는 것
export const carTips = [
  { text: "연비는 랭 4000·올-터레인이 좋고 다트가 가장 나쁘다", src: "Reddit (42.21 코드 분석)", url: "https://www.reddit.com/r/projectzomboid/comments/1x68czg/" },
  { text: "짐을 많이 싣는 차: 스텝 승합차 160, 밴·불드라이버 130, D6 110. 불드라이버는 가장 시끄럽다", src: "PZwiki Vehicle", url: "https://pzwiki.net/wiki/Vehicle" },
  { text: "열쇠는 며칠 뒤에 생기기도 한다. 단, 한 번 문을 연 차는 다시 안 생긴다", src: "Reddit", url: "https://www.reddit.com/r/projectzomboid/comments/1wyyrfo/" },
  { text: "정비 레벨은 폐차장의 여러 차로 올린다. 같은 차의 같은 부품은 하루에 한 번만 경험치가 들어온다", src: "PZwiki Mechanics", url: "https://pzwiki.net/wiki/Mechanics" },
  { text: "타이어·브레이크·서스펜션·머플러는 잠긴 차에서도 열쇠 없이 뗄 수 있다", src: "게임 파일 (mechanicRequireKey)" },
];
