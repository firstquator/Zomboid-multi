# 요리 조사 기록 (42.21, 2026-10-18 확인)

사이트 "플레이 팁" 페이지의 "요리" 탭에 넣을 재료다. 처음 하는 친구가 그림(게임 아이콘)만 보고도 따라 할 수 있게 고르는 것을 목표로 했다.

## 기준과 표기

- 게임: **42.21.0** 설치본. 근거는 거의 다 게임 파일(스크립트·Lua·번역)과 `projectzomboid.jar` 디컴파일(CFR 0.152)이다. 웹(pzwiki)은 B42 버전이 적힌 페이지만 보조로 봤다.
- 줄임말
  - `PZ/` = `C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\`
  - `KO/` = `PZ/media/lua/shared/Translate/KO/` (한국어 게임 표기)
  - `EVO` = `PZ/media/scripts/generated/evolvedrecipes.txt` (진화형 요리 정의, 714줄)
  - `FOOD` = `PZ/media/scripts/generated/items/food.txt`
  - `RCP/` = `PZ/media/scripts/generated/recipes/`
  - `LUA/` = `PZ/media/lua/`
  - `jar:클래스 N행` = `projectzomboid.jar` 를 CFR 로 디컴파일한 그 클래스의 줄 번호. 예: `jar:EvolvedRecipe 265~469` = `zombie/scripting/objects/EvolvedRecipe.java`
  - `DATA` = 저장소 `web/public/data/items-detail.json` (아이템 이름·아이콘·food 필드)
  - 아이콘 = 저장소 `web/public/icons/item/<이름>.webp`. 표에 적은 아이콘 파일은 모두 존재를 확인했다. 가구(오븐 등)는 아이템 아이콘이 없어서 게임 UI 텍스처 이름을 적었다(저장소에 없음, `PZ/media/texturepacks/UI.pack`·`UI2.pack` 안).
- 한국어 표기는 바닐라 `KO/` 기준이다. 우리 서버는 통합 번역 모드를 쓰므로 실제 화면 문구가 조금 다를 수 있다(→ 8장).
- 샌드박스는 기본 프리셋(`PZ/media/lua/shared/Sandbox/Apocalypse.lua`) 기준. 요리에 관련된 값: `FoodRotSpeed = 3`(보통), `FridgeFactor = 3`(냉장 5배), `ElecShut = 2`(14~30일 사이 단전), `WaterShut = 2`, `EnablePoisoning = 1`(독 넣기 켜짐), `DaysForRottenFoodRemoval = -1`(상한 음식 안 사라짐).
- 수치 표기: 게임 툴팁의 "배고픔 -65"를 사이트에서는 "배고픔 65 줄임"처럼 쓰면 된다. 불행(Unhappiness)도 음수가 좋은 쪽이다.

---

## 0. 한눈에 보는 핵심 (사이트 맨 위 요약 후보)

1. **익히면 배가 1.3배 더 부르다.** 익힌 음식의 배고픔 회복은 원래 값 × 1.3이다. 탄 음식은 1/3, 신선하지 않은 음식은 1/1.3, 상한 음식은 1/2.2로 줄어든다. (`jar:Food.getHungerChange 1517~1536`)
2. **요리(진화형 요리)는 그릇·냄비·빵 같은 "바탕"을 우클릭해서 재료를 하나씩 넣는 방식**이다. 메뉴는 「수프 만들기」 → 「당근 (8) 주 재료로 하기」, 그다음부터는 「수프」 → 「감자 (18) 추가하기」. (`LUA/client/ISUI/ISInventoryPaneContextMenu.lua 4233~4300`, `KO/ContextMenu.json`)
3. **요리의 배고픔은 넣은 재료의 "괄호 안 숫자" 합계**다(익히면 × 1.3). 재료가 그보다 크면 나머지는 남는다(양배추를 수프에 넣으면 절반 남음). (`jar:EvolvedRecipe.addItem 326~441`)
4. **서로 다른 재료를 넣을 때마다 불행 5 감소.** 같은 재료를 또 넣으면 보너스가 없고, 세 번째부터는 오히려 불행해진다. 요리 0레벨이면 4번째 재료부터 보너스가 사라지고 5·6번째는 손해다. (`jar:EvolvedRecipe 381~397`)
5. **수프·스튜는 냄비에 물을 90% 이상 채워야 시작**되고, 익힌 뒤에는 재료를 더 넣을 수 없다. 재료를 다 넣고 익힌다. (`EVO` MinimumWater 0.9, `jar:RecipeManager.getEvolvedRecipe 430`)
6. **신선하지 않은 재료도 요리에 넣으면 그 페널티가 없어진다.** 냄비·그릇으로 시작한 요리는 새 음식(신선)으로 만들어진다. 빵으로 시작한 샌드위치만 빵의 나이를 이어받는다. (`jar:EvolvedRecipe 269~304`)
7. **날고기·생선·달걀을 날로 먹으면 식중독**(독 +15). 이런 재료를 넣은 수프·스튜·볶음도 익히기 전에는 위험하다. 샐러드·샌드위치·버거에는 아예 익힌 것만 들어간다. (`jar:BodyDamage.JustAteFood 592~610`, `EVO`의 `|Cooked`)
8. **오븐이 가장 빠르다**(최고 온도에서 표시 시간의 약 절반). 전자레인지·바비큐·벽난로·모닥불은 그보다 느리다. 오븐 온도를 맨 아래 두 칸(0·50)에 두면 안 익는다. (`jar:IsoStove`, `LUA/client/ISUI/Fireplace/ISOvenUI.lua 122~147`)
9. **전자레인지에 냄비·팬·통조림 같은 금속을 넣으면 불이 나고 고장 난다.** 날고기·빵·파스타 등은 전자레인지로 익히면 불행·지루함 +5. (`jar:IsoStove 90~99, 253~265`, `jar:Food 385~432`)
10. **단전 뒤 오븐·전자레인지는 발전기를 연결해야만 켜진다.** 바비큐·벽난로·모닥불은 땔감만 있으면 된다. (`LUA/client/ISUI/LootWindow/Handlers/StoveToggle.lua 8`)
11. **실내 모닥불은 위험하다.** 10분마다 1/5 확률로 옆 칸 나무·카펫 바닥에 불이 붙는다. 불빛·소리 반경도 실내가 더 크다(실외 최대 10칸, 실내 최대 18칸). (`LUA/server/Camping/SCampfireSystem.lua 96~130`, `SCampfireGlobalObject.lua 319~327`)
12. **물 끓이기:** 냄비·주전자·머그컵에 담은 오염된 물을 불에 올려 두면 깨끗한 물로 바뀐다. 플라스틱 물병은 전자레인지에서만. (`jar:InventoryItem 1303~1333`)
13. **냉장고는 상하는 속도를 1/5로, 냉동고는 0으로** 만든다(전기가 있을 때). 안 딴 통조림은 아예 안 상한다. 익힌 밥·파스타는 하루면 신선하지 않게 된다. (`jar:Food.getFridgeFactor 642~651`, `updateAge 686~698`, `404~408`)
14. **요리 기술은 경험치 배율이 기본 25%다.** "열정적인 요리사"(+2, 133%)나 주방장(+4, 166%)이 아니면 요리책을 꼭 읽는다. 재료 하나 넣을 때 3, 익힐 때 10을 얻는다. (`jar:IsoGameCharacter 15616~15660`, `jar:EvolvedRecipe 463~467`, `jar:Food 433~445`)
15. **요리 7레벨부터 상한 재료도 넣을 수 있다**(배고픔은 5~10%만). 레벨이 오를수록 재료를 덜 쓰고(10레벨 70%) 열량이 늘어난다. (`jar:EvolvedRecipe 222~233, 356~365, 391~402`)
16. **포크나 숟가락을 갖고 있으면** 통조림·그릇 음식을 먹을 때 행복·지루함 효과가 25% 좋아진다(나쁜 효과는 25% 줄어듦). (`LUA/shared/TimedActions/ISEatFoodAction.lua 255~315`, `jar:BodyDamage 564~575`)

---

## 1. 진화형 요리 (evolved recipe)

### 1-1. 정의 파일과 전체 목록

- **사이트에 쓸 한 줄**: 수프·스튜·볶음·샐러드·샌드위치 같은 "내가 재료를 골라 넣는 요리"는 모두 27가지 종류가 있다(같은 요리의 냄비 종류 차이를 합치면 61개 정의).
- **근거**: `EVO` (B42 위치는 `media/scripts/generated/` 아래. B41 의 `media/scripts/evolvedrecipes.txt` 와 다르다). 낚시 밑밥 1개는 `RCP/recipes_fishing_evolvedrecipe.txt`(AddBaitToChum, 「미끼」). 재료 쪽은 각 음식 아이템의 `EvolvedRecipe = Soup:8;Stew:8;…` 줄이 정한다(`FOOD` 372개, `PZ/media/scripts/generated/items/drainable.txt` 2개). 재료 이름이 요리 정의 이름이나 `Template` 과 같으면 연결된다(`jar:Item.OnScriptsLoaded 3759~3777`, 대소문자 무시). `|Cooked` 가 붙은 재료는 익힌 것만 넣을 수 있다(`jar:Item 3458~3490`, `jar:EvolvedRecipe.needToBeCooked 136~142`).

### 1-2. 만드는 법과 메뉴 문구

- **사이트에 쓸 한 줄**: 냄비(물 가득)·프라이팬·그릇·빵 조각을 **우클릭 → 「○○ 만들기」 → 넣을 재료 선택**. 재료를 더 넣으려면 만들어진 요리를 다시 우클릭 → 「○○」 → 「재료 추가하기」. 익혀야 하는 요리는 그다음 열원에 넣는다.
- 순서
  1. 바탕을 준비한다. 수프·스튜는 냄비(또는 양동이)에 물을 **90% 이상**(요리용 냄비 1.5L 기준 1.35L 이상), 음료는 머그컵에 물을 **가득**. 샐러드 그릇은 **비어 있어야** 한다. 물은 싱크대·우물 등에서 「물 담기」. (`jar:EvolvedRecipe.getItemsCanBeUse 150~155`, `hasMinimumWater 628~638`, `KO/ContextMenu.json` ContextMenu_Fill "물 담기")
  2. 바탕을 우클릭하면 「수프 만들기」「스튜 만들기」가 뜬다(가방이나 주변 보관함에 넣을 수 있는 재료가 하나라도 있어야 보인다).
  3. 하위 메뉴: 「당근 (8) 주 재료로 하기」처럼 재료 이름과 괄호 안 숫자(이 요리에 더해지는 배고픔)가 나온다. 「무작위 채소 주 재료로 만들기」처럼 종류별 무작위 항목도 있다. 양념은 「소금 (향신료/소스) 주 재료로 하기」처럼 표시된다.
  4. 한 번 넣으면 바탕이 결과물(예: 「요리용 냄비 [스프]」)로 바뀐다. 이 결과물을 우클릭하면 메뉴가 「수프」 → 「감자 (18) 추가하기」 / 「무작위 채소 추가하기」로 바뀐다.
  5. 넣을 수 없는 항목은 회색이고 이유가 뜬다: 「냉동식품을 추가할 수 없습니다.」, 「조리된 상태여야 합니다.」
  6. 재료 넣는 시간은 100틱 − 요리 레벨×2.5틱(아주 짧다). 이름은 넣은 재료로 자동으로 붙는다(예: "당근, 감자 그리고 양배추 수프"; 재료 종류가 3개를 넘으면 그냥 "수프").
- **메뉴 문구(한국어)**: ContextMenu_Create_From_Ingredient "%1 만들기", ContextMenu_From_Ingredient "%1 %2 주 재료로 하기", ContextMenu_Add_Ingredient "%1 %2 추가하기", ContextMenu_FromRandom "무작위 %1 주 재료로 만들기", ContextMenu_AddRandom "무작위 %1 추가하기", ContextMenu_EvolvedRecipe_Spice "(향신료/소스)", ContextMenu_EvolvedRecipe_Poison "(독)", ContextMenu_CantAddFrozenFood "냉동식품을 추가할 수 없습니다.", ContextMenu_NeedCooked "조리된 상태여야 합니다.", ContextMenu_EvolvedRecipe_RecipeName "%1 %2", ContextMenu_EvolvedRecipe_and "그리고".
- **근거**: `LUA/client/ISUI/ISInventoryPaneContextMenu.lua` 332~334(바탕 아이템을 우클릭했을 때 요리 목록 찾기), 2008~2021(무작위 종류), 2028~2050(재료 항목·회색 처리), 4233~4300(메뉴 구성: 결과물이 아니면 "만들기", 결과물이면 요리 이름만), `LUA/shared/TimedActions/ISAddItemInRecipe.lua` 100~120(실행), 128~222(이름 짓기), 225~229(시간), `KO/ContextMenu.json` 171~173, 186~198, 311, 368~369, 474.
- **B42**: 확인(게임 파일)

### 1-3. 진화형 요리 표

- "최대 재료" = 넣을 수 있는 재료 수(양념 제외 아님, 같은 칸을 씀). "익혀야 함" 칸의 숫자는 조리 시간/타는 시간(기준 분, 2-1 참고). "재료 종류" 숫자는 그 요리에 들어갈 수 있는 아이템 수(42.21 스크립트에서 센 값).
- 메뉴 문구는 바탕을 처음 우클릭했을 때의 문구다. 바탕이 곧 결과물인 요리(오믈렛·빵·피자 등)는 「요리 이름」만 나오고 하위 메뉴가 「~ 추가하기」다.

| 이름 | 기본 아이템 id | 아이콘(기본 → 결과) | 결과 아이템 id | 최대 재료 | 익혀야 함 | 들어가는 재료 종류 | 메뉴 문구 |
|---|---|---|---|---|---|---|---|
| 수프 | `Base.Pot` (물 90% 이상) | `Pot` → `PotFull` | `Base.PotOfSoupRecipe` 「요리용 냄비 [스프]」 | 6 | 예 (50/100) | 채소 48, 고기 25, 생선·해산물 12, 콩 9, 버섯 9, 빵 5, 달걀 4, 쌀 4, 면 3, 치즈 2, 견과 2, 기타(호박·땅콩버터 등) 8 + 양념·소스 62 (총 193) | 「수프 만들기」 |
| 스튜 | `Base.Pot` (물 90% 이상) | `Pot` → `PotFull` | `Base.PotOfStew` 「요리용 냄비 [스튜]」 | 6 | 예 (70/140), 차갑게 먹으면 불행 +2 | 채소 46, 고기 41, 생선·해산물 13, 콩 9, 버섯 9, 빵 5, 달걀 4, 쌀 4, 사료 3, 면 2, 치즈 2, 기타 7 + 양념 56 (201) | 「스튜 만들기」 |
| 볶음 | `Base.Pan` | `Pan` → `PanFull` | `Base.PanFriedVegetables` 「볶음 요리」 | 4 | 예 (60/120, 스크립트 기본값) | 채소 41, 고기 38, 생선·해산물 14, 버섯 9, 달걀 3, 콩 3, 면 1, 기타 5 + 양념 63 (179) | 「볶음 만들기」 |
| 구이(오븐 쟁반) | `Base.RoastingPan` 「오븐 쟁반」 | `Roastingpan` → `RoastingpanFull` | `Base.PanFriedVegetables2` 「구이 요리」 | 6 | 예 (60/120) | 볶음과 같음(템플릿 Stir fry) | 「구이 만들기」 |
| 샐러드 | `Base.Bowl` (비어 있음) | `Bowl` → `TZ_CraftSalat` | `Base.Salad` | 6 | 아니오 (고기·생선·달걀은 익힌 것만, 49개) | 채소 42, 고기 31, 생선·해산물 14, 과일 9, 버섯 9, 달걀 7, 빵 5, 콩 3 + 양념 65 (189) | 「샐러드 만들기」 |
| 과일 샐러드 | `Base.Bowl` (비어 있음) | `Bowl` → `FruitSalad` | `Base.FruitSalad` | 6 | 아니오 | 과일 28, 우유 1, 주스 1 + 양념 4 (34) | 「과일 샐러드 만들기」 |
| 샌드위치 | `Base.BreadSlices` 「빵 조각」 | `BreadSlices` → `Sandwich` | `Base.Sandwich` | 4 | 선택 (5/20. 데우면 배고픔 1.3배, 데운 뒤에도 추가 가능) | 고기 37(익힌 것만 다수), 채소 27, 생선·해산물 16, 달걀 9, 버섯 8 + 양념 70 (178, 익힌 것만 48) | 「샌드위치 만들기」 |
| 버거 | `Base.BunsHamburger_single` 「햄버거 빵」 | `BunsHamburger_single` → `Burger` | `Base.BurgerRecipe` 「햄버거」 | 4 (만든 햄버거에 +2) | 아니오 (고기는 익힌 것만, 44개) | 고기 34, 채소 23, 생선·해산물 10, 달걀 9, 버섯 9 + 양념 62 (152) | 「버거 만들기」 |
| 파스타 | `Base.WaterPotPasta` 「요리용 냄비 [파스타]」 | `Pot_Water` → `PotFull` | `Base.PastaPot` 「파스타」 | 5 (손잡이 냄비 4) | 예 (20/50), 따뜻하게·차갑게 효과 있음 | 고기 37, 채소 28, 생선·해산물 12, 버섯 9, 콩 4, 달걀 3, 치즈 3 + 양념 60 (156) | 「파스타 만들기」 |
| 밥 | `Base.WaterPotRice` 「요리용 냄비 [쌀]」 | `Pot_Water` → `PotFull` | `Base.RicePot` 「쌀」 | 5 (손잡이 냄비 4) | 예 (20/50) | 고기 37, 채소 35, 생선·해산물 14, 콩 10, 버섯 9, 달걀 3 + 양념 44 (155) | 「밥 만들기」 |
| 따뜻한 음료 | `Base.Mugl` 「머그컵」(물 가득) | `Mugl` → `MugFulll` | `Base.HotDrink` 「머그컵 [따뜻한 음료]」 | 3 | 예 (10/50) | 차·커피·코코아·우유·과일, 설탕·꿀·약초 같은 양념 32 (45) | 「음료 만들기」 |
| 오믈렛 | `Base.OmeletteRecipe` 「오믈렛」(팬+달걀 2개, 4장) | `PanFull` | 같은 아이템 | 3 | 예 (10/30, 날달걀) | 채소 27, 버섯 9, 고기 5, 치즈 3, 콩 3, 생선 2 + 양념 40 (89) | 「오믈렛」 |
| 식사용 파이 | `Base.PiePrep` 「구울 준비된 파이 반죽」 | `PieWhole` | `Base.PieWholeRaw` 「파이」 | 4 | 예 (40/110) | 채소 28, 고기 28, 생선·해산물 10, 버섯 8 + 양념 12 (86) | 「식사용 파이 만들기」 |
| 간식용 파이 | `Base.PiePrep` | `PieWhole` | `Base.PieWholeRawSweet` 「파이」 | 4 | 예 (40/110) | 과일 24, 단것 8, 기타 7, 우유 1 + 양념 5 (45) | 「간식용 파이 만들기」 |
| 케이크 | `Base.CakePrep` 「케이크 시트」 | `Cake` | `Base.CakeRaw` 「케이크」 | 4 | 예 (40/110) | 과일 25, 단것 20, 기타 7, 우유·주스 + 양념 5 (59) | 「케이크 만들기」 |
| 머핀 | `Base.BakingTray_Muffin` 「머핀 반죽」 | `Muffintray_Batter` | `Base.BakingTray_Muffin_Recipe` | 1 | 예 (30/60) | 과일 27, 단것 8 + 양념 8 (47) | 「머핀 만들기」 |
| 빵(반죽에 넣기) | `Base.BreadDough` 「빵」(반죽) | `Dough` | 같은 아이템 | 2 | 예 (20/50) | 단것 8, 치즈 2, 견과 1, 과일 1, 기타 5 + 양념 28 (45) | 「빵」 |
| 피자 | `Base.PizzaRecipe` 「피자」(반죽) | `PizzaWhole` | 같은 아이템 | 6 | 예 (20/50) | 고기 19, 채소 15, 생선·해산물 10, 버섯 8, 과일 2 + 양념 39 (94) | 「피자」 |
| 오트밀 | `Base.Oatmeal` 「오트밀」(4장 「그릇에 오트밀 담기」) | `Oatmeal` | 같은 아이템 | 3 | 예 (5/30) | 과일 23, 기타 3, 우유 1 + 양념 9 (36) | 「오트밀 그릇」 |
| 토스트 | `Base.Toast` 「토스트」 | `Toast` | 같은 아이템 | 3 | 아니오 (이미 구운 빵) | 단것 7, 생선 3, 고기 2, 콩 2, 치즈 2 + 양념 33 (56) | 「토스트」 |
| 베이글 3종 | `Base.BagelPlain` / `BagelPoppy` / `BagelSesame` | `BagelPlain` 등 | 같은 아이템 | 3 | 선택 (5/10) | 토스트와 같음 | 「베이글」「양귀비 씨앗 베이글」「참깨 베이글」 |
| 핫도그 | `Base.Hotdog` 「핫도그」(4장 「핫도그 준비하기」) | `HotdogCrafted` | 같은 아이템 | 2 | 아니오 | 채소 9, 버섯 7, 고기 4, 치즈 2 + 양념 26 (49) | 「핫도그」 |
| 타코 | `Base.TacoShell` 「타코 쉘」 | `TacoShell` → `Taco` | `Base.TacoRecipe` 「타코」 | 5 (만든 타코에 +2) | 아니오 (익힌 것만 30) | 고기 16, 채소 14, 생선·해산물 12, 달걀 9 + 양념 43 (99) | 「타코 만들기」 |
| 부리토 | `Base.Tortilla` 「토르티야」 | `Tortilla` → `Burrito` | `Base.BurritoRecipe` 「부리토」 | 5 | 아니오 (익힌 것만 34) | 고기 16, 채소 14, 생선·해산물 12, 달걀 9, 쌀 4 + 양념 43 (103) | 「부리토 만들기」 |
| 팬케이크 | `Base.Pancakes` | `Pancakes` → `PancakesFruit` | `Base.PancakesRecipe` | 3 | 아니오 | 과일 29, 단것 9, 기타 6 + 양념 7 (53) | 「팬케이크 만들기」 |
| 와플 | `Base.Waffles` | `Waffles` → `SafflesFruit` | `Base.WafflesRecipe` | 3 | 아니오 | 팬케이크와 같음 | 「와플 만들기」 |
| 아이스크림 콘 | `Base.ConeIcecream` | `ConeIcecream` → `ConeIceCreamTopped` | `Base.ConeIcecreamToppings` | 3 | 아니오 | 단것 25, 과일 17, 기타 8 + 양념 5 (56) | 「아이스크림 콘 만들기」 |

같은 요리의 다른 바탕(표에서 뺀 변형)

| 요리 | 다른 바탕 → 결과 (아이콘) | 최대 재료 |
|---|---|---|
| 수프 | `Base.Bucket`·`Base.BucketEmpty` 「양동이」 → `Base.BucketOfSoup` (`MetalBucket` → `MetalBucket_Soup`), `Base.PotForged` 단조 냄비 → `Base.PotForgedSoupRecipe` (`Pot_Forged` → `Pot_Forged_Soup`), 이미 있던 `Base.PotOfSoup` 「요리용 냄비 [스프]」에 더 넣기 | 6 / 6 / 4 |
| 스튜 | 양동이 → `Base.BucketOfStew` (`MetalBucket_Soup`), 단조 냄비 → `Base.PotForgedStew` (`Pot_Forged_Stew`) | 6 |
| 볶음 | `Base.GridlePan` 「번철 팬」(`Griddle`) → `GriddlePanFriedVegetables`, `Base.PanForged`(`FryingPan_Forged`) → `PanFriedVegetablesForged` (`FryingPan_Forged_Stirfry`) | 4 |
| 샐러드·과일 샐러드 | `Base.ClayBowl` 찰흙 그릇 → `SaladClay` / `FruitSaladClay` | 6 |
| 샌드위치 | `Base.Baguette` 「바게트」 → `Base.BaguetteSandwich` (`Baguette` → `BaguetteSandwich`) | 4 |
| 파스타·밥 | `Base.WaterSaucepanPasta`/`Rice` 손잡이 냄비 → `PastaPan`/`RicePan` (`SaucepanFilled`), 구리 손잡이 냄비(`CopperPot_Pasta`), 단조 냄비(`Pot_Forged_Pasta`/`Pot_Forged_Rice`) | 4 / 4 / 5 |
| 따뜻한 음료 | 찻잔·도자기 찻잔·하얀/스피포 머그컵·찰흙 머그컵·금속/금/은/구리 잔·텀블러 | 3 |
| 오믈렛 | `Base.OmeletteRecipeForged` (`FryingPan_Forged_Eggs`) | 3 |
| 피자·부리토 | 다 구운 `Base.PizzaWhole`, 만든 `Base.Burrito` 에는 양념만(최대 0) | 0 |

- **근거**: `EVO` 3행(Soup)~704행(Hotdog) 각 블록(BaseItem, ResultItem, MaxItems, Cookable, AddIngredientIfCooked, CanAddSpicesEmpty, MinimumWater, Template), 메뉴 이름 `KO/ContextMenu.json` 188~279·296·299·402·464~533·602~632·852~854(ContextMenu_EvolvedRecipe_<정의 이름>), 아이템 이름 `KO/ItemName.json`, 아이콘·조리 시간 `DATA`·`FOOD`. 볶음·구이 결과물은 스크립트에 조리 시간이 없어 기본값 60/120(`jar:Item 112~113`). 재료 수는 `FOOD`·`drainable.txt` 의 `EvolvedRecipe` 줄을 세어 냈다(종류는 FoodType 기준, 고기 = Meat·Beef·Poultry·Game·Venison·Bacon·Sausage·작은 동물 사체).
- **B42**: 확인(게임 파일). 「도자기 찻잔」 음료(HotDrinkTeaCeramic)와 단조 프라이팬 오믈렛(키 이름이 "Omelette Forged" 인데 번역은 "Omelette_Forged")은 한국어 메뉴 키가 없어 화면에 키 문자열이 그대로 나올 수 있다 → 미확인.

### 1-4. 요리가 계산되는 규칙 (코드 그대로)

- **사이트에 쓸 한 줄**: 요리의 배고픔은 재료 숫자의 합(익히면 × 1.3), 다른 재료 하나마다 불행 5 감소, 양념은 종류마다 한 번씩만.
- 규칙
  1. 처음 재료를 넣을 때 바탕이 결과물로 바뀌면서 열량·배고픔·불행·지루함이 0에서 시작한다(바탕이 빵 조각처럼 음식이면 그 음식의 배고픔·열량에서 시작). **스크립트에 적힌 결과물 수치(수프 배고픔 40 등)는 쓰이지 않는다.** 단 수프·스튜의 갈증 -40, 음료의 갈증 -20은 남는다(물로 만든 요리라 목도 축여 준다).
  2. 재료를 넣으면 요리 배고픔 += 괄호 숫자(재료에 남은 배고픔보다 크면 남은 만큼). 재료는 "괄호 숫자 × (1 − 0.03 × 요리 레벨)"만큼 줄어든다. 이미 익힌 재료는 그보다 1/1.3만 줄어든다.
  3. 열량·탄수화물·단백질·지방은 "재료의 값 × (1 + 레벨/15) × 쓴 비율"만큼 더해진다.
  4. 불행: 넣을 때마다 −5. 같은 재료가 이미 n개 들어 있으면 +5n. 이미 들어 있는 재료 수 − 2 가 요리 레벨보다 크면 "(재료 수 − 2 − 레벨×3) × 5"만큼 더 바뀐다. → 0레벨: 4번째 재료는 ±0, 5번째 +5, 6번째 +10(손해). 3레벨 이상: 6개까지 항상 −5씩. (1·2레벨에서는 이 식 때문에 5·6번째 재료가 −10~−20을 주는 특이한 결과가 나온다.) 불행은 +25 위로는 안 올라간다.
  5. 양념(Spice = true 인 111종: 소금, 후추, 케첩, 마요네즈, 버터, 설탕, 꿀, 말린 허브 등)은 **요리마다 같은 양념 한 번씩만**. 넣을 때마다 불행·지루함이 "괄호 숫자 × 2"만큼 준다(소금·후추는 1 → 2씩). 수프·스튜·볶음·구이·샐러드·과일 샐러드·버거·타코·부리토는 재료가 하나 들어간 뒤에만, 샌드위치·파스타·밥·음료·파이·케이크·빵·피자 등은 빈 바탕에도 넣을 수 있다(CanAddSpicesEmpty).
  6. 못 넣는 재료: 얼어 있는 것(모든 요리), 탄 것, 상한 것(요리 7레벨 미만). 상한 바탕(예: 상한 빵 조각)도 7레벨 미만이면 요리 메뉴 자체가 안 뜬다.
  7. 날것이 위험한 재료(날고기·생선·달걀 등 81종)를 날로 넣으면 요리 전체가 "요리되지 않아 식중독 위험"이 된다. 익히면 풀린다.
  8. 익힌 뒤에 재료를 더 넣을 수 있는 요리: 샌드위치·버거·파스타·밥·음료·타코·부리토·팬케이크·와플·오믈렛·토스트·오트밀·베이글·핫도그(AddIngredientIfCooked = true). 수프·스튜·볶음·구이·파이·케이크·머핀·빵·피자는 익히면 끝.
  9. 신선도: 냄비·그릇·컵처럼 음식이 아닌 바탕으로 시작하면 결과물은 새 음식(신선)이다. 빵 조각·바게트처럼 음식 바탕이면 바탕의 나이 비율을 이어받는다. 다른 재료의 나이는 결과에 영향이 없다 → **신선하지 않은 채소는 수프에 넣어 처리**하면 좋다.
  10. 정해진 재료 조합과 정확히 같으면 이름이 바뀌고 배고픔·불행·지루함 보너스가 붙는 "고유 요리"(UniqueRecipe)가 있다. (`jar:EvolvedRecipe.checkUniqueRecipe 471~501`. 42.21 에 정의된 고유 요리 목록은 확인 안 함 → 미확인)
- **근거**: `jar:EvolvedRecipe` 136~142(익힌 것만), 144~183(넣을 수 있는 재료, 물 조건), 192~263(양념·상함·탐·얼음), 265~469(addItem 전체: 289~316 초기화, 326~441 배고픔·열량·불행, 450 재료 기록, 459~461 독, 463~467 경험치 3), 538~585(양념 효과), `jar:RecipeManager.getEvolvedRecipe 421~446`(상한 바탕 7레벨, 익힌 바탕 추가 가능 여부). pzwiki Cooking(42.18.0) "Evolved recipes crafted from a base ingredient … inherit the age of the base ingredient … the age of any other ingredients does not have any effect" 와 일치.
- **B42**: 확인(게임 파일, 디컴파일). 1·2레벨 특이점은 코드상 결과이고 실측은 안 함.

---

## 2. 조리 방법 (열원)

### 2-1. 익는 원리

- **사이트에 쓸 한 줄**: 익힐 음식을 열원 안(보관함 칸)에 넣고 켜거나 불을 붙이면, 음식이 뜨거워진 뒤 "요리 중" 막대가 차고, 다 차면 "데운"이 붙는다. 그대로 두면 "타는 중"이 되고 "타 버린"이 된다.
- 내용
  - 음식 온도(heat)는 열원 온도로 서서히 올라가고, **1.6을 넘어야 익기 시작**한다. 익는 동안 게임 1분마다 조리값이 "음식 온도 ÷ 1.5"씩 쌓인다. 조리값이 MinutesToCook 을 넘으면 익음(+ 요리 경험치 10), MinutesToBurn 을 넘으면 탐. 음식 온도는 최대 3.0이라 **가장 뜨거운 열원에서도 표시 시간의 절반**이 한계다.
  - 툴팁: 「요리 중」 막대(초록) → 「타는 중」 막대(빨강). 요리 5레벨 이상이면 「조리 시간 (분)」이 보인다.
  - 이름 앞에 붙는 말: 「신선한」「신선하지 않은」「상한」「데우지 않은」「데운」「구운」「타 버린」「냉동된」.
  - 오븐·전자레인지 같은 **전력망 전기를 쓰는 열원**에 탄 음식을 오래 두면(조리값 50 이상이고 "익는 시간×2 + 타는 시간÷2" 이상) 확률적으로 불이 난다. 모닥불·벽난로는 예외.
  - 오염된 물을 끓이면 정화되고, 오염된 음식(물에 젖은 것 등)은 10분 넘게 익히면 오염이 풀린다.
  - 익힌 밥·파스타 냄비는 익는 순간 신선 기한이 1일, 상하는 기한이 2일로 바뀐다.
  - "익혀야 불행이 사라지는" 재료(감자·가지·대파·호박·생선·콩 통조림 등 36종)는 익히면 불행 수치가 0이 된다(툴팁 「행복을 가져가는 악마를 없애기 위해 요리를 해 보세요.」).
- **대표 조리 시간 (기준 분 / 타는 기준 분)**: 스테이크·소고기·다진 고기·돼지갈비·소시지 50/70, 닭다리 30/60, 토끼 고기 25/70, 쥐·작은 새 고기 20/70, 생선살 20/50, 베이컨 20/50, 달걀 4/20, 감자·당근·옥수수 10/30, 열린 통조림 10/30, 빵 조각 4(→ 토스트), 수프 50/100, 스튜 70/140, 볶음·구이 60/120, 파스타·밥 20/50, 샌드위치 5/20, 따뜻한 음료 10/50, 오믈렛 10/30, 파이·케이크 40/110, 피자·빵 반죽 20/50, 머핀 30/60, 오트밀 5/30.
- **근거**: `jar:Food.update 342~483`(355~368 조리값, 372~374 오염 해제, 375~446 익음, 404~408 밥·파스타 기한, 401~419 불행 제거, 433~445 경험치 10, 447~450 탐, 454~464 화재), `jar:Food.updateTemperature 561~586`(최대 3.0), `jar:Food.DoTooltip 1309~1337`(요리 중/타는 중 막대), 1361~1370(5레벨 조리 시간), 1404~1407, `jar:Food.getName 1208~1237`, `KO/IG_UI.json` IGUI_invpanel_Cooking "요리 중"·IGUI_invpanel_Burning "타는 중", `KO/Tooltip.json` 2~8·260·411, 조리 시간은 `FOOD`·`DATA`.
- **B42**: 확인(게임 파일, 디컴파일)

### 2-2. 열원별 정리

| 열원 | 한국어 이름 | 아이콘 후보 | 필요한 것 | 단전 뒤 | 온도 → 속도(기준 대비) | 주의 |
|---|---|---|---|---|---|---|
| 오븐(가스레인지) | 「오븐」(보관함 이름), 가구 이름 「현대적인 오븐」「빨간색 오븐」 등 | UI `media/ui/Container_Oven.png` | 전기(전력망 또는 발전기, 발전기 소모 0.09) | 발전기 없으면 버튼이 안 뜸 | 온도 손잡이 0·50·100·150·200·250·300 중 100 이상에서 익음. 200 이상이면 음식 최고 온도 3.0 → **2배** | 처음 켜면 200. 타이머는 알람만 울리고 **꺼지지 않음**. 탄 음식 화재 |
| 전자레인지 | 「전자레인지」 | UI `Container_Microwave.png` | 전기 | 같음 | 손잡이 50·70·90·110·130. 50은 안 익음, 기본 100 → 1.33배, 130 → 1.53배 | **금속(냄비·팬·통조림 등 HasMetal) 넣으면 불·고장.** 날고기·생선·빵·파스타·밥·스튜 등 115종은 불행·지루함 +5 「전자레인지로 조리함」. 타이머(최대 60분)가 끝나면 꺼짐, 안 맞추면 1분 |
| 바비큐 그릴(숯) | 「바베큐 그릴 (숯)」 | UI `Container_Oven.png`(게임도 이 그림을 씀), 아이템 `Charcoal` | 땔감(숯·판자·통나무·종이 등) + 불 붙일 것 | 상관없음 | 1.8 → 1.2배 | 연료 최대 1200분 |
| 바비큐 그릴(프로판) | 「바베큐 그릴 (프로판 통)」 | 아이템 `PropaneTank` | 프로판 통(「프로판 가스통 넣기」/「프로판 가스통 빼기」) | 상관없음 | 1.8 → 1.2배 | 「켜기」/「끄기」. 통이 없으면 「프로판 가스가 담긴 통이 필요합니다.」 |
| 벽난로·난로 | 「벽난로」, 「난로」(가구 「골동품 난로」 등, 보관함 종류 woodstove) | UI `Container_Oven.png` | 땔감 + 불 | 상관없음 | 1.8 → 1.2배 | 실내용. 건축하는 「금속 통 난로」가 같은 방식인지는 미확인 |
| 모닥불 | 「모닥불」(돌 3개로 건축 메뉴에서 만듦) | UI `Container_Campfire.png`, `Build_Campfire`(UI2), 아이템 `Rock` | 땔감 + 불 | 상관없음 | 연료 3시간 이하 1.7, 그 이상 1.9 → 1.13~1.27배 | **실내면 10분마다 1/5 확률로 옆 칸 나무·카펫 바닥에 불.** 불빛·소리 반경 실외 2~10칸, 실내 2~18칸(10분마다 좀비를 부름) |
| 모닥불 구덩이 | 「모닥불 구덩이 (돌)」(석공 1), 「모닥불 구덩이 (돌 벽돌)」(석공 2) | `Build_CookingPitSimple`, `Build_CookingPit`(UI2) | 땔감 + 불 | 상관없음 | 미확인 | 툴팁 「요리와 보온을 위한 조금 고전적인 방법입니다.」 |

- 불 다루기(B42): 바비큐·모닥불·벽난로·나무 난로는 **그 가구의 보관함 창 위 버튼**으로 「떌감으로 태우기」(원문 오타 그대로) / 「모닥불 불 붙이기」 / 「모닥불 끄기」를 한다(`KO/ContextMenu.json` ContextMenu_Firetiles_tooltip "바베큐, 모닥불, 벽난로, 나무 스토브는 이제 해당 가구의 보관함 창에서 상호작용할 수 있습니다."). 오븐·전자레인지도 보관함 창의 「켜기」/「끄기」, 「설정」 버튼.
- 땔감 시간(시간 단위, 낮은 쪽이 적용될 수 있음): 통나무 6, 판자 2, 나뭇가지 1, 숯 0.5, 불쏘시개용 나무토막 0.5, 막대기 0.25. (`LUA/server/Camping/camping_fuel.lua 14~60`)
- **근거**: 오븐·전자레인지 `jar:IsoStove` 43~50(온도 상수), 81~99(전원 끊기면 꺼짐, 금속 화재), 100~136(온도 상승, 전자레인지는 즉시 최고), 253~265(금속 판정), 320~343(처음 켤 때 200/100, 전자레인지 타이머 기본 60초), 404~406(보관함 온도 = (현재+100)/100), 476~484(발전기 가능, 0.09), `LUA/client/ISUI/Fireplace/ISOvenUI.lua 122~147`, `ISMicrowaveUI.lua 91~113`, `LUA/client/ISUI/LootWindow/Handlers/StoveToggle.lua 8`·`StoveSettings.lua 8`(전원 있을 때만 버튼), `jar:Food 385~432`(전자레인지 불행·지루함). 바비큐 `jar:IsoBarbecue 44~56, 185~209, 267~272`, `LUA/client/ISUI/ISBBQMenu.lua`. 벽난로·난로 `jar:IsoFireplace 69, 172~180, 187`. 모닥불 `LUA/server/Camping/SCampfireGlobalObject.lua 114~123`(퍼지지 않는 불 오브젝트), 218~229(온도 1.7/1.9), 319~327(반경), `SCampfireSystem.lua 96~130`(실내 번짐), 173~184(10분마다), `PZ/media/scripts/generated/entities/outdoors/entity_campfire.txt`(돌 3개). 아이콘 `LUA/shared/Definitions/ContainerButtonIcons.lua 5~91`. 구덩이 `PZ/media/scripts/generated/entities/agricultural/workstations/entity_simple_cooking_pit.txt`, `entity_cooking_pit.txt`, `KO/Recipes.json` SimpleCookingPit·CookingPit·MetalBarrelOven, `KO/Tooltip.json` 452. 한국어 `KO/IG_UI.json` 213~216·517~522·1050·1063~1065·1161~1207, `KO/Moveables.json`. 보조: pzwiki Heat source(42.5.1) "Propane/Charcoal barbecue … Burning food does not spread fire", "Microwave … Metal items put inside will spread fire".
- **B42**: 확인(게임 파일, 디컴파일). 모닥불 구덩이의 온도는 미확인.

### 2-3. 익히는 순서 (사이트 그림 순서 후보)

1. 바탕에 재료를 넣는다(1장) 또는 익힐 음식(스테이크 등)을 그대로 준비한다.
2. 열원 가까이 가서 보관함 창을 열고 음식을 끌어 넣는다.
3. 오븐은 「켜기」(필요하면 「설정」으로 온도 200 이상), 바비큐·모닥불은 「모닥불 불 붙이기」(라이터·성냥 필요, 땔감 먼저).
4. 음식에 마우스를 올려 「요리 중」 막대를 본다. 다 차면 꺼낸다. 「타는 중」이 보이면 바로 꺼낸다.
5. 냄비 요리는 「음식 2그릇으로 나누기」/「음식 4그릇으로 나누기」로 그릇에 덜어 친구와 나눈다(제작법 툴팁에 「나누려면 요리해야 합니다.」라고 나온다. 익히기 전에도 막히는지는 확인 안 함).

- **근거**: 2-1·2-2 근거, `RCP/recipes_cooking.txt` 318~484(Make4Bowls·Make2Bowls, 수프·스튜·파스타·밥 냄비만), `KO/Tooltip.json` 329.
- **B42**: 확인(게임 파일)

### 2-4. 물 끓이기와 정수

- **사이트에 쓸 한 줄**: 단수 뒤 받은 빗물·강물은 냄비·주전자·머그컵에 담아 불에 올려 두면 끓어서 깨끗해진다. 플라스틱 물병은 전자레인지에서만 데울 수 있다. 「물 정수 알약」도 된다.
- 내용: 용기에 "불에 올려 데울 수 있음"(base:cookable) 태그가 있어야 한다. 요리용 냄비, 손잡이 냄비, 주전자, 머그컵, 찻잔, 그릇, 유리병, 금속 컵 등 82종. 물병·운동용 물병·플라스틱 컵 등 29종은 전자레인지 전용(base:cookablemicrowave). 온도 1.6을 넘으면 오염된 물이 조금씩 깨끗한 물로 바뀐다. 휘발유가 든 용기를 데우면 불이 난다(모닥불·벽난로 제외).
- 아이콘: `Pot`, `Kettle`, `Mugl`, `WaterPurificationTablets`
- **근거**: `jar:InventoryItem 1303~1344`, `DATA` tags(base:cookable / base:cookablemicrowave 이면서 fluid 있음), `KO/Tooltip.json` 101 "오염된 물. 마시기엔 안전하지 않습니다.<br>오븐에 넣거나 불로 끓이세요.", `RCP/recipes_medical.txt 168~186`(PurifyWater, 물 정수 알약), `KO/Recipes.json` 850 "물 정수하기".
- **B42**: 확인(게임 파일, 디컴파일)

---

## 3. 요리 기술 (Cooking, 「요리」)

### 3-1. 레벨별 효과

- **사이트에 쓸 한 줄**: 요리 레벨이 오르면 같은 재료로 더 많이·더 맛있게 만든다. 7레벨부터는 상한 재료도 조금 쓸 수 있다.

| 효과 | 내용 | 근거 |
|---|---|---|
| 재료 덜 씀 | 재료가 줄어드는 양 = 괄호 숫자 × (1 − 0.03×레벨). 0레벨 100% → 5레벨 85% → 10레벨 70% | `jar:EvolvedRecipe 391` |
| 열량 증가 | 더해지는 열량·영양 × (1 + 레벨/15), 다만 쓴 비율이 줄어 실제로는 10레벨에 약 117% | `jar:EvolvedRecipe 398~402`, pzwiki Cooking(42.18.0) 표와 일치 |
| 행복 보너스 | 0레벨은 재료 4개째부터 보너스가 사라짐. 3레벨부터는 6개까지 재료마다 불행 −5 | `jar:EvolvedRecipe 388~397` |
| 상한 재료 | 7레벨부터 넣을 수 있음. 7~8레벨은 원래 배고픔의 5%, 9~10레벨은 10%만 더해지고 재료는 통째로 없어짐. 상한 양념도 7레벨부터 | `jar:EvolvedRecipe 222~233, 356~365, 546~554`, `jar:RecipeManager 424` |
| 양념 | **레벨 제한 없음**(코드상). 상한 양념만 7레벨 | `jar:EvolvedRecipe 213~226` |
| 조리 시간 표시 | 5레벨부터 음식 툴팁에 「조리 시간 (분)」 | `jar:Food 1361~1370` |
| 독 알아보기 | 다른 사람이 독을 넣은 요리 등: 요리 레벨 ≥ 10 − 독 감지 수치이면 「(독)」 표시. 야생 버섯·산딸기는 요리 레벨과 무관하게 **약초꾼 제작법**(「약초꾼」 특성, 「잡지: 약초꾼들」)이 있어야만 알아봄 | `jar:IsoGameCharacter.isKnownPoison 10831~10852`, `FOOD` HerbalistType(버섯·산딸기 18종), `LUA/shared/Foraging/Categories/Mushrooms.lua 5~12`·`Berries.lua 5~60` |
| 재료 넣는 시간 | 100틱 − 레벨×2.5틱 | `LUA/shared/TimedActions/ISAddItemInRecipe.lua 225~229` |
| 칼로 통조림 열기 | 요리 0레벨이고 단검 기술 3 이하면 손 다칠 확률이 조금 더 높음(기본 약 20% → 25%) | `jar:RecipeCodeOnCreate 640~679` |
| 보존식 병뚜껑 | 「병에 담긴 보존식 만들기」에서 레벨이 높을수록 뚜껑이 덜 상함 | `jar:RecipeCodeOnCreate 283~291` |

- 독 넣기: 서버 기본값 `EnablePoisoning = 1`(켜짐)이라, 재료가 3개 이상 들어간 요리에는 독(알고 있는 독 아이템)을 넣을 수 있다(`jar:EvolvedRecipe 166~181`, `jar:EvolvedRecipe.addPoison 503~536`). 친구끼리라도 남이 준 요리는 조심. 사이트에는 넣지 않아도 된다.
- **B42**: 확인(디컴파일)

### 3-2. 경험치 얻는 법

- **사이트에 쓸 한 줄**: 요리에 재료를 넣을 때(3), 음식이 다 익었을 때(10), 제작창 요리 제작법(3~20)으로 오른다. 기본 배율이 25%라 요리책을 먼저 읽자.
- 내용
  - 진화형 요리에 재료 하나 넣을 때 +3(양념 포함).
  - 음식이 익는 순간, 그 음식을 열원에 넣은 사람(chef)에게 +10. 탄 음식·상한 음식·NoCookingXP 태그는 제외.
  - 제작창 요리 제작법의 xpAward: 빵 자르기·햄 자르기 등 3, 반죽 만들기 10, 닭·칠면조 자르기 20(4장 표).
  - 배율: 직업·특성으로 받은 요리 보너스가 없으면 ×0.25, +1 ×1, +2 ×1.33, +3 이상 ×1.66. 「현자」 ×1.3, 「손재주꾼」 ×1.3(요리는 제작 분류), 「느린 학습」 ×0.7. 그다음 요리책 배율(1권 ×3, 2권 ×5, 3권 ×8, 4권 ×12, 5권 ×16, 각 2레벨 구간)과 샌드박스 경험치 배율이 곱해진다.
  - 요리책: 「요리 1권: "더 나은 햄버거 조리법"」~「요리 5권: "뤼방 베르 고메 - 요리 기술 총집합본"」(아이콘 `Book9` 등). 우리 서버는 책이 거의 바로 읽힌다(`docs/research/tips.md` 기준과 표기).
  - TV "Life and Living" 의 요리 프로그램, 요리 VHS 도 경험치를 준다(pzwiki Cooking 42.18.0, 첫 3레벨까지).
- **근거**: `jar:EvolvedRecipe 463~467`(+3), `jar:Food 433~445`(+10), `LUA/client/TimedActions/ISInventoryTransferAction.lua 670~673`(음식을 옮긴 사람을 chef 로 기록), `RCP/*.txt` xpAward, `jar:IsoGameCharacter 15616~15665`(배율), `LUA/server/XpSystem/XPSystem_SkillBook.lua 35~41`, `KO/ItemName.json` 178~182, `KO/UI.json` 235 "현자", 263 "느린 학습", 1562 "손재주꾼".
- **B42**: 확인(디컴파일). 단 멀티에서는 서버가 chef 를 계정 이름(username)으로 찾는데(`jar:GameServer.getPlayerByUserNameForCommand 2203~2213`) 옮길 때 기록되는 값은 캐릭터 이름(getFullName)이라, **익힐 때 +10이 멀티에서 실제로 들어오는지는 미확인**(안 들어올 가능성이 있다). 재료 넣을 때 +3과 제작법 경험치는 서버가 직접 준다.

### 3-3. 「열정적인 요리사」와 요리 직업

- **사이트에 쓸 한 줄**: 「열정적인 요리사」(3점)는 요리 +2(경험치 1.33배), 도축 +1, 그리고 빵·파이·케이크·쿠키·피자 반죽 등 15가지 제작법을 처음부터 안다.
- 내용
  - 특성 `base:cook` 「열정적인 요리사」: 비용 3, 요리 +2·도축 +1, 제작법 15개(케이크 반죽, 파이 반죽, 빵 반죽, 바게트, 비스킷, 초콜릿 칩·오트밀·쇼트브레드·설탕 쿠키, 피자, 튀김옷 입힌 어니언 링, 새우튀김, 양배추 롤, 병에 담긴 보존식, 과카몰레). 설명 「다양한 요리 레시피를 알고 있습니다.」
  - 직업 「주방장」: 요리 +4(×1.66), 도축 +2, 정비 +1, 단검 +1, 제작법 20개(위 목록 + 초콜릿 쿠키, 초밥·김초밥·주먹밥, 머핀).
  - 직업 「햄버거 조리사」: 요리 +2, 정비 +1, 단검 +1. 같은 이름의 직업 특성(`base:cook2`)을 받지만 이 특성에는 제작법이 없다 → **반죽류 제작법은 못 받는다.**
  - 「열정적인 요리사」와 직업 특성은 같이 고를 수 없다.
- **근거**: `PZ/media/scripts/generated/characters/character_traits.txt 180~202`, `character_professions.txt 14~43`, `KO/UI.json` 135 "주방장", 144 "햄버거 조리사", 327~330. 보조: pzwiki Cooking(42.18.0) "Keen Cook (+2)", "Burger Flipper (+2)", "Chef (+4)".
- **B42**: 확인(게임 파일)

---

## 4. 제작창(B)의 요리 제작법

- **사이트에 쓸 한 줄**: 제작창 「요리」 탭에는 통조림 열기, 빵 자르기, 냄비에 파스타·쌀 넣기, 그릇에 나누기 같은 기본 작업이 있다. 대부분 배울 필요 없고, 반죽·빵·피자·보존식만 배워야 한다.
- 42.21 의 Cooking 분류 craftRecipe 는 86개다. 처음 하는 사람에게 쓸모 있는 것만 골랐다. "섞는 도구" = 포크·숟가락·뒤집개 등(base:mixingutensil), "날카로운 칼" = 부엌칼·사냥칼·과도 등(base:sharpknife), "깡통 따개" = 깡통 따개·P38·멀티툴 등(base:canopener).

| 제작법 (한국어) | id | 재료 | 도구(남음) | 결과 | 경험치 | 배워야 함 |
|---|---|---|---|---|---|---|
| 통조림 열기 | `OpenCannedFood` | 통조림 1 (콩·옥수수·참치·수프 등 17종) | 깡통 따개 | 열린 통조림 | - | 아니오 |
| 날붙이로 통조림 열기 | `OpenCannedFoodWithKnifeOrSharpStoneFlake` | 통조림 1 | 날카로운 칼(닳음) 또는 날카로운 부싯돌 조각 | 열린 통조림 (손 다칠 수 있음, 「날이 손상됩니다. 손을 다칠 수 있습니다.」) | - | 아니오 |
| 고리 달린 통조림 열기 | `OpenCannedFood2` | 염장 소고기·정어리 통조림 | 없음 | 열린 통조림 | - | 아니오 |
| 빵 자르기 | `SliceBread` | 빵 또는 바게트 1 | 무딘 칼·날카로운 칼·고기 써는 칼 | 빵 조각 3 | 요리 3 | 아니오 |
| 요리용 냄비에 파스타 넣기 | `PlacePastaInCookingPot2` | 요리용 냄비, 물 1.5L, 파스타 10 | - | 요리용 냄비 [파스타] | - | 아니오 |
| 냄비에 쌀 넣기 | `PlaceRiceInCookingPot2` | 요리용 냄비, 물 1.5L, 쌀 10 | - | 요리용 냄비 [쌀] | - | 아니오 |
| 손잡이 냄비에 파스타/쌀 넣기 | `PlacePastaInSaucepan2` / `PlaceRiceInSaucepan2` | 손잡이 냄비, 물 0.6L, 파스타/쌀 10 | - | 손잡이 냄비 [파스타]/[쌀] | - | 아니오 |
| 음식 2그릇/4그릇으로 나누기 | `Make2Bowls` / `Make4Bowls` | 그릇 2/4, 익힌 수프·스튜·파스타·밥 냄비 | - | 그릇 [스프] 등 + 빈 냄비 | - | 아니오 |
| 그릇에 콩 담기 | `MakeBowlOfBeans` | 그릇, 열린 콩 통조림 | - | 그릇 [콩] | 요리 3 | 아니오 |
| 그릇에 오트밀 담기 | `MakeBowlOfOatmeal` | 그릇, 물 0.3L, 오트밀 통조림 10 | - | 오트밀(진화형 바탕) | 요리 3 | 아니오 |
| 그릇에 시리얼 담기 | `MakeBowlOfCereal` | 그릇, 우유 0.3L, 시리얼 5 | - | 그릇 [시리얼] | 요리 3 | 아니오 |
| 오믈렛 준비하기 | `PrepareOmelette` | 프라이팬, 날달걀 2 | 섞는 도구 | 오믈렛(진화형 바탕, 익혀야 함) | 요리 3 | 아니오 |
| 팬케이크 준비하기 | `MakePancake` | 물 0.3L, 팬케이크 믹스 | 섞는 도구, 그릇 | 팬케이크 | 요리 3 | 아니오 |
| 핫도그 준비하기 | `MakeHotDog` | 핫도그 빵, 핫도그 소시지 | - | 핫도그 | - | 아니오 |
| 달걀곽 열기 | `OpenEggCarton` | 달걀곽 | - | 달걀 12 | - | 아니오 |
| 햄 자르기 | `SliceHam` | 햄 | 날카로운 칼·고기 써는 칼 | 햄 조각 6 | 요리 3 | 아니오 |
| 닭 자르기 | `CutChicken` | 통 닭고기 | 날카로운 칼·고기 써는 칼 | 닭다리·닭날개·닭가슴살 각 2 | 요리 20 | 아니오 |
| 생선에서 살 바르기 | `SliceFillet` | 생선 | 날카로운 칼·고기 써는 칼 | 생선살 2 | 도축 10 | 아니오 |
| 작은 동물 도축하기 | `ButcherSmallAnimal` | 죽은 새·쥐·청설모·생쥐·개구리·토끼 | 날카로운 칼·고기 써는 칼 | 고기 | 도축 10 | 아니오 |
| 고기 패티 만들기 | `MakeMeatPatty` | 다진 고기 40 | - | 고기 패티 | 요리 3 | 아니오 |
| 병에 담긴 보존식 열기 | `OpenJarOfFood` | 보존식 병 | - | 내용물 | - | 아니오 |
| 빵 반죽 준비하기 | `MakeBreadDough` | 밀가루 10, 소금 2, 효모 1, 물 1L | 섞는 도구, 그릇, 밀대 | 빵(반죽, 진화형 바탕) | 요리 10 | **예** (요리 7 자동, 잡지 「훌륭한 요리 - 1993년 5월호」) |
| 파이 반죽 준비하기 | `MakePieDough` | 밀가루 10, 버터·라드·마가린 1, 소금 2, 물 2L | 밀대, 섞는 도구, 그릇 | 파이 반죽 | 요리 10 | **예** (요리 7, 잡지 「훌륭한 요리 - 1993년 6월호」) |
| 피자 준비하기 | `MakePizza` | 밀가루 6, 소금 1, 치즈 15, 피자 소스 15, 효모 1, 물 0.5L | 밀대, 섞는 도구, 그릇 | 피자(진화형 바탕) | 요리 10 | **예** (요리 6, 잡지 「이탈리아의 맛」) |
| 병에 담긴 보존식 만들기 | `MakeJar` | 유리병, 유리병 뚜껑, 채소 6(종류별 개수 다름), 식초 2, 소금 1, 물 0.5L | 칼 | 채소 보존식 병(오래 감) | 요리 10 | **예** (요리 8, 잡지 「미국식 자급자족」) |
| 물 정수하기 (기타 분류) | `PurifyWater` | 물이 든 용기, 물 정수 알약 | - | 깨끗한 물 | - | 아니오 |

- 배우는 법 정리: 「열정적인 요리사」·「주방장」으로 시작하거나, 잡지(「잡지: 훌륭한 요리 - 1993년 6월호/5월호」, 「이탈리아의 맛」, 「할머니의 주방」(쿠키 5종), 「세계의 음식」(초밥 3종), 「맛있는 식사 - 1993년 6월호」(새우튀김·어니언 링·양배추 롤·과카몰레), 「미국식 자급자족」(보존식))를 읽거나, 요리 레벨이 오르면 자동(반죽·쿠키·머핀 7, 피자·초밥·튀김·양배추 롤·과카몰레 6, 보존식 8). 머핀은 가르치는 잡지가 없다(주방장이나 요리 7).
- 아이콘: `CanOpener`, `KnifeChopping`, `BreadSlices`, `Pot_Water`, `BowlFull`, `Egg`, `HamSlices`, `ChickenWhole`, `FishFillet`, `MagazineFood`~`MagazineFood6`(잡지)
- **근거**: `RCP/recipes_cannedFood.txt` 107·145·183, `RCP/recipes_baking.txt` 84·150·176, `RCP/recipes_cooking.txt` 63·191·209~300·318~484·508·536·555·574·645·683·701·821·841·1073·1128, `RCP/recipes_jarring.txt` 3·32, `RCP/recipes_medical.txt 168`, 한국어 `KO/Recipes.json`, 잡지 `PZ/media/scripts/generated/items/literature.txt 5218~5300, 5488`(LearnedRecipes), 자동 습득 각 레시피의 `AutoLearnAny`, 칼 다침 `KO/Tooltip.json` Tooltip_Recipe_OpenCanWithKnife. 태그 목록 `DATA` tagItems. 파스타·쌀 "10"은 봉지(배고픔 60)에서 배고픔 10만큼을 쓰는 것으로 보인다(냄비 [파스타] 배고픔 10과 일치, 추정).
- **B42**: 확인(게임 파일)

---

## 5. 음식 보관과 상함

- **사이트에 쓸 한 줄**: 음식은 「신선한」 → 「신선하지 않은」 → 「상한」 순서로 변한다. 냉장고에 넣으면 5배 오래 가고, 냉동고에 얼리면 멈춘다. 전기가 끊기면 둘 다 소용없다. 안 딴 통조림은 영원히 간다.

| 상태 | 배고픔 | 불행·지루함 | 그 밖 |
|---|---|---|---|
| 신선한 (DaysFresh 전) | 그대로 | 그대로 | |
| 신선하지 않은 | ÷1.3 | +10, +10 | 스트레스 효과 ÷1.3 |
| 상한 (DaysTotallyRotten 뒤) | ÷2.2 | +20, +20 | **먹으면 식중독**: 썩은 정도에 따른 확률로 독 5×(배고픔×10), 아니면 2×(배고픔×10) |
| 데운(익힌) | ×1.3 | (따뜻할 때 GoodHot −2) | 지구력 ×2, 배부를 때 먹으면 "음식으로 회복" 시간 2배 |
| 타 버린 | ÷3 | +20, +20 | |
| 냉동된 | 그대로 | +30, +30 (아이스크림 등 예외) | 요리 재료로 못 넣음 |
| 날것 위험(DangerousUncooked) | | | 「요리되지 않아 식중독 위험이 있습니다.」 먹으면 독 +15(먹은 양 비례), "음식으로 회복" 시간 0. 달걀은 「데우지 않은 상태로 먹으면 질병이나 메스꺼움을 유발할 수 있습니다.」(강철 위장이면 달걀은 괜찮음) |

- 따뜻한 음식(GoodHot, 148종): 익혀서 따뜻할 때(온도 1.3 초과) 먹으면 불행 −2. 차가운 음식 페널티(BadCold, 61종: 고기·생선·스튜·파스타 등): 익힌 뒤 식으면 불행 +2. 식으면 툴팁 「따뜻하게 먹는 것이 더 좋습니다.」 (값이 작아서 사이트에서는 "따뜻하게 먹으면 조금 더 좋다" 정도)
- 냉장고·냉동고: 전기(전력망 또는 발전기)가 있을 때 냉장고·냉동고 안 음식은 상하는 속도 ×0.2(기본 샌드박스 FridgeFactor 3). 냉동고에서 얼 수 있는 음식은 4시간이면 얼고, 언 동안은 전혀 안 상한다. 밖에 꺼내면 1.5시간이면 녹는다(따뜻한 곳에서는 더 빨리, 전기 들어오는 냉장고 안에서는 2배 느리게).
- 단전: 기본 샌드박스는 14~30일 사이 어느 날 전기가 끊긴다. 그 뒤로는 냉장고 안 음식도 보통 속도로 상하고, 냉동고 음식은 녹기 시작한다. 오븐·전자레인지도 못 쓴다. 미리 통조림·보존식으로 바꾸거나 발전기를 준비한다.
- 통조림: 안 딴 통조림은 신선 기한이 없다(안 상함). 따면 2~3일 신선, 4~5일이면 상함(옥수수 통조림 [열림] 2/4, 볼로네제 3/5). 따는 법은 4장.
- 보존식 병(「병에 담긴 보존식 만들기」, 배워야 함)으로 채소를 오래 둘 수 있다.
- 요리와 신선도: 냄비·그릇으로 만든 요리는 새 음식이라 신선하다(수프·스튜 3일 신선/5일 상함, 샐러드 2/3, 볶음 3/5). 익힌 밥·파스타는 1일/2일로 짧아진다. 샌드위치는 빵의 나이를 이어받는다.
- 소금: 42.21 에는 소금으로 고기를 절여 오래 두는 제작법이 없다. 소금은 요리 양념, 빵·파이 반죽, 보존식 재료로 쓰인다(→ 미확인 아님, 스크립트 검색 결과 없음).
- 특성: 「강철 위장」은 식중독 독 ÷2(날달걀은 0), 「소화불량」은 ×2. 「영양사」는 모든 음식의 열량·영양을 툴팁에서 본다(포장 음식은 글을 읽을 수 있으면 누구나).
- **근거**: `jar:Food.getHungerChange 1517~1536`, `getUnhappyChange 1466~1492`, `getBoredomChange 1495~1515`, `getEnduranceChange 1448~1459`, `getStressChange 1539~1556`, `DoTooltip 1371~1411`, `getFridgeFactor 642~651`, `getFoodRotSpeed 653~661`, `updateAge 668~712`(냉장 ×0.2, 단전 뒤 정상, 냉동 ×0), `updateFreezing 752~773`(4시간/1.5시간), `isFreezing/isThawing 1990~2007`, `jar:BodyDamage.JustAteFood 527~642`(독·식중독·회복 시간), `FOOD`(GoodHot 148, BadCold 61, DangerousUncooked 81, RemoveUnhappinessWhenCooked 36, BadInMicrowave 115 — 개수는 직접 셈), `DATA`(통조림 daysFresh 없음), `KO/Tooltip.json` 2~8·16·160·301, `Apocalypse.lua`(FridgeFactor 3, FoodRotSpeed 3, ElecShut 2, ElecShutModifier 14), `KO/Sandbox.json` 643 "14일-30일", `KO/UI.json` 299 "소화불량", 301 "강철 위장", 324 "영양사". 냉장 5배는 `docs/research/tips.md` 4-4 와 일치.
- **B42**: 확인(게임 파일, 디컴파일)

---

## 6. 쉬운 추천 요리

- 계산 방법: 1-4 의 식을 그대로 옮긴 스크립트로 냈다(요리 0레벨, 재료 모두 신선, 양념 없음). "배고픔"은 툴팁에 보이는 값(익히는 요리는 익힌 뒤 ×1.3). 불행은 음수일수록 기분이 좋아진다. 재료의 괄호 숫자는 `FOOD` 의 EvolvedRecipe 값.
- 비교 기준: 같은 재료를 따로 날로 먹으면 괄호 숫자 합만큼만 배가 부르고 행복 보너스가 없다(감자는 날로 먹으면 오히려 불행 +5).

| # | 요리 | 바탕 + 재료 (아이콘) | 배고픔 | 불행 | 열량 | 그 밖 | 왜 좋은가 |
|---|---|---|---|---|---|---|---|
| 1 | 채소 수프 | `Base.Pot`(물 가득, `Pot`) + 당근(8) `Carrots`, 감자(18) `Potato`, 양배추(12) `Cabbage`, 토마토(12) `Tomato` | **65** (날로 먹으면 50) | −15 | 199 | 갈증 −64, 3일 신선, 양배추 절반 남음 | 집집마다 있는 채소로 바로. 신선하지 않은 채소도 새 수프가 된다. 4그릇으로 나눠 먹기 좋다 |
| 2 | 통조림 스튜 | `Base.Pot`(물 가득) + 볼로네제(24) `CannedBologneseOpen`, 옥수수(16) `CannedCornOpen`, 감자(18) `CannedPotatoOpen`, 토마토 통조림(12) `CannedTomatoOpen` | **91** | −15 | **1120** | 갈증 −59 | 통조림은 안 따면 안 상해서 쌓아 두기 좋다. 한 냄비로 하루 열량의 큰 몫 |
| 3 | 고기 채소 볶음 | `Base.Pan`(`Pan`) + 스테이크(20) `Steak`, 감자(18), 당근(8), 토마토(12) | **75** | −15 | 219 | 반드시 익힘(60/120), 스테이크 절반 남음 | 금방 상하는 생고기를 빨리 처리 |
| 4 | 햄 치즈 샌드위치 | `Base.BreadSlices`(`BreadSlices`) + 햄 조각(10) `HamSlices`, 치즈(5) `Cheese`, 양상추(3) `Lettuce` | 28 (데우면 36) | −15 | 485 | 불 없이 가능 | 불·전기 없이 바로. 데우면 더 든든 |
| 5 | 채소 샐러드 | `Base.Bowl`(빈 그릇, `Bowl`) + 양상추(5), 토마토(6), 당근(4), 양배추(12) | 27 | −15 | 128 | 2일 신선 | 불 없이 기분 회복. 단 배는 덜 찬다 |
| 6 | 과일 샐러드 | `Base.Bowl` + 사과(8) `Apple`, 바나나(8) `Banana`, 오렌지(6) `Orange`, 배(8) `Pear` | 30 | −15 | 170 | 2일 신선 | 과일이 상하기 전에 한 번에 |
| 7 | 볼로네제 파스타 | `Base.Pot` + 물 1.5L + 파스타 → 「요리용 냄비 [파스타]」(`Pot_Water`) + 볼로네제(24), 토마토(12), 치즈(10) | **72** | −15 | **1189** | 익힌 뒤 1일 신선, 따뜻하게 먹으면 불행 −2 | 열량이 가장 높다. 익힌 파스타는 금방 상하니 4그릇으로 나눠 바로 먹는다 |

- 레벨이 오르면: 3레벨 이상이면 재료 6개짜리 수프(당근·감자·양배추·토마토·대파·양파)가 배고픔 87, 불행 −30이 된다(0레벨은 같은 수프가 불행 0). 10레벨이면 같은 4재료 수프의 열량이 232로 오르고 재료는 70%만 줄어든다(감자가 5.4만큼 남음).
- 양념: 소금·후추를 하나씩 넣으면 불행·지루함이 각각 2씩 더 준다. 버터(4)는 8.
- 재료 넣을 때마다 요리 경험치 3, 다 익으면 10(4재료 수프 = 22, 경험치 배율 적용 전).
- **근거**: 계산식 `jar:EvolvedRecipe.addItem 265~469`, `jar:Food.getHungerChange 1517~1536`, 재료 값 `FOOD`(Carrots Soup:8, Potato Soup:18, Cabbage Soup:12, Tomato Soup:12, CannedBologneseOpen Stew:24, Steak Stir fry:20, HamSlice Sandwich:10, Cheese Sandwich:5, Lettuce Sandwich:3·Salad:5, Apple FruitSalad:8 등), 바탕 값 `DATA`(BreadSlices 배고픔 10·열량 177, WaterPotPasta 배고픔 10·열량 560), 신선 기한 `DATA`·`jar:Food 404~408`.
- **B42**: 확인(코드로 계산). 게임 안에서 실측하지는 않았다.

---

## 7. 그림(아이콘) 후보

모두 `web/public/icons/item/<이름>.webp` 에 있다(존재 확인함). 사이트에서는 아이템 id 로 `items-detail.json` 의 `icon` 을 쓰면 된다.

- 바탕(기본 아이템): `Base.Pot` `Pot`, `Base.Pan` `Pan`, `Base.Bowl` `Bowl`, `Base.BreadSlices` `BreadSlices`, `Base.Mugl` `Mugl`, `Base.RoastingPan` `Roastingpan`, `Base.Saucepan` `SaucepanEmpty`, `Base.Kettle` `Kettle`, `Base.BunsHamburger_single` `BunsHamburger_single`, `Base.Baguette` `Baguette`, `Base.TacoShell` `TacoShell`, `Base.Tortilla` `Tortilla`, `Base.WaterPotPasta`/`WaterPotRice` `Pot_Water`, `Base.Bucket` `MetalBucket`
- 결과(요리): 수프·스튜·파스타·밥 냄비 `PotFull`, 양동이 수프 `MetalBucket_Soup`, 단조 냄비 `Pot_Forged_Soup`·`Pot_Forged_Stew`, 볶음 `PanFull`, 구이 `RoastingpanFull`, 샐러드 `TZ_CraftSalat`, 과일 샐러드 `FruitSalad`, 샌드위치 `Sandwich`, 바게트 샌드위치 `BaguetteSandwich`, 햄버거 `Burger`, 음료 `MugFulll`, 타코 `Taco`, 부리토 `Burrito`, 파이 `PieWhole`, 케이크 `Cake`, 피자 `PizzaWhole`, 토스트 `Toast`, 오트밀 `Oatmeal`, 핫도그 `HotdogCrafted`, 팬케이크 `PancakesFruit`, 와플 `SafflesFruit`, 아이스크림 콘 `ConeIceCreamTopped`, 머핀 `Muffintray_Batter`, 빵 반죽 `Dough`
- 그릇에 나눈 것: 그릇 [스프]·[스튜]·[콩]·[라면] `BowlFull`, 그릇 [밥]·[파스타] `FriedRice`
- 재료(추천 요리): `Carrots`, `Potato`, `Cabbage`, `Tomato`, `Onion`, `Leek`, `Lettuce`, `Steak`, `Chicken`, `HamSlices`, `Cheese`, `Egg`, `Apple`, `Banana`, `Orange`, `Pear`, `CannedBologneseOpen`, `CannedCornOpen`, `CannedPotatoOpen`, `CannedTomatoOpen`, `CannedPeasOpen`, `CannedCarrotsOpen`, `BeansOpen`, `TunaOpen`, `SpagettiRaw`(파스타), `RiceRaw`(쌀), `Bread`, 양념 `Salt`·`Pepper`
- 도구·연료: `CanOpener`(깡통 따개), `KnifeChopping`(부엌칼), `Fork`, `Spoon`, `Spork`, `Lighter`, `Matches`, `Matchbox`, `BBQLighter`, `Charcoal`, `PropaneTank`, `Logs`, `Plank`, `Branch`, `Rock`(모닥불 돌), `DryFirestarterBlock`, `Generator`, `WaterPurificationTablets`, `OvenMitt`
- 책·잡지: `Book9`(요리 1권), `MagazineFood`~`MagazineFood6`
- 열원(가구) — 저장소에 없음, 게임 UI 텍스처에서 뽑아야 함: 오븐·바비큐·벽난로·난로 `media/ui/Container_Oven.png`, 전자레인지 `Container_Microwave.png`, 모닥불 `Container_Campfire.png`, 냉장고 `Container_Fridge.png`, 냉동고 `Container_Freezer.png`(이상 UI.pack/UI2.pack), 건축 메뉴 그림 `Build_Campfire`, `Build_CookingPit`, `Build_CookingPitSimple`, `Build_BarrelOven`(UI2.pack). 타일 스프라이트로는 전자레인지 `appliances_cooking_01_24`, 모닥불 `camping_01_6`.
- **근거**: `DATA` 의 각 아이템 `icon`, `LUA/shared/Definitions/ContainerButtonIcons.lua 5~91`, `PZ/media/scripts/generated/items/moveable.txt 1308~1315`, 텍스처 목록(UI.pack·UI2.pack 이름 목록).
- **B42**: 확인(게임 파일)

---

## 8. 확인 못 한 것

- 멀티에서 "음식이 익을 때 +10 경험치"가 실제로 들어오는지(서버는 계정 이름으로 찾고, 기록되는 값은 캐릭터 이름이라 안 들어올 수 있음).
- 열원별 실제 조리 분(예열·음식이 데워지는 시간 포함). 위의 속도 배수는 코드상 최고치다.
- 모닥불 구덩이(돌/돌 벽돌)·금속 통 난로의 온도.
- 오븐 온도 손잡이 눈금이 화면에서 °F/°C 로 몇 도인지(손잡이 배경 텍스처를 열어 보지 않음). 내부 값 0~300 중 100 이상이면 익는다는 것만 확인.
- 「음식 4그릇으로 나누기」로 나눴을 때 한 그릇 수치(InheritFood 분배 방식). 대략 1/4로 보이지만 실측 안 함. 익히기 전 냄비도 나눌 수 있는지(툴팁은 "요리해야 한다"인데 스크립트에 검사 조건이 안 보임).
- 파스타·쌀 "10"이 배고픔 10만큼이라는 해석(추정).
- 42.21 의 고유 요리(UniqueRecipe) 목록과 보너스.
- 전력망이 끊긴 뒤 발전기로 돌리는 오븐에서도 탄 음식 화재가 나는지(코드가 `hasGridPower` 를 보는데 발전기를 포함하는지 확인 안 함).
- 도자기 찻잔 음료·단조 프라이팬 오믈렛 메뉴의 한국어 문구(키 없음/불일치).
- 우리 서버의 통합 번역 모드를 쓰면 메뉴 문구가 바닐라 `KO/` 와 다를 수 있다. 사이트에 문구를 넣기 전에 게임 화면에서 한 번 맞춰 보는 것이 좋다.
- 1·2레벨에서 5·6번째 재료가 큰 행복 보너스를 주는 계산 결과(코드상, 실측 안 함). 사이트에는 "3레벨부터 재료 6개까지 보너스"로만 쓰는 것을 권한다.
