// 플레이 팁 페이지의 요리 탭.
//
// 근거: docs/research/cooking.md (42.21 스크립트·Lua·KO 번역, jar 디컴파일). 메뉴 이름은 바닐라 KO 표기다.
// 추천 요리 수치는 게임 계산식으로 낸 값이다(요리 0레벨, 신선한 재료, 양념 없음). 게임 안에서 잰 값은 아니다.
// 그림: "item:이름" → web/public/icons/item/이름.webp, "cook:이름" → web/public/guide/cook/이름.webp

export const cookFacts = [
  { icon: "item:PotFull", title: "익히면 1.3배 든든하다", text: "익힌 음식은 배고픔이 1.3배 더 채워진다. 탄 음식은 3분의 1, 상한 음식은 절반도 안 된다." },
  { icon: "item:Bowl", title: "바탕을 우클릭해 재료를 넣는다", text: "냄비(물)·프라이팬·그릇·빵 조각을 우클릭 → 「수프 만들기」 → 넣을 재료를 고른다. 재료 옆 괄호 숫자가 요리에 더해지는 배고픔이다." },
  { icon: "item:Carrots", title: "재료는 여러 가지로", text: "서로 다른 재료를 넣을 때마다 불행이 5씩 준다. 같은 재료를 또 넣으면 보너스가 없다. 요리 0레벨이면 3가지까지가 좋다." },
  { icon: "item:Steak", title: "날고기는 꼭 익힌다", text: "날고기·생선·달걀을 날로 먹으면 식중독에 걸린다. 이런 재료를 넣은 수프·볶음도 익히기 전에는 위험하다." },
  { icon: "item:Cabbage", title: "시든 채소는 수프로", text: "냄비·그릇으로 만든 요리는 새 음식이라 신선하다. 신선하지 않은 채소는 수프에 넣어 처리한다." },
  { icon: "item:Fork", title: "포크·숟가락을 챙긴다", text: "갖고 있으면 그릇·통조림 음식을 먹을 때 기분 좋아지는 효과가 25% 커진다." },
];

// 익히는 순서
export const cookSteps = [
  { icon: "item:Pot", title: "재료를 넣는다", text: "바탕에 재료를 넣는다. 스테이크·감자처럼 그대로 익혀도 된다." },
  { icon: "cook:Container_Oven", title: "열원에 넣는다", text: "오븐·바비큐·모닥불 옆에서 보관함 창을 열고 음식을 끌어 넣는다." },
  { icon: "item:Lighter", title: "켜거나 불을 붙인다", text: "오븐은 「켜기」(온도 200 이상이 가장 빠르다). 바비큐·모닥불은 땔감을 넣고 라이터·성냥으로 「모닥불 불 붙이기」." },
  { icon: "item:PotFull", title: "막대가 차면 꺼낸다", text: "음식에 마우스를 올리면 「요리 중」 막대가 보인다. 빨간 「타는 중」이 보이면 바로 꺼낸다. 오븐 타이머는 알람만 울리고 꺼지지 않는다." },
  { icon: "item:BowlFull", title: "그릇에 나눈다", text: "익힌 수프·스튜·파스타·밥은 제작창(B)의 「음식 4그릇으로 나누기」로 나눠 같이 먹는다." },
];

// 진화형 요리(바탕에 재료를 넣는 요리). cook: 익히는 기준 시간(분), null 이면 불이 필요 없다.
// ings: 들어가는 재료 종류(그림, 이름)
const ING = {
  veg: ["item:Carrots", "채소"],
  meat: ["item:Steak", "고기"],
  cmeat: ["item:Steak", "익힌 고기"],
  fish: ["item:FishFillet", "생선"],
  fruit: ["item:Apple", "과일"],
  egg: ["item:Egg", "달걀"],
  cheese: ["item:Cheese", "치즈"],
  spice: ["item:Salt", "양념"],
};
const ings = (...k) => k.map((x) => ({ icon: ING[x][0], name: ING[x][1] }));

export const recipes = [
  { name: "수프", base: { icon: "item:Pot", label: "냄비 + 물 90% 이상" }, result: "item:PotFull", menu: "수프 만들기", max: 6, cook: 50, ings: ings("veg", "meat", "fish", "spice"), note: "갈증도 채워 준다. 익힌 뒤에는 재료를 더 넣을 수 없다." },
  { name: "스튜", base: { icon: "item:Pot", label: "냄비 + 물 90% 이상" }, result: "item:PotFull", menu: "스튜 만들기", max: 6, cook: 70, ings: ings("meat", "veg", "fish", "spice"), note: "고기가 잘 어울린다. 식으면 불행이 조금 오른다." },
  { name: "볶음", base: { icon: "item:Pan", label: "프라이팬" }, result: "item:PanFull", menu: "볶음 만들기", max: 4, cook: 60, ings: ings("meat", "veg", "egg", "spice"), note: "생고기를 빨리 처리하기 좋다." },
  { name: "구이", base: { icon: "item:Roastingpan", label: "오븐 쟁반" }, result: "item:RoastingpanFull", menu: "구이 만들기", max: 6, cook: 60, ings: ings("meat", "veg", "fish", "spice"), note: "볶음과 같은 재료를 6개까지 넣는다." },
  { name: "파스타", base: { icon: "item:Pot_Water", label: "냄비 [파스타]" }, result: "item:PotFull", menu: "파스타 만들기", max: 5, cook: 20, ings: ings("meat", "veg", "cheese", "spice"), note: "제작창 「요리용 냄비에 파스타 넣기」로 바탕을 만든다. 익힌 뒤 하루면 신선하지 않다." },
  { name: "밥", base: { icon: "item:Pot_Water", label: "냄비 [쌀]" }, result: "item:PotFull", menu: "밥 만들기", max: 5, cook: 20, ings: ings("meat", "veg", "fish", "spice"), note: "제작창 「냄비에 쌀 넣기」로 바탕을 만든다." },
  { name: "샐러드", base: { icon: "item:Bowl", label: "빈 그릇" }, result: "item:TZ_CraftSalat", menu: "샐러드 만들기", max: 6, cook: null, ings: ings("veg", "fruit", "cmeat", "spice"), note: "불이 필요 없다. 고기·생선·달걀은 익힌 것만 들어간다." },
  { name: "과일 샐러드", base: { icon: "item:Bowl", label: "빈 그릇" }, result: "item:FruitSalad", menu: "과일 샐러드 만들기", max: 6, cook: null, ings: ings("fruit", "spice"), note: "과일이 상하기 전에 한 번에 처리한다." },
  { name: "샌드위치", base: { icon: "item:BreadSlices", label: "빵 조각" }, result: "item:Sandwich", menu: "샌드위치 만들기", max: 4, cook: null, warm: true, ings: ings("cmeat", "veg", "cheese", "spice"), note: "불 없이 된다. 데우면 1.3배 든든하다. 빵의 신선도를 이어받는다." },
  { name: "버거", base: { icon: "item:BunsHamburger_single", label: "햄버거 빵" }, result: "item:Burger", menu: "버거 만들기", max: 4, cook: null, ings: ings("cmeat", "veg", "egg", "spice"), note: "고기는 익힌 것만 들어간다." },
  { name: "타코·부리토", base: { icon: "item:TacoShell", label: "타코 쉘·토르티야" }, result: "item:Taco", menu: "타코 만들기", max: 5, cook: null, ings: ings("cmeat", "veg", "fish", "spice"), note: "고기·생선·달걀은 익힌 것만 들어간다." },
  { name: "따뜻한 음료", base: { icon: "item:Mugl", label: "머그컵 + 물 가득" }, result: "item:MugFulll", menu: "음료 만들기", max: 3, cook: 10, ings: [{ icon: "item:Mugl", name: "차·커피·코코아" }, { icon: "item:Salt", name: "설탕·꿀" }], note: "갈증도 채워 준다." },
  { name: "오믈렛", base: { icon: "item:Egg", label: "프라이팬 + 날달걀 2" }, result: "item:PanFull", menu: "오믈렛", max: 3, cook: 10, ings: ings("veg", "meat", "cheese", "spice"), note: "제작창 「오믈렛 준비하기」(섞는 도구 필요)로 바탕을 만든다." },
  { name: "파이", base: { icon: "item:PieWhole", label: "파이 반죽", learn: true }, result: "item:PieWhole", menu: "식사용 파이 만들기", max: 4, cook: 40, ings: ings("meat", "veg", "fruit", "spice"), note: "반죽은 배워야 만든다. 고기·채소는 식사용, 과일은 간식용 파이." },
  { name: "피자", base: { icon: "item:PizzaWhole", label: "피자 반죽", learn: true }, result: "item:PizzaWhole", menu: "피자", max: 6, cook: 20, ings: ings("meat", "veg", "fish", "spice"), note: "반죽은 배워야 만든다." },
];

// 쉬운 추천 요리(요리 0레벨, 배고픔은 익힌 뒤 값. 툴팁과 같은 단위)
export const bestDishes = [
  { name: "채소 수프", base: "item:Pot", items: [["item:Carrots", "당근"], ["item:Potato", "감자"], ["item:Cabbage", "양배추"], ["item:Tomato", "토마토"]], hunger: 65, unhappy: -15, kcal: 199, cook: true, why: "집집마다 있는 채소로 바로 만든다. 날로 먹으면 50인데 수프로 65가 되고 갈증도 채운다." },
  { name: "통조림 스튜", base: "item:Pot", items: [["item:CannedBologneseOpen", "볼로네제"], ["item:CannedCornOpen", "옥수수"], ["item:CannedPotatoOpen", "감자"], ["item:CannedTomatoOpen", "토마토"]], hunger: 91, unhappy: -15, kcal: 1120, cook: true, why: "통조림은 안 따면 상하지 않아 쌓아 두기 좋다. 한 냄비로 하루 열량의 큰 몫이다." },
  { name: "볼로네제 파스타", base: "item:Pot_Water", items: [["item:CannedBologneseOpen", "볼로네제"], ["item:Tomato", "토마토"], ["item:Cheese", "치즈"]], hunger: 72, unhappy: -15, kcal: 1189, cook: true, why: "열량이 가장 높다. 익힌 파스타는 금방 상하니 4그릇으로 나눠 바로 먹는다." },
  { name: "고기 채소 볶음", base: "item:Pan", items: [["item:Steak", "스테이크"], ["item:Potato", "감자"], ["item:Carrots", "당근"], ["item:Tomato", "토마토"]], hunger: 75, unhappy: -15, kcal: 219, cook: true, why: "금방 상하는 생고기를 빨리 처리한다. 꼭 익혀서 먹는다." },
  { name: "햄 치즈 샌드위치", base: "item:BreadSlices", items: [["item:HamSlices", "햄 조각"], ["item:Cheese", "치즈"], ["item:Lettuce", "양상추"]], hunger: 28, unhappy: -15, kcal: 485, cook: false, why: "불도 전기도 없이 바로 만든다. 데우면 36으로 오른다." },
  { name: "과일 샐러드", base: "item:Bowl", items: [["item:Apple", "사과"], ["item:Banana", "바나나"], ["item:Orange", "오렌지"], ["item:Pear", "배"]], hunger: 30, unhappy: -15, kcal: 170, cook: false, why: "과일이 상하기 전에 한 번에 먹고 기분도 좋아진다." },
];

// 열원. speed: 같은 음식이 익는 속도(기준 대비 최고치), null 은 확인 못 함.
export const heatSources = [
  { icon: "cook:Container_Oven", name: "오븐", need: "전기", cut: "단전 뒤엔 발전기 필요", speed: 2, warn: "온도 200 이상이 가장 빠르다. 타이머는 알람만 울리고 꺼지지 않는다. 탄 음식을 오래 두면 불이 난다." },
  { icon: "cook:Container_Microwave", name: "전자레인지", need: "전기", cut: "단전 뒤엔 발전기 필요", speed: 1.53, warn: "냄비·팬·통조림 같은 금속을 넣으면 불이 나고 고장 난다. 고기·빵·파스타는 맛이 떨어진다(불행·지루함 +5)." },
  { icon: "item:Charcoal", name: "바비큐 그릴", need: "숯·땔감, 또는 프로판 통", cut: "단전과 상관없음", speed: 1.2, warn: "프로판 그릴은 프로판 통을 넣고 「켜기」." },
  { icon: "item:Logs", name: "벽난로·난로", need: "땔감", cut: "단전과 상관없음", speed: 1.2, warn: "실내에서 쓰는 열원이다." },
  { icon: "cook:Container_Campfire", name: "모닥불", need: "돌 3개로 짓고 땔감", cut: "단전과 상관없음", speed: 1.27, warn: "실내에서 피우면 10분마다 옆 바닥에 불이 번질 수 있다. 불빛과 소리로 좀비가 온다." },
  { icon: "cook:Build_CookingPit", name: "모닥불 구덩이", need: "석공 1~2로 짓고 땔감", cut: "단전과 상관없음", speed: null, warn: "건축 창에서 짓는다." },
];
export const fuels = [
  { icon: "item:Logs", name: "통나무", hours: 6 },
  { icon: "item:Plank", name: "판자", hours: 2 },
  { icon: "item:Charcoal", name: "숯", hours: 0.5 },
];
export const boilWater = {
  icons: ["item:Pot", "item:Kettle", "item:Mugl", "item:WaterPurificationTablets"],
  text: "단수 뒤 받은 빗물·강물은 「오염된 물」이다. 냄비·주전자·머그컵에 담아 불에 올려 두면 끓어서 깨끗해진다. 플라스틱 물병은 전자레인지에서만 데운다. 물 정수 알약 1알로도 된다.",
};

// 음식 상태
export const foodStates = [
  { name: "신선한", hunger: "그대로", mood: "그대로", tone: "good" },
  { name: "데운 (익힌)", hunger: "×1.3", mood: "따뜻할 때 불행 −2", tone: "good" },
  { name: "신선하지 않은", hunger: "÷1.3", mood: "불행·지루함 +10", tone: "" },
  { name: "상한", hunger: "÷2.2", mood: "불행·지루함 +20, 식중독 위험", tone: "bad" },
  { name: "타 버린", hunger: "÷3", mood: "불행·지루함 +20", tone: "bad" },
  { name: "냉동된", hunger: "그대로", mood: "불행·지루함 +30, 요리 재료로 못 씀", tone: "" },
];
export const storage = [
  { icon: "cook:Container_Fridge", title: "냉장고", text: "전기가 있으면 상하는 속도가 5분의 1이 된다." },
  { icon: "cook:Container_Freezer", title: "냉동고", text: "4시간이면 얼고, 언 동안은 상하지 않는다. 꺼내면 1시간 반쯤에 녹는다." },
  { icon: "item:CannedCornOpen", title: "통조림", text: "안 딴 통조림은 상하지 않는다. 따면 2~3일 신선하고 4~5일이면 상한다." },
  { icon: "item:PotFull", title: "만든 요리", text: "수프·스튜·볶음은 3일 신선(5일 상함), 샐러드는 2일, 익힌 밥·파스타는 1일이다." },
];

// 요리 기술
export const cookSkill = [
  { lv: "0", text: "재료 3가지까지 넣을 때마다 불행 −5" },
  { lv: "3", text: "재료 6가지까지 넣을 때마다 불행 −5" },
  { lv: "5", text: "음식 툴팁에 조리 시간(분)이 보인다" },
  { lv: "7", text: "상한 재료도 넣을 수 있다(배고픔은 5%만 더해짐)" },
  { lv: "10", text: "재료를 70%만 쓰고 열량은 약 117%가 된다" },
];
export const cookXp = [
  { icon: "item:Carrots", text: "요리에 재료를 하나 넣을 때 경험치 3" },
  { icon: "item:PotFull", text: "음식이 다 익었을 때 경험치 10 (멀티에서 들어오는지는 확인 못 함)" },
  { icon: "item:Book9", text: "요리 경험치는 기본 25%만 들어온다. 요리 1~5권을 먼저 읽는다. 우리 서버는 거의 바로 읽힌다" },
  { icon: "item:MagazineFood", text: "「열정적인 요리사」(3점)는 요리 +2와 반죽·쿠키·피자 등 제작법 15개를 알고 시작한다" },
];

// 제작창(B) 요리 제작법. learn: 배워야 만든다(요리 레벨이 오르거나 잡지를 읽으면 배움)
export const cookCrafts = [
  { icon: "item:CanOpener", name: "통조림 열기", need: "깡통 따개" },
  { icon: "item:KnifeChopping", name: "날붙이로 통조림 열기", need: "칼이나 날카로운 돌 조각(손을 다칠 수 있다)" },
  { icon: "item:BreadSlices", name: "빵 자르기", need: "칼 → 빵 조각 3" },
  { icon: "item:Pot_Water", name: "요리용 냄비에 파스타·쌀 넣기", need: "냄비, 물 1.5L, 파스타·쌀" },
  { icon: "item:BowlFull", name: "음식 4그릇으로 나누기", need: "그릇 4, 익힌 냄비 요리" },
  { icon: "item:Egg", name: "오믈렛 준비하기", need: "프라이팬, 날달걀 2, 섞는 도구" },
  { icon: "item:HamSlices", name: "햄 자르기", need: "칼 → 햄 조각 6" },
  { icon: "item:Chicken", name: "닭 자르기", need: "칼 → 닭다리·날개·가슴살" },
  { icon: "item:FishFillet", name: "생선에서 살 바르기", need: "칼 → 생선살 2" },
  { icon: "item:Dough", name: "빵 반죽 준비하기", need: "밀가루·소금·효모·물, 밀대", learn: "요리 7 또는 잡지" },
  { icon: "item:PieWhole", name: "파이 반죽 준비하기", need: "밀가루·버터·소금·물, 밀대", learn: "요리 7 또는 잡지" },
  { icon: "item:PizzaWhole", name: "피자 준비하기", need: "밀가루·치즈·피자 소스·효모", learn: "요리 6 또는 잡지" },
];
