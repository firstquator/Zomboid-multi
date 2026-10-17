# 차량 사용법 조사 (42.21, 2026-10-18 확인)

사이트 "차량 사용법" 섹션에 쓸 사실과 근거를 정리한다. 항목마다 **사이트 한 줄**(그대로 옮겨 쓸 수 있는 쉬운 문장), **근거**, **그림 후보**를 적는다. 그림 후보 전체 목록은 맨 아래 "그림 후보" 표에 있다.

## 기준과 근거 표기

- 게임 빌드: **42.21.0**. 이 PC 의 `%USERPROFILE%\Zomboid\version.txt` 와 `console.txt` 에서 확인했다.
- `<게임>` 은 `C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid` 를 줄인 것이다.
- 근거 표기
  - `[Lua]` 게임 Lua 파일과 줄 번호. 예: `<게임>\media\lua\shared\keyBinding.lua:104`
  - `[스크립트]` `<게임>\media\scripts\generated\...` 의 txt 와 줄 번호
  - `[번역]` `<게임>\media\lua\shared\Translate\KO\*.json` 의 키
  - `[Java]` `<게임>\projectzomboid.jar` 의 클래스와 함수. CFR 0.152 로 디컴파일해서 읽었다. 디컴파일 줄 번호는 원본과 달라서 함수 이름으로 적는다.
  - `[모드]` 이 PC 에 받아진 창작마당 모드 파일. `[웹]` 창작마당·PZwiki·Reddit 글(보조 근거)
- 커뮤니티 글과 게임 파일이 다르면 게임 파일을 따랐다. B41 자료는 쓰지 않았고, 쓸 때는 "B41 자료"라고 적었다.

## 0. 우리 서버의 샌드박스 기본값은 Apocalypse 프리셋 값이다

**사이트 한 줄**: (사이트에는 안 써도 됨. 아래 확률 계산의 전제)

우리 서버는 차량 관련 샌드박스 값을 건드리지 않는다. 그런데 "기본값"이 두 가지라서 먼저 정리한다.

- Java 코드의 기본값: `[Java] zombie.SandboxOptions` 필드 선언(`newEnumOption("CarSpawnRate", 5, 4)` 등).
- 게임이 실제로 쓰는 기본값: `[Lua] <게임>\media\lua\shared\Sandbox\SandboxVars.lua:1-4` 가 `SandboxVars = require "Sandbox/Apocalypse"` 를 읽고 `getSandboxOptions():initSandboxVars()` 를 부른다. `initSandboxVars` 는 이 Lua 표의 값을 Java 옵션에 넣는다(`[Java] SandboxOptions.initSandboxVars`: `option.fromTable(vars)`).
- 호스트 서버도 이 순서를 따른다. `[Java] zombie.network.GameServer` 가 `LuaManager.LoadDirBase("shared")` 를 먼저 하고, 그 다음에 `<서버이름>_SandboxVars.lua` 를 읽거나 새로 쓴다. `[Java] SandboxOptions.readLuaFile` 은 파일에 있는 키만 바꾸고 기본값으로 되돌리지 않는다.
- 그래서 **우리 서버에서 설치 스크립트가 안 쓰는 키는 Apocalypse 프리셋 값**이 된다. 이 PC 에서 서버가 처음 만든 파일의 `ZombieRespawn = 4`(`docs/research/hosting.md:238`)가 Java 기본값(2)이 아니라 Apocalypse 값(4)과 같아서, 이 판단과 맞는다.

차량 관련 키 중 두 기본값이 다른 것은 6개다. 아래 확률은 모두 **Apocalypse 값(우리 서버)** 으로 계산했다.

| 키 | 우리 서버(Apocalypse) | Java 기본값 | 근거 |
|---|---|---|---|
| `KeyLootNew` | 0.4 | 0.6 | `Apocalypse.lua:36`, `SandboxOptions` 141행 선언 |
| `CarSpawnRate` | 3 (보통) | 4 (많음) | `Apocalypse.lua:108`, 선언 214행 |
| `InitialGas` | 2 (적음) | 3 (보통) | `Apocalypse.lua:111`, 선언 217행 |
| `FuelStationGasMax` | 0.8 | 0.7 | `Apocalypse.lua:114`, 선언 220행 |
| `CarAlarm` | 3 (적음) | 4 (보통) | `Apocalypse.lua:122`, 선언 228행 |
| `RecentlySurvivorVehicles` | 2 (적음) | 3 (보통) | `Apocalypse.lua:126`, 선언 232행 |

(`Apocalypse.lua` 는 `<게임>\media\lua\shared\Sandbox\Apocalypse.lua`. 선언 행은 디컴파일한 `SandboxOptions.java` 기준.)

- 커뮤니티 계산(Reddit 2026-10-07, 아래 8절)은 열쇠 확률을 15% 로 잡았는데, 이것은 Java 기본값 0.6 기준이다. 우리 서버는 10% 다.

## 1. 기본 키 설정

**사이트 한 줄(요약)**: 차 옆에서 **E** 로 타고 내리고, **N** 으로 시동, **W·A·S·D** 로 운전, **Space** 브레이크, **V** 를 누르고 있으면 차량 메뉴가 뜬다.

| 동작 | 기본 키 | 게임 설정 화면 이름 | 근거 |
|---|---|---|---|
| 타기 / 내리기, 차 옆에서 문·후드·트렁크 열기 | E | 상호작용 | `[Lua] keyBinding.lua:32-33`. E 를 누르면 `[Java] IsoPlayer.enterExitVehicle` 이 `OnUseVehicle` 을 보내고, `[Lua] media\lua\server\Vehicles\Vehicles.lua:1341-1354` 가 타기·내리기 또는 가까운 부품(문·후드·트렁크) 사용을 고른다. `[번역] UI.json:433` |
| 앞으로 / 뒤로 / 방향 | W / S / A / D | 앞으로 이동 / 뒤로 이동 / 왼쪽으로 이동 / 오른쪽으로 이동 | `[Lua] keyBinding.lua:13,17,21,25`, `[번역] UI.json:427-430`. 달리는 중 S 는 먼저 브레이크, 멈춘 뒤 후진(`[Java] CarController` 175-183행). W 와 S 를 같이 누르면 브레이크 |
| 시동 걸기 / 끄기 | N | 시동 걸기 | `[Lua] keyBinding.lua:103-104`. 같은 키가 켜기·끄기를 번갈아 한다(`[Lua] media\lua\client\Vehicles\ISUI\ISVehicleMenu.lua:1659-1664`). `[번역] UI.json:1035` |
| 브레이크 | Space | 브레이크 | `[Lua] keyBinding.lua:107-108`, `[번역] UI.json:1692` |
| 정속 주행(크루즈) | 왼쪽 Shift | 정속 주행 | `[Lua] keyBinding.lua:111-112`, `[번역] UI.json:1693`. Shift+W 로 켜고 속도를 올리고, Shift+S 로 낮추고, 브레이크로 끈다(`[번역] Tooltip.json Tooltip_Dashboard_SpeedRegulator`) |
| 전조등 | F | 전조등 | `[Lua] keyBinding.lua:115-116`. 운전석에서만(`[Lua] media\lua\server\Items\ItemBindingHandler.lua:23-28`). 걸어 다닐 때 F 는 손전등 켜기(같은 파일, `LIGHT_SOURCE` = F, `keyBinding.lua:281-282`) |
| 히터/에어컨 창 | O | 히터/에어컨 | `[Lua] keyBinding.lua:119-120`, `ISVehicleMenu.lua:1665-1666`, `[번역] UI.json:1037` |
| 정비 화면 | U | 차량 정보 | `[Lua] keyBinding.lua:123-124`. 차 안과 차 옆 모두(`ISVehicleMenu.lua:1652-1653, 1667-1668`). `[번역] UI.json:1038` |
| 경적 | Q (누르고 있는 동안) | 경적 | `[Lua] keyBinding.lua:127-128`. 운전자만, 배터리가 있어야 함(`ISVehicleMenu.lua:1686-1690, 1706`). `[번역] UI.json:1041` |
| (동승자) 외치기 | Q | 외치기 | `[Lua] keyBinding.lua:338-339`. 운전자가 아니면 같은 Q 가 외치기(`ISVehicleMenu.lua:1674-1679`). `[번역] UI.json:458` |
| 차량 메뉴(원형 메뉴) | V (누르고 있다가 놓으며 고르기) | 차량 메뉴 | `[Lua] keyBinding.lua:131-132`, `media\lua\client\ISUI\ISUIHandler.lua:49-53, 76-84`. 차 안과 차 밖에서 내용이 다르다(2·3·5절). `[번역] UI.json:1039` |
| 좌석 이동(좌석 고르기 창) | Z | 좌석 이동 | `[Lua] keyBinding.lua:135-136`, `ISVehicleMenu.lua:1691-1695`. 차 밖에서 누르면 탈 자리를 고르는 창. `[번역] UI.json:1040` |
| 기어 변속 | 키 없음(자동) | – | `keyBinding.lua` 의 `[Vehicle]` 묶음(100-136행)에 기어 키가 없다. 계기판의 글자가 현재 기어(`[번역] Tooltip_Dashboard_Shift` "현재 기어") |
| 사이렌·경광등 | 키 없음 | – | V 메뉴의 "경광등"(`ISVehicleMenu.lua:147-149`). 경찰차·구급차·소방차처럼 경광등이 달린 차만 |

- 키 이름(`StartVehicleEngine` 등)과 번역 키(`UI_optionscreen_binding_StartVehicleEngine`)가 같은 것은 `[Java] zombie.input.KeybindId` 의 문자열로 확인했다.
- **Shift 를 누른 채 E 로 타면** 가까운 문으로 들어가서 운전석으로 옮겨 앉는다(`ISVehicleMenu.lua:1391-1392, 1401-1430`).
- 마우스로도 된다. 운전 중 화면 아래 계기판 아이콘을 누르면 열쇠 꽂기·시동, 전조등, 문 잠금, 트렁크 잠금, 히터, 라디오를 켜고 끈다(`ISVehicleDashboard.lua:502-565`).

**그림 후보**: 계기판 전체(`dashboard`), 라디얼 메뉴 아이콘들(맨 아래 표 A·B). 실제 화면은 PZwiki `VehicleRadialMenu.png`(B41 화면, 표 C).

## 2. 열쇠와 시동

### 2-1. 시동이 걸리는 조건

**사이트 한 줄**: 운전석에 앉아 **차 열쇠를 갖고 있거나 열쇠가 꽂혀 있으면** N 으로 시동이 걸린다. 배터리가 거의 없으면 안 걸린다.

- 근거
  - `[Java] BaseVehicle.tryStartEngine`: 열쇠 소지, 열쇠가 꽂힘(`isKeysInIgnition`), 배선을 딴 차(`isHotwired`) 중 하나면 허용. 엔진 상태 0 이면 실패.
  - 같은 함수: 시동을 걸 때마다 배터리 2.5% 를 쓰고, 남은 양이 10% 이하면 "전력 부족"으로 실패.
  - 연료가 없으면 엔진이 멈춘다(`[Java] VehicleEngine.getAutoShutDownReason` → `OutOfFuel`). `[Lua] Vehicles.lua:880-882`(`CheckEngine.GasTank`).
  - 열쇠가 없으면 캐릭터 머리 위에 "열쇠 없음" 그림이 뜬다(`tryStartEngine` 의 `[img=media/ui/CarKey_none.png]`).
  - 생존 가이드 문구: "차 안에 타고 있고 맞는 열쇠도 가지고 있다면 %1(으)로 시동을 걸 수 있습니다."(`[번역] SurvivalGuide.json:185`)
- 엔진 상태가 50% 아래면 달리다 가끔 꺼진다(`[Java] VehicleEngine.shouldAutoStall`).

### 2-2. 열쇠가 나오는 곳

**사이트 한 줄**: 열쇠는 **꽂혀 있거나, 글러브박스, 근처 집의 서랍·옷장·조리대, 근처 좀비 몸**에서 나온다. 계산대에서도 가끔 나온다.

- 근거 `[Java] BaseVehicle.trySpawnKey`, `addKeyToWorld`, `addKeyToGloveBox`, `addKeyToSquare`, `trySpawnVehicleKeyInObject`, `trySpawnVehicleKeyOnZombie`
- 차가 처음 세상에 불려 올 때(`BaseVehicle.addToWorld`) 정해진다. 아래 확률은 우리 서버 기준이다. 한 번 굴릴 때의 확률(`keySpawnChancedD100`)은 `KeyLootNew × 25` = 0.4 × 25 = **10%**(`BaseVehicle` 생성자).
  1. 먼저 열쇠를 놓을지 정한다. 보통 구역 70%, 폐차장·교통 정체 구역 20%, 경주차 100%(`[Lua] media\lua\shared\VehicleZoneDefinition.lua:20, 158, 183, 190, 197, 204, 577`).
  2. 문이 하나라도 안 잠겨 있고 부서진 차가 아니면: 10% 로 **꽂혀 있음**, 아니면 10% 로 **글러브박스**.
  3. 그래도 안 놓였으면 차 둘레 약 20×20칸을 뒤져서 아직 아무도 안 연 가구에 넣는다. 가구 종류는 조리대(counter), 사무 서랍, 선반, 책상, 서류함, 사물함, 금속 선반, 텐트, 협탁, 판자 은닉처, 옷장, 서랍장이고, 상점 칸은 뺀다. 가구 대신 **좀비**가 걸리면 그 좀비가 죽을 때 떨어뜨린다. 사고 차·교통 정체 차·부서진 차는 좀비에게만 준다.
  4. 그래도 못 놓으면 10% 로 차 근처 바닥에 떨어뜨린다.
  5. 이렇게 못 놓은 차는 그 구역이 다시 불려 올 때 다시 굴린다. 이미 문을 연 적이 있거나, 옮겼거나, 배선을 땄거나, 불탄 차는 다시 굴리지 않는다.
- 열쇠가 열쇠고리에 담겨 나올 수 있고(10%), 그러면 근처 집 열쇠가 함께 들어 있기도 하다(10%)(`putKeyToZombie`, `addKeyToGloveBox`, `randomlyAddNearestBuildingKeyToContainer`).
- 일반 전리품: 계산대(`cashregister`)에 `"CarKey", 2`(`[Lua] media\lua\server\Items\Distributions.lua:183-187`), 허리 가방 앞·뒤에 `"CarKey", 10`(같은 파일 16867-16871, 16915-16919). 이렇게 나온 열쇠가 어느 차 것인지는 미확인.
- "간단한 차량 사용"(`VehicleEasyUse`)을 켜면 열쇠가 항상 글러브박스에 있다(`trySpawnKey`). 우리 서버는 꺼져 있다(`Apocalypse.lua:110`).
- PZwiki 의 "열쇠가 문짝에 꽂혀 있기도 하다"는 말은 생성 코드에서 찾지 못했다. 문에 꽂힌 열쇠를 챙기는 코드(`ISVehicleMenu.lua:1461-1468`)와 서버 명령(`VehicleCommands.lua:264-267`)은 있지만, 열쇠를 문에 꽂아 생성하는 경로는 미확인.

### 2-3. 열쇠 없이 시동: 배선 따기

**사이트 한 줄**: 열쇠가 없으면 운전석에서 V → **"배선 따기"**. **전기공학 1 + 차량정비 2**, 또는 **좀도둑** 직업이어야 한다. 실패하면 다시 하면 된다.

- 조건: `[Lua] ISVehicleMenu.lua:109-121`. 운전석, 열쇠 없음, 꽂힌 열쇠 없음, 아직 배선 안 땀, `(전기공학 >= 1 and 차량정비 >= 2) or 좀도둑 특성`.
  - 98행에 남아 있는 "전기 2 / 정비 3" 조건은 메뉴를 만드는 줄이 주석 처리돼 있어 실제로는 쓰이지 않는다.
  - 조건이 안 되면 메뉴에 "열쇠가 없습니다. 전기공학 1단계와 차량정비 2단계에 도달하면 차량의 배선을 딸 수 있습니다."가 뜬다(`[번역] ContextMenu_VehicleHotwireSkill`).
- 좀도둑 특성은 좀도둑 직업을 고르면 붙는다(`[스크립트] characters\character_professions.txt:3-11` `GrantedTraits = base:burglar`). 설명: "차량 배선을 딸 수 있습니다."(`[번역] UI_trait_BurglarDesc`)
- 성공률: `[Java] BaseVehicle.tryHotwire`. `(100 − 엔진 품질)` 을 5~50 으로 자른 값 + 전기공학 레벨 × 4 (%).
  - 예: 엔진 품질 70 인 차를 전기공학 1 로 따면 30 + 4 = 34%.
  - 좀도둑이라고 성공률이 오르지는 않는다(식에 직업이 없음).
  - PZwiki 설명("기본 50% 에서 엔진 품질 50 초과분만큼 감소, 전기 1레벨당 +4%")과 같다.
- 걸리는 시간: `200 − 전기공학 × 3` 틱(`[Lua] media\lua\shared\Vehicles\TimedActions\ISHotwireVehicle.lua` `getDuration`).
- 실패해도 다시 할 수 있다. 실패할 때 켜지는 "배선 망가짐" 표시(`hotwiredBroken`)는 42.21 에서 저장만 되고 어디서도 검사하지 않는다(Lua 에서는 치트 메뉴 주석에만 나옴: `ISVehicleMechanics.lua:381, 1039`).
- 배선을 딴 차는 그 뒤로 누구나 N 으로 시동을 건다(`tryStartEngine` 의 `isHotwired`). 계기판 툴팁: "배선이 따여 있습니다."(`[번역] Tooltip_Dashboard_Hotwired`)

### 2-4. 잠긴 차에 들어가기

**사이트 한 줄**: 잠긴 차는 V(차 밖) → **"창문 부수기"**. 깨진 창문 옆 문은 열쇠 없이 열린다. **맨손이면 유리에 베이니** 무기를 들고 깬다.

- 문이 잠겨 있을 확률(우리 서버 `LockedCar = 4`): **50%**. 한 문이 정해지면 나머지 문도 따라간다. 문마다 5% 로 자물쇠가 고장 나 있다(`[Lua] Vehicles.lua:132-174`).
- 창문 부수기 메뉴: `ISVehicleMenu.lua:344-352`, `[번역] ContextMenu_Vehicle_Smashwindow` "%1 부수기".
- 손에 무기가 없으면 유리에 긁힌다(`[Lua] media\lua\shared\TimedActions\ISSmashWindow.lua:54-57`).
- 창문이 없거나, 열려 있거나, 깨진 문은 열쇠 없이 잠금을 풀 수 있다(`[Java] BaseVehicle.canUnlockDoor`). 차 안에 앉아 있으면 어느 문이든 풀 수 있다.
- 창문을 깨면 경보가 울린다(2-5).
- 운전석 창보다 조수석이나 뒷좌석 창을 깨는 것이 좋다는 팁은 8절 6번.

### 2-5. 도난 경보

**사이트 한 줄**: 잠긴 차 일부에는 경보가 달려 있다. 열쇠 없이 문을 열거나 창문을 깨면 **약 50초 동안 크게 울리고 멀리 있는 좀비까지 몰려온다.** 끄는 방법은 없고, 한 번 울린 차는 다시 안 울린다.

- 경보가 달릴 확률: 우리 서버 `CarAlarm = 3` 이면 **8%**(1 없음, 2 3%, 4 15%, 5 25%, 6 50%)(`[Java] IsoChunk.AddVehicles_OnZone`). 불탄 차·부서진 차는 제외.
- 잠기지 않은 채 나온 차는 경보가 지워진다(`[Lua] Vehicles.lua:166-169`). 그래서 경보는 잠긴 차에만 있다.
- 울리는 경우
  - 아무도 연 적 없는 차의 문·트렁크·후드를 열쇠 없이 열 때(`[Lua] media\lua\shared\Vehicles\TimedActions\ISOpenVehicleDoor.lua:80-92`). 예전의 20% 확률 판정은 주석 처리돼 있어 **반드시** 울린다.
  - 창문을 때려 상하게 할 때(`[Java] VehicleWindow.damage`).
  - 배선을 따다가: 한 번 시도할 때마다 `(11 − 전기공학)%`(`[Java] BaseVehicle.tryHotwire`).
- 크기와 길이: 소리 반경 150칸(`[Java] VehicleAlarm` `WORLDSOUND_RADIUS = 150`).
  - 길이는 `0.66 × 30 / 하루 길이(실제 분)` 게임 시간이다(`VehicleAlarm.update`, `GameTime.getDeltaMinutesPerDay`). 이걸 실제 시간으로 바꾸면 하루 길이와 상관없이 **약 50초**다.
- 끄기: 메뉴가 없다(일반 플레이 기준. 디버그 메뉴만 있음: `ISVehicleMenu.lua:736-740`).
  - 배터리가 0 이 되면 멈춘다(`VehicleAlarm.update`).
  - 한 번 울리면 경보가 지워진다(`BaseVehicle.triggerAlarm`: `alarmed = false`).
- 열쇠를 갖고 열거나 열쇠가 꽂힌 차는 울리지 않는다(`ISOpenVehicleDoor.lua:85`).
- [웹] 42.9.0 부터 저장했다 다시 불러와도 울리던 경보가 꺼지지 않는다(PZwiki Build 42.9.0).

### 2-6. "생존자 차" (상태 좋은 차)

**사이트 한 줄**: 가끔 **잠겨 있지만 상태가 아주 좋은 차**가 있다. 배터리와 기름이 넉넉하다.

- 근거
  - 우리 서버 `RecentlySurvivorVehicles = 2` 이면 10%(1 없음, 3 30%, 4 50%)(`[Java] BaseVehicle.createPhysics`).
  - 이런 차는 배터리 80~100%(`Vehicles.lua:120-123`), 문 잠김(`Vehicles.lua:140-145`, `LockedCar` 가 "없음"이 아닐 때), 기름이 탱크의 2/3 이상(`Vehicles.lua:225-228`), 타이어 공기 2/3 이상(`Vehicles.lua:395-398`)이다.
  - 화면 이름: "생존자의 차량"(`[번역] Sandbox_RecentlySurvivorVehicles`)

### 2-7. 열쇠 관리

**사이트 한 줄**: 시동을 끄면 열쇠가 자동으로 내 가방에 들어온다. 꽂아 두고 내리려면 **설정 → 접근성 설정 → "열쇠 꽂은 채 내리기"** 를 켠다. 차 열쇠는 복사할 수 없다.

- 시동을 끌 때 이 옵션이 꺼져 있으면 열쇠가 빠진다(`[Java] BaseVehicle` 엔진 상태 변경 부분: `if (!Core.getInstance().getOptionLeaveKeyInIgnition()) this.setKeysInIgnition(false)`).
- 옵션 위치: `[Lua] media\lua\client\OptionScreens\MainOptions.lua:2367`(접근성 설정 탭), `2542`. 기본값 꺼짐(`[Java] Core` `newOption("leaveKeyInIgnition", false)`). `[번역] UI_optionscreen_LeaveKeyInIgnition` "열쇠 꽂은 채 내리기".
- 열쇠 복사 레시피는 건물 열쇠용 `CopyBuildingKey` 하나뿐이다(`[스크립트] recipes\recipes.txt:429-447`, 입력 태그 `base:buildingkey`).
- 차 밖에서 문을 잠그려면 열쇠가 있어야 한다. 차 안에서는 열쇠 없이 잠근다(`[Java] BaseVehicle.canLockDoor`).

**그림 후보(2절)**: 열쇠 아이콘 `Item_CarKey`, 열쇠 없음 `CarKey_none`, 시동 아이콘 `ignition`·`ignition_key_on`·`ignition_hotwired`, 라디얼 `vehicle_ignitionON`, 창문 부수기 `vehicle_smash_window.png`. 웹: PZwiki `VehicleKey.png`(B41 화면).

## 3. 연료

### 3-1. 주유소에서 넣기

**사이트 한 줄**: 시동을 끄고 주유구 쪽을 주유기 옆에 댄 뒤 V(또는 우클릭) → **"주유기로 연료 넣기"**. **전기가 들어와야** 한다.

- 메뉴 조건: `[Lua] ISVehicleMenu.lua:1054-1101`.
  - 시동이 꺼져 있어야 한다(1062행).
  - 주유구 기준 앞뒤좌우 2칸 안에 기름이 남은 주유기가 있어야 한다(`[Lua] media\lua\client\Vehicles\ISUI\ISVehiclePartMenu.lua:25-47`).
  - 그 칸에 전력망 전기가 들어오거나, "외부에서 발전기 사용 가능"이 켜져 있고 전기가 들어와야 한다(1088행).
- `[번역] ContextMenu_VehicleRefuelFromPump` "주유기로 연료 넣기". 차 밖에서 V 메뉴나 우클릭 메뉴 모두에 뜬다(`FillPartMenu` 가 두 곳에서 불림: 314행, 603행).
- 주유기의 기름양: 처음에 최대치의 0~80%(`FuelStationGasMin 0.0`, `FuelStationGasMax 0.8`), 20% 는 처음부터 비어 있다(`FuelStationGasEmptyChance 20`)(`Apocalypse.lua:112-115`).
- 계기판에 주유구 방향 화살표가 있다(`ISVehicleDashboard.lua:593-594`). 생존 가이드: "계기판의 연료 게이지에서 주유구 방향을 확인하는 걸 잊지 마세요."(`[번역] SurvivalGuide.json:190`)

### 3-2. 단전 뒤

**사이트 한 줄**: 전기가 끊기면(게임 시작 후 **14~30일 사이**) 주유기 옆에 **발전기를 놓고 연결**해야 주유기가 돈다. 발전기 소리에도 좀비가 몰려온다.

- 단전 시점: `ElecShut = 2`(`Apocalypse.lua:17`) → 14~30일 사이 무작위(`[Java] SandboxOptions.randomElectricityShut` case 2).
- 발전기 조건: "외부에서 발전기 사용 가능"(`AllowExteriorGenerator`) 기본 켜짐(`Apocalypse.lua:97`).
  - 툴팁: "이렇게 하면 주유기에 전력을 공급하는 등의 행위가 가능합니다."(`[번역] Sandbox_AllowExteriorGenerator_tooltip`)
  - 발전기 범위는 `GeneratorTileRange` 기본 20칸(`SandboxOptions` 289행).
- 발전기 연결 지식은 전기공학 3 에 자동으로 배운다(`[Lua] media\lua\server\XpSystem\XpUpdate.lua:262-264`). 잡지나 직업으로 배우는 경로도 있다.
- [웹] Reddit 2026-01-10(B42): "주유기 옆에 발전기를 놓고 기름을 채워 연결해야 한다. 쓸 때만 켜라."

### 3-3. 기름통으로 넣기

**사이트 한 줄**: 기름이 든 통을 들고 차 옆에서 V(또는 우클릭) → **"기름 넣기"**. 기름통(10L), 제리캔(20L)뿐 아니라 **기름이 든 아무 액체 용기**나 된다.

- 조건: 시동이 꺼져 있고, 가방에 기름(Petrol)이 든 용기가 있고, 탱크가 가득 차지 않았을 것(`ISVehicleMenu.lua:9-11, 1062-1069`). `[번역] ContextMenu_VehicleAddGas` "기름 넣기".
- 용기 용량
  - 기름통 `Base.PetrolCan` 10L(`[스크립트] items\normal.txt`, `FluidContainer Capacity = 10.0`, `[번역] ItemName "기름통"`)
  - 제리캔 `Base.JerryCan` 20L(같은 파일, `Capacity = 20.0`, "제리캔")
- 생존 가이드: "전원이 공급된 주유기에서는 아무 액체 용기에 기름을 채울 수 있습니다."(`[번역] SurvivalGuide.json:190`)

### 3-4. 다른 차에서 빼기

**사이트 한 줄**: **고무 호스**와 빈(또는 덜 찬) 통을 들고, 시동이 꺼진 차 옆에서 V(또는 우클릭) → **"기름 빼기"**.

- 조건: `ISVehicleMenu.lua:1070-1084`.
  - 시동 꺼짐, 차에 기름이 있음, 빈 용기나 덜 찬 기름 용기가 있음, `SiphonGas` 태그 아이템이 있음.
  - 호스가 없으면 "호스가 필요합니다."(`[번역] ContextMenu_VehicleNeedHose`)
  - 가방 속까지 찾는다(`getFirstTagRecurse`).
- 호스 아이템: `Base.RubberHose`, 태그 `base:siphongas`(`[스크립트] items\normal.txt:11180-11189`), `[번역]` "고무 호스".
- PZwiki Vehicle 문서의 "빈 기름통만 있으면 빼기 메뉴가 뜬다"는 B41 자료라서 쓰지 않는다.

### 3-5. 연료 게이지와 연비

**사이트 한 줄**: 운전 중 화면 아래 계기판의 **연료 바늘**을 본다. 15% 밑으로 내려가면 경고등이 켜진다. **무게가 1000 에 가까운 차(올-터레인, 랭 4000, D6)가 연비가 좋고, 쉐볼리에 다트가 가장 나쁘다.**

- 게이지 그림: `ISVehicleDashboard.lua:588-590`. 15% 미만 경고: 같은 파일 370행.
- 연료 소모: `[Lua] Vehicles.lua:450-503`(`Update.GasTank`).
  - 차 무게 배수 `|1000 − 무게| / 300 + 1`(465행). 무게 1000 이 가장 적게 쓴다.
  - 엔진 품질이 낮을수록 많이 쓴다(464행).
  - 서 있어도(공회전) 쓴다(472-483행).
  - 히터를 켜면 더 쓴다(459-462행, 약 6%).
  - 연료 탱크 상태가 70 미만이면 조금씩 샌다(490-494행).
- 차종 무게(`[스크립트] vehicles\vehicle_*_template.txt` 의 `mass`): 다트 650, 니알라 800, 세리스 웨건 900, 랜처 900, 랭 4000 950, 올-터레인 1000, D6 1030, 불드라이버 1104, 스텝 승합차 1160.
- [웹] Reddit 2026-10-15(42.21.0 코드 분석): 랭 4000 이 가장 좋고 올-터레인이 1% 차이로 2위, 다트는 약 3.5배를 쓴다. 게임 식과 방향이 맞는다.
- 처음 발견한 차의 기름(우리 서버): 45% 확률로 기름이 있고(`ChanceHasGas = 2`), 있으면 1L ~ 탱크의 1/4 정도로 적다(`InitialGas = 2` "적음")(`Vehicles.lua:229-259`).

**그림 후보(3절)**: 연료 게이지 `rj-vehicle_fuelguage-full/low/empty`, 라디얼 `vehicle_refuel_from_pump.png`·`gas_refuel.png`·`gas_siphon.png`, 아이콘 `Item_Petrol`·`Item_JerrycanMilitary`·`Item_RubberHose`. 웹: PZwiki `VehicleGas1.png`(주유기)·`VehicleGas2.png`(기름통)·`Out_of_gas_generic.png`(B42 빈 주유기).

## 4. 정비

### 4-1. 정비 화면 여는 법

**사이트 한 줄**: 차를 세우고 **U**(차 안이나 옆), 또는 V → **"차량 정비"**, 또는 후드 앞에서 **E**. 캐릭터가 후드로 걸어가서 열고 정비 창을 띄운다.

- 근거
  - `ISVehicleMenu.lua:960-1004`(`onMechanic`), 185-189행(달리는 중이면 "정비 창을 열기 위해서는 차량을 세워야 합니다."), 297행(차 밖 메뉴).
  - 후드 앞 E: `[Lua] Vehicles.lua:829-857`.
  - `[번역] ContextMenu_VehicleMechanics` "차량 정비".
  - 생존 가이드: "차량의 후드에서 %1을(를) 누르거나, %2 메뉴에서 %3 아이콘을 선택해 차량의 상태를 확인하세요."(`[번역] SurvivalGuide.json:192`)
- 후드가 잠겨 있어도, 열쇠가 있거나 문·창문 하나라도 열려 있거나·깨졌거나·없으면 연다(`Vehicles.lua:1370-1389` `RequiredKeyNotFound`, 주석 "If the player can get in the vehicle, they can pop the hood").
- 멀티에서 관리자는 어디서든 바로 연다(`ISVehicleMenu.lua:969-971`).

### 4-2. 정비 화면에서 하는 일

**사이트 한 줄**: 부품마다 **상태(%)** 가 나온다. 부품을 **우클릭**해서 장착·분리·수리하기·공기압 넣기를 고른다. 툴팁에 필요한 도구, 기술, 성공률이 나온다.

- 메뉴 이름(`[번역]`): "장착"(IGUI_Install), "분리"(IGUI_Uninstall), "수리하기"(ContextMenu_Repair), "엔진 수리"(IGUI_RepairEngine), "엔진 부품 분리"(IGUI_TakeEngineParts), "공기압 넣기"/"공기압 빼기"(IGUI_InflateTire/DeflateTire), "차량상태"(IGUI_OverallCondition), "수리 성공률:"/"손상 가능성:"(Tooltip_chanceSuccess/Failure), "필요 기술: %1 %2", "정비 매뉴얼: %1", "차량 열쇠 필요함".
- 기술이 모자라도 시도는 된다. 모자란 레벨마다 성공률이 `20 + 15 × 부족 레벨` 만큼 떨어지고, 실패하면 부품이 5~10 상할 수 있다(`[Lua] Vehicles.lua:1463-1485, 1404-1461`).
  - 예: 3레벨이 필요한데 2레벨이면 성공률 65%.
- 기술이 높은 사람이 브레이크·타이어를 달면 제동력·접지력이 조금 더 좋다(`[Java] BaseVehicle.updatePartStats` 의 `getMechanicSkillInstaller`).

### 4-3. 부품별 도구와 레벨 (일반 차 기준)

**사이트 한 줄**: 타이어는 **잭 + 십자 휠 렌치**(정비 1), 배터리·라이트·라디오는 **스크류드라이버**(기술 필요 없음), 문·후드·트렁크·브레이크·서스펜션은 **렌치**(정비 3~4 + 정비 지식).

| 부품 | 도구 | 차량정비 | 정비 지식 | 근거 (`[스크립트] vehicles\`) |
|---|---|---|---|---|
| 타이어 | 잭(`Base.Jack`) + 십자 휠 렌치(`base:lugwrench`) | 1 | 필요 없음 | `template_tire.txt:61-97`. 브레이크·서스펜션이 달려 있어야 장착(12, 22, 32, 42행) |
| 배터리 | 스크류드라이버 | – | 필요 없음 | `template_battery.txt:19-42`. 시동이 꺼져 있어야 분리(`Vehicles.lua:921-930`) |
| 전조등 | 스크류드라이버 | – | 필요 없음 | `template_headlight.txt:38-59` |
| 라디오 | 스크류드라이버 | – | 필요 없음 | `template_radio.txt:18-40` |
| 좌석 | 스크류드라이버 | 1 | 필요 | `template_seat.txt:77-104`. 비어 있어야 분리 |
| 브레이크 | 잭 + 렌치 | 3 | 필요 | `template_brake.txt:68-105`. 타이어를 먼저 빼야 함 |
| 서스펜션 | 잭 + 렌치 | 3 | 필요 | `template_suspension.txt:68-105`. 타이어를 먼저 빼야 함 |
| 후드 | 렌치 | 3 | 필요 | `template_engine_door.txt:43-69` |
| 트렁크 문 | 렌치 | 3 | 필요 | `template_trunk_door.txt:55-81` |
| 문 | 렌치 | 4 | 필요 | `template_door.txt:175-201`. 창문을 먼저 빼야 함 |
| 옆 창문 | 스크류드라이버 | 3 | 필요 | `template_window_nodoor.txt:64-90`. 문이 달려 있어야 장착 |
| 앞·뒤 유리 | 스크류드라이버 | 5 | 필요 | `template_windshield.txt:23-101` |
| 머플러 | 렌치 | 5 | 필요 | `template_muffler.txt:18-44` |
| 연료 탱크 | 스크류드라이버 + 렌치 | 5 | 필요 | `template_gastank.txt:31-72`. 비어 있어야 분리 |

- 대형 차는 일부 레벨이 더 높다. 예: 올-터레인 좌석 2, 연료 탱크 7(`vehicle_suv_template.txt:154-179`).
- 엔진 수리: 예비 엔진 부품 + 렌치 + 차량정비가 차의 "엔진 수리 레벨" 이상이어야 한다(`[Lua] media\lua\client\Vehicles\ISUI\ISVehicleMechanics.lua:333-338`).
  - 엔진 수리 레벨: 일반 4, 대형 5, 스포츠 6(`engineRepairLevel`, `vehicle_car_normal_template.txt:6`, `vehicle_suv_template.txt`, `vehicle_car_sports.txt`).
  - "엔진 부품 분리"는 엔진 상태가 10 넘게 남아 있어야 한다(325행). `[번역] Base.EngineParts` "예비 엔진 부품".
- 열쇠가 필요한 부품: 배터리, 문, 엔진, 후드, 연료 탱크, 글러브박스, 전조등, 좌석, 트렁크, 트렁크 문, 창문, 앞·뒤 유리(`mechanicRequireKey = true`). 단, 문·창문 하나라도 열렸거나 깨졌으면 열쇠 없이 된다(4-1).
  - **타이어·브레이크·서스펜션·머플러는 잠긴 차에서도 열쇠 없이 뗄 수 있다.**
- 불탄 차·부서진 차 분해("망가진 자동차 분해하기"): 용접 마스크 + 프로판 토치(10회분 이상)(`ISVehicleMenu.lua:616-646`). `[번역] Tooltip_removeBurntVehicle`

### 4-4. 차종별 정비 지식 (잡지·직업)

**사이트 한 줄**: 차는 **일반 / 대형 / 스포츠** 세 종류다. 대형·스포츠 차의 부품을 다루려면 **"라이네스 상용/고성능 차량 설명서"** 잡지를 읽어야 한다. **자동차 정비공** 직업은 셋 다 알고 시작한다.

- 차 종류: `mechanicType` 1 = 일반, 2 = 대형, 3 = 스포츠(`[번역] IGUI_VehicleType_1~3` "일반/대형/스포츠").
  - 일반: 니알라, 다트, 호라이즌, 세리스 웨건, 랜처, 택시, 경찰차, 트레일러
  - 대형: 올-터레인, D6, 불드라이버, 밸류라인 계열, 스텝 승합차, 구급차, 소방차
  - 스포츠: 코세트, 랭 4000, 대시 엘리트, 프리마니, 경주차
  - 근거: 각 `vehicle_*_template.txt`/`vehicle_*.txt` 의 `mechanicType`
- 필요한 지식
  - 일반 차 부품: "표준 차량정비"(`Basic Mechanics`, 공통 템플릿)
  - 대형 차: "상용 차량정비"(`Intermediate Mechanics`, 스크립트 1818곳)
  - 스포츠 차: "고성능 차량정비"(`Advanced Mechanics`, 202곳)
  - `[번역]` "- 표준 차량정비", "- 상용 차량정비", "- 고성능 차량정비"
- 배우는 방법
  - 잡지: "잡지: 라이네스 표준/상용/고성능 차량 설명서"(`Base.MechanicMag1~3`, `[스크립트] items\literature.txt:5774-5820`)
  - 자동차 정비공 직업: 셋 다(`[스크립트] characters\character_professions.txt` `base:mechanics` `GrantedRecipes = Basic Mechanics;Intermediate Mechanics;Advanced Mechanics`)
  - "차량 지식" 특성(3점): 표준·상용(`character_traits.txt:655-666`)
  - 차량정비 8레벨에서 표준, 9레벨에서 상용, 10레벨에서 고성능을 저절로 배운다(`[Lua] XpUpdate.lua:250-260`, 발명가 특성이면 1레벨 빨리).

### 4-5. 배터리

**사이트 한 줄**: 시동을 켜 두면 배터리가 충전된다. 시동을 끈 채 전조등·라디오·경광등을 켜 두면 닳는다. 다 닳은 배터리는 **차량 배터리 충전기**(전기 필요)로 채우거나 다른 차 배터리로 바꾼다.

- 엔진이 돌면 게임 1분에 0.1% 씩 충전(`[Lua] Vehicles.lua:505-523`). 빈 배터리를 가득 채우려면 시동을 켠 채 게임 시간 약 17시간.
- 시동 꺼진 채 전조등·라디오·경광등·사이렌: 닳음(562-575, 681-686, 646-653행). 히터는 시동 중에도 조금 닳음(615-617행).
- 처음 차를 찾았을 때 배터리는 세상이 오래될수록 낮다(114-130행).
- 충전기: 바닥에 놓고 배터리를 연결해서 켠다. 켜려면 전기가 있어야 한다(`[Lua] media\lua\client\ISUI\ISWorldObjectContextMenu.lua:413-470`). `[번역]` "차량 배터리 충전기", "차량 배터리 연결", "켜기".

### 4-6. 타이어 공기

**사이트 한 줄**: 타이어는 정비 화면에서 우클릭 → **"공기압 넣기"**(**타이어 펌프** 필요). 공기가 거의 없으면 달리다 타이어가 빠진다.

- 근거
  - `[Lua] ISVehiclePartMenu.lua:290-303`(타이어 펌프 `TirePump` 필요). `[번역] Base.TirePump` "타이어 펌프".
  - 달리면 공기가 조금씩 빠지고, 공기가 5 미만이면 타이어가 빠질 수 있고, 상태가 15 미만이면 터질 수 있다(`Vehicles.lua:752-783`).
  - 타이어가 없거나 바람이 빠져도 운전은 된다(`Vehicles.lua:888-892`, "allow driving on removed/flat tires").

### 4-7. 정비 경험치 올리기

**사이트 한 줄**: 정비 경험치는 **같은 차의 같은 부품은 게임 시간 24시간에 한 번만** 들어온다. 폐차장의 여러 차에서 부품을 떼고 붙이며 올린다. 어려운 부품일수록 경험치가 많다.

- 근거
  - `[Java] IsoPlayer.addMechanicsItem`: 부품 ID + 차 ID 로 기록하고, 처음일 때만 경험치를 준다. 필요 레벨 6 이상이면 6~14, 4 이상이면 6~10, 2 이상이면 4~8.
  - 기록은 게임 시간 24시간 뒤 지워진다(`IsoPlayer.updateMechanicsItems`, `86400000L`).
  - 장착·분리가 각각 따로 기록된다(`Vehicles.lua:1413, 1443` 끝 글자 "0"/"1").
- [웹] PZwiki Mechanics(42.18.0): "같은 차의 같은 부품은 24시간에 한 번" — 일치.

**그림 후보(4절)**: 정비 화면 차 그림 `media\ui\vehicles\mechanic overlay\4door_base.png` 등, 라디얼 `vehicle_repair`, 도구 아이콘 `Item_Wrench`·`Item_LugWrench`·`Item_CarJack`·`Item_Screwdriver`·`Item_TirePump`·`Item_CarBattery`·`Item_CarBatteryCharger`·`Item_EngineParts`·`Item_MagazineMechanic1~3`. 웹: PZwiki `VehicleMechanics.png`(2018, 구버전).

## 5. 운전 중 주의

### 5-1. 소음

**사이트 한 줄**: 차는 시끄럽다. **엔진 소리, 경적, 경보, 사이렌**이 멀리 있는 좀비를 부른다. **머플러가 없거나 망가지면 두 배로 시끄럽다.**

- 엔진: 차종별 기본 소음(`engineLoudness`)
  - 다트·호라이즌 55, 니알라·세리스 웨건 80, 코세트·랜처 90, 올-터레인·밸류라인·스텝 승합차 100, D6 110, 불드라이버 120
  - 각 `vehicle_*_template.txt` 의 `engineLoudness`
- 계산: `[Java] BaseVehicle.updatePartStats`
  - 기본 소음 × 좀비 유인 배율 ÷ 2
  - 머플러 상태가 나쁠수록 커지고, 머플러가 없으면 ×2
- 엔진 회전수가 높을수록 멀리 퍼진다(`[Java] VehicleEngine.updateWorldSounds`).
- 멀티 서버 설정 `CarEngineAttractionModifier`(기본 0.5)가 범위를 더 줄인다(같은 함수, `ServerOptions` 168행).
  - 툴팁: "차량의 좀비 유인 범위를 조정합니다."(`[번역] UI_ServerOption_CarEngineAttractionModifier_tooltip`)
- 다른 소리
  - 경적 150칸(`BaseVehicle.onHornStart`)
  - 경보 150칸(`VehicleAlarm`)
  - 사이렌 100칸, 계속 반복(`BaseVehicle.updateWorldSounds`, `SirenEffectsZombies` 기본 켜짐)
  - 사이렌 자동 꺼짐 `SirenShutoffHours = 0`(안 꺼짐)(`Apocalypse.lua:124, 129`)
- 생존 가이드: "엔진 소리는 좀비의 주위를 끌 수 있습니다."(`[번역] SurvivalGuide.json:185`)

### 5-2. 좀비를 치면 차가 상한다

**사이트 한 줄**: 좀비를 치면 **후드가 먼저 상하고, 후드가 깨지면 엔진이 상한다.** 세게 치면 앞유리·앞타이어·전조등도 상한다. 후진으로 치면 트렁크·뒷유리·연료 탱크가 상한다.

- 근거
  - `[Java] BaseVehicle.addDamageFrontHitAChr`: 후드 → (후드 0 또는 없음) 엔진, 피해 12 초과 시 앞유리, 앞타이어, 전조등.
  - `addDamageRearHitAChr`: 트렁크, 뒷문, 뒷유리, 뒷타이어, 후미등, 연료 탱크.
  - 벽·차와 부딪힌 충돌 피해 배수는 "차량이 입는 손상"(`CarDamageOnImpact = 3` 보통)(`BaseVehicle.crash`).
  - 달리면 서스펜션·머플러·타이어가 조금씩 닳는다. 비포장길과 급커브에서 더 빨리 닳는다(`Vehicles.lua:722-783`).
  - 후드가 없거나 망가지면 엔진이 뜨거워진다(`Vehicles.lua:526-560`).

### 5-3. 사고 시 부상

**사이트 한 줄**: 세게 부딪히면 **탄 사람 모두 다친다.** 크게 부딪히면 깊은 상처, 골절, 유리 박힘까지 생긴다. 창문이 많이 깨져 있을수록 유리에 다치기 쉽다.

- 근거
  - `[Java] BaseVehicle.damagePlayers`: "차량 탑승 시 교통사고 피해 활성화"(`PlayerDamageFromCrash`) 기본 켜짐(`Apocalypse.lua:123`).
  - `addRandomDamageFromCrash`: 충돌이 클수록 다치는 부위가 1~3곳. 부위 피해 40 초과면 1/12 확률로 깊은 상처, 50 초과면 1/10 확률로 골절. 30 초과면 깨진 창문 수에 따라 유리 상처.
  - 차종마다 보호 정도가 다르다(`playerDamageProtection`).
- 차로 친구를 쳐도 피해가 없다. "차량이 플레이어에게 주는 피해량" 기본 "없음"(`DamageToPlayerFromHitByACar = 1`, `Apocalypse.lua:120`, `[번역] _option1 "없음"`).

### 5-4. 짐 싣기 (트렁크·글러브박스·좌석)

**사이트 한 줄**: **트렁크**는 차 뒤에서 트렁크를 열고 쓴다. **글러브박스**는 앞좌석에서, **좌석**에도 짐을 둘 수 있다. 부품 상태가 나쁘면 담을 수 있는 양이 줄어든다.

- 트렁크 크기
  - 다트·호라이즌·랜처 40, 세리스 웨건 60, D6 짐칸 110, 밴(밸류라인·구급차)·불드라이버 130, 스텝 승합차 160
  - `[스크립트]` 각 차 파일의 `capacity`. 예: `vehicle_stepvan_template.txt`, `vehicle_van.txt`, `vehicle_pickuptruck_template.txt`, `vehicle_car_small_template.txt`
- 차 파일에 값이 없는 차는 트렁크 부품 아이템 값을 쓴다. 일반 차 트렁크 40/55/70, 대형 70/85/150, 스포츠 45(`[스크립트] items` 의 `SmallTrunk1`·`NormalTrunk1`·`BigTrunk1`·`SmallTrunk2`·`NormalTrunk2`·`BigTrunk2`·`NormalTrunk3` `MaxCapacity`). 니알라가 55 인지는 부품 선택 방식 때문에 미확인.
  - [웹] PZwiki 표의 올-터레인 85 는 `NormalTrunk2` 85 와 같다.
- 글러브박스: 일반 3, 대형 10, 스포츠 5(`GloveBox1~3`). 좌석: 20(`NormalCarSeat1`). 상태가 나쁘면 줄어든다(`conditionAffectsCapacity = true`, `template_trunk.txt` 등).
- 쓰는 법
  - 트렁크: 차 밖, 트렁크 문이 열려 있거나 트렁크 문이 없을 때(`[Lua] Vehicles.lua:24-34`). 올-터레인·밴처럼 일부 차는 뒷좌석에서 차 안 트렁크를 쓸 수 있다(42-59행, `vehicle_suv_template.txt:147-153`).
  - 글러브박스: 차 안 앞좌석, 또는 차 밖에서 조수석 문을 열고(88-106행).
  - 좌석: 차 안에서 손이 닿는 자리, 또는 차 밖에서 그 문을 열고(61-86행). 짐이 있는 자리에 앉으려 하면 짐을 트렁크나 옆자리로 옮기고, 4분의 1 이하로 줄어야 앉는다(`ISVehicleMenu.lua:1333-1370`).
- 트렁크 문이 없거나 상태가 60 미만이면, 시속 20km 넘게 달리며 급하게 꺾을 때 짐이 길에 떨어진다(`Vehicles.lua:786-814`).
- 생존 가이드: "차량 트렁크엔 많은 아이템을 넣을 수 있습니다. 시체 한 두 구도 거뜬하죠."(`[번역] SurvivalGuide.json:197`)

### 5-5. 히터·라디오·문 잠그기·잠

**사이트 한 줄**: **O** 로 히터/에어컨 온도를 맞춘다(시동 중일 때만). **라디오는 앞좌석에서만** 켠다. 차 안에서는 V → **"모든 문 잠그기"** 로 문을 잠근다.

- 히터: 시동이 켜져 있고 엔진 온도가 30 을 넘어야 실내 온도가 바뀐다(`Vehicles.lua:577-623`). 창문을 열면 실내가 식는다(658-679행). 시동을 끄면 히터가 꺼진다(`[Java] BaseVehicle` 엔진 정지 부분).
- 라디오: V 메뉴 "장치 조작하기"는 앞좌석 두 자리만(`ISVehicleMenu.lua:151-158`). 계기판 라디오 아이콘도 된다. 시동을 끈 채 켜 두면 배터리가 닳는다.
- 문 잠그기: 차 안 V 메뉴 "모든 문 잠그기 / 모든 문 잠금 해제하기"(173-182행), 계기판 문 아이콘. 트렁크는 계기판 트렁크 아이콘(`ISVehicleDashboard.lua:525-529`). `[번역] ContextMenu_Lock_Doors`
- 잠: 멀티 서버 기본값 `SleepAllowed = false` 라서 차 안 메뉴에 "잠자기"가 안 나온다(`ISVehicleMenu.lua:190`, `[Java] ServerOptions` 124행). 우리 서버는 이 값을 안 바꾼다(README).
- 술에 취해(만취 2단계 이상) 운전하면 조작이 늦게 먹는다(`[Java] CarController` 147행 `bDrunkDriver`, `delayCommandWhileDrunk`).
- 동승자는 달리는 차에서 못 내린다. "움직이고 있는 차량에서 나올 수 없습니다."(`ISVehicleMenu.lua:1564-1571`). 운전자가 내리거나 자리를 옮기면 차가 먼저 선다(1562-1563, 1106행).

### 5-6. 견인·트레일러

**사이트 한 줄**: 트레일러를 차 **뒤에 6칸 안으로** 대고 내려서 V → **"(트레일러)를 (차)에 연결하기"**. 도구는 필요 없다. 차로 다른 차나 불탄 차도 끌 수 있다.

- 근거
  - `[Lua] ISVehicleMenu.lua:354`(차 밖 메뉴), 447-588(`TowMenu`), 1728-1739.
  - `[Lua] media\lua\client\Vehicles\ISVehicleTrailerUtils.lua:3-18`(주변 6칸 탐색).
  - `[Lua] media\lua\client\Vehicles\TimedActions\ISAttachTrailerToVehicle.lua`(도구 검사 없음).
  - `[번역] ContextMenu_Vehicle_AttachTrailer` "%1를 %2에 연결하기", `ContextMenu_Vehicle_DetachTrailer` "%1 분리하기".
  - 생존 가이드: "차량 뒤에 서서 %1 메뉴에서 트레일러를 연결하거나 떼어내세요."(`[번역] SurvivalGuide.json:195`)
- 서버 설정: 차량 견인·트레일러 견인·불탄 차 견인을 각각 끌 수 있다(`DisableVehicleTowing`/`DisableTrailerTowing`/`DisableBurntTowing`, 기본 모두 false, `ServerOptions` 175-177행). 우리 서버는 기본값.
- 가축 트레일러에 동물을 태울 수 있다(`ISVehicleMenu.lua:665-714`).
- [웹] 42.20.0: 너무 빨리 급하게 꺾으면 트레일러가 풀릴 수 있다(PZwiki Build 42.20.0). 코드로는 미확인.
- [웹] 견인은 마력이 높은 스포츠카가 잘 끈다(PZwiki Trailer). 코드로는 미확인.

**그림 후보(5절)**: 라디얼 `vehicle_temperatureHOT`·`vehicle_speakersON`·`vehicle_lockdoors`·`vehicle_horn`·`vehicle_siren`·`vehicle_lightbar`, `ZoomIn.png`(연결)·`ZoomOut.png`(분리), 아이콘 `Item_CarTrunk`·`Item_GloveBox`·`Item_CarSeat`. 웹: PZwiki `VehicleTow.png`(B41)·`Cow-in-livestock-trailer.jpg`(2026-09, B42.2x).

## 6. 멀티에서

### 6-1. 같이 타기

**사이트 한 줄**: **운전은 한 명**(운전석), 나머지는 빈자리에 탄다. **Z** 로 자리를 바꾼다. 경적은 운전자만 울리고, 동승자가 Q 를 누르면 외친다.

- 운전석은 좌석 0 이다. 시동·배선 따기·전조등·경적은 `isDriver` 검사를 한다(`ISVehicleMenu.lua:87, 109, 123, 143`).
- 좌석 수: 각 차 파일의 `seats`(다트·니알라 4, D6·밴·스텝 승합차 2, 밸류라인 좌석형 6).
- 이미 누가 앉은 자리: "이미 누가 좌석에 타고있어."(`ISVehicleMenu.lua:1378-1382`)
- 자리 바꾸기: Z(좌석 이동 창) 또는 V → "좌석 이동"(85행). 문으로 못 들어가는 뒷자리는 다른 문으로 타서 옮겨 앉는다(1281-1296행).

### 6-2. 다른 사람 차 쓰기

**사이트 한 줄**: 바닐라에는 **차 주인 개념이 없다.** 열쇠를 가진 사람, 또는 배선이 따진 차는 누구나 몬다. 차 열쇠는 하나뿐이니 **글러브박스에 두거나 "열쇠 꽂은 채 내리기"를 켜서** 같이 쓴다.

- 서버 옵션(`[Java] ServerOptions`)과 샌드박스 옵션(`SandboxOptions`) 전체에 차 소유·잠금 권한 항목이 없다. 차량 관련 서버 옵션은 아래 표가 전부다.
- 열쇠 복사 불가(2-7). 배선 딴 차는 누구나 시동(2-3). [웹] PZwiki Vehicle: "Any player can access a hot-wired car." — 일치.

### 6-3. 차량 관련 서버 설정 (ini, 우리 서버는 기본값)

| 키 | 기본값 | 의미 | 근거 (`[Java] ServerOptions` 행) |
|---|---|---|---|
| `CarEngineAttractionModifier` | 0.5 | 엔진 소리로 좀비를 부르는 범위 배율 | 168 |
| `SpeedLimit` | 70.0 | 멀티에서 차 속도 계산에 쓰는 제한값. 실제 체감 효과는 미확인 | 137, `BaseVehicle.getFakeSpeedModifier`, `CarController` |
| `DisableVehicleTowing` | false | 차로 차 끌기 끄기 | 175 |
| `DisableTrailerTowing` | false | 트레일러 끌기 끄기 | 176 |
| `DisableBurntTowing` | false | 불탄 차 끌기 끄기 | 177 |
| `SleepAllowed` | false | 잠자기 허용(차 안 "잠자기" 메뉴 포함) | 124 |

### 6-4. 차량 관련 샌드박스 설정 (우리 서버 = Apocalypse 값)

| 키 | 화면 이름(`[번역] Sandbox.json`) | 우리 서버 | Java 기본 | 실제 효과(코드) |
|---|---|---|---|---|
| `EnableVehicles` | 차량 생성 여부 | true | true | – |
| `CarSpawnRate` | 차량 생성 빈도 | 3 보통 | 4 많음 | 구역별 생성 확률 ÷ 1.5. 많음은 그대로, 적음은 ÷10, 매우 많음은 ×2(`IsoChunk.AddVehicles_OnZone`) |
| `ZombieAttractionMultiplier` | 좀비 유인 배율 | 1.0 | 1.0 | 엔진 소음 배율(`Vehicles.lua:280`, `updatePartStats`) |
| `VehicleEasyUse` | 간단한 차량 사용 | false | false | 켜면 문 안 잠김, 기름·배터리 가득, 열쇠는 글러브박스 |
| `InitialGas` | 초기 차량의 연료량 | 2 적음 | 3 보통 | `Vehicles.lua:238-256` |
| `ChanceHasGas` | 차량에 연료가 있을 확률 | 2 보통 | 2 보통 | 45%(낮음 20%, 높음 95%)(`Vehicles.lua:230-236`) |
| `FuelStationGasInfinite` | 무한 기름 주유기 | false | false | – |
| `FuelStationGasMin` / `Max` | 초기 주유소의 최소/최대 기름양 | 0.0 / 0.8 | 0.0 / 0.7 | 주유기 처음 기름 비율 |
| `FuelStationGasEmptyChance` | 초기 주유소의 고갈 확률 | 20 | 20 | 처음부터 빈 주유기 % |
| `LockedCar` | 차량이 잠겨 있을 확률 | 4 보통 | 4 보통 | 50%(없음 0, 매우 적음 15, 적음 30, 많음 65, 매우 많음 80)(`Vehicles.lua:146-157`) |
| `CarGasConsumption` | 차량 연료 소비량 | 1.0 | 1.0 | 소비량 배율(`Vehicles.lua:485`) |
| `CarGeneralCondition` | 차량의 상태 | 3 보통 | 3 보통 | 발견 차 부품 상태 |
| `CarDamageOnImpact` | 차량이 입는 손상 | 3 보통 | 3 보통 | 충돌 손상 배수(`BaseVehicle.crash`) |
| `DamageToPlayerFromHitByACar` | 차량이 플레이어에게 주는 피해량 | 1 없음 | 없음 | 차에 치인 플레이어 피해 |
| `TrafficJam` | 폐차 교통체증 | true | true | 큰길에 폐차 정체 |
| `CarAlarm` | 차량 도난방지 경보 발동 확률 | 3 적음 | 4 보통 | 8%(보통 15%)(`IsoChunk.AddVehicles_OnZone`) |
| `PlayerDamageFromCrash` | 차량 탑승 시 교통사고 피해 활성화 | true | true | 5-3 |
| `SirenShutoffHours` | 사이렌 재생 시간 | 0.0 | 0.0 | 0 = 자동으로 안 꺼짐 |
| `SirenEffectsZombies` | 좀비의 사이렌 소리 반응 여부 | true | true | 사이렌 100칸 |
| `RecentlySurvivorVehicles` | 생존자의 차량 | 2 적음 | 3 보통 | 10%(보통 30%, 많음 50%) |
| `KeyLootNew` | 열쇠 | 0.4 | 0.6 | 열쇠 배치 판정 한 번의 확률 = 값 × 25%(10%) |
| `AllowExteriorGenerator` | 외부에서 발전기 사용 가능 | true | true | 단전 뒤 주유기에 발전기 |
| `ElecShut` | (전기 끊김) | 2 | 2 | 14~30일 |

- `Apocalypse.lua:17, 36, 97, 107-129`, Java 선언은 `SandboxOptions` 122-235행.
- 메모: 질문에 나온 `CarAlarm` 의 화면 번역 키는 `CarAlarmFrequency` 다(`setTranslation("CarAlarmFrequency")`).

**그림 후보(6절)**: 라디얼 `vehicle_changeseats`, 계기판 `ignition_key_on`(열쇠 꽂힘). 실제 화면은 이 PC 에서 직접 찍는 것을 권장(맨 아래 메모).

## 7. 모드 영향

**사이트 한 줄**: 우리 모드 중 차에 영향을 주는 건 **Common Sense(쇠지렛대로 잠긴 차 문 따기)** 정도다. 나머지는 편의 기능이다.

| 모드 | 차량 관련 변화 | 근거 |
|---|---|---|
| Common Sense [B42.20+] (3750253491) | 쇠지렛대가 있으면 잠긴 차 옆에서 V → 문 따기(Pry). 설명 원문: "Pry open Doors, Windows and Vehicles with Crowbars". 3.5.0 부터 "Pry 옵션은 각 분류 메뉴로 이동", 2026-09-15 댓글 "차 옆에서 V 를 누르면 옵션이 뜬다". 3.5.2(7/13) 멀티 수정에 "따고 난 트렁크가 안 열림", "자물쇠가 고장 난 채 남아 차 안에 갇힘" 고침. 10/13 무렵 "차 문 따기 오류" 댓글 뒤 "already fixed". | `[웹]` https://steamcommunity.com/sharedfiles/filedetails/?id=3750253491 , 변경 기록 https://steamcommunity.com/sharedfiles/filedetails/changelog/3750253491 . 3750253491 파일은 이 PC 에 없어 코드 확인 못 함 |
| (참고) Common Sense 원본 (2875848298) 코드 | 차 밖 V 메뉴에 "Pry open" 칸(잠긴 문만, 후드 제외). 성공 판정은 좀도둑이면 80%, 아니면 `(100 − 180/힘 − 20)` 정도. 실패하면 샌드박스 옵션에 따라 20% 확률로 가까운 창문이 깨진다. 샌드박스 `PryVehicleDoors`·`ShatterVehicleWindows`(기본 켜짐), `WindowShatterChance` 20. | `[모드] <창작마당>\2875848298\mods\CommonSense\42.0\media\lua\client\ISUI\BB_CS_Tools.lua:85-147`, `BB_CS_TimedAction.lua:88-126`, `42.0\media\sandbox-options.txt`. **우리가 쓰는 판(3750253491)과 같은지는 미확인** |
| Common Sense 와 경보 | 3750253491 은 서버에 문 따기를 보낸 뒤 바닐라 문 열기(`ISOpenVehicleDoor`)를 그대로 부른다(개발자 답글 2026-07-29, 웹 조사). 그러면 바닐라 규칙대로 경보가 울린다(2-5). 원본 코드는 문을 직접 열어서 이 검사를 안 탄다. | 추정. 실제로 해 보지 않음 |
| Proximity Inventory B42.20+ (2847184718) | 차 안에서도 "근처" 탭이 생기고 제목에 " - 차량"이 붙는다. 손 닿는 좌석·글러브박스 물건을 한 탭에서 본다. 작성자 주석: 차량 지원을 막 켰다. | `[모드] 2847184718\mods\ProximityInventory\common\media\lua\client\ProximityInventory\ProximityInventory.lua:76-78, 327` |
| Skill Recovery Journal (2503622437) | 차량정비 경험치와 잡지로 배운 정비 지식이 기본 설정으로 복구된다(직업·특성으로 받은 지식과 시작 보너스는 제외). 운전 중(시동 켜고 움직이는 중)에는 일지를 못 쓴다. | `[모드] 2503622437\mods\Skill Recovery Journal\42.19\media\lua\shared\Skill Recovery Journal Action.lua:17-18`. 복구 규칙은 웹 조사(모드 코드 `RecoverCraftingSkills`, `RecoverRecipes`) |
| Better Sorting (2313387159) | 인벤토리 "차량 정비" 분류 이름이 "역학"으로 보일 수 있다. Hx 가 덮어쓰는지 미확인. | 웹 조사(모드 KO 번역 파일) |
| Hx's 좀보이드 통합 번역 (3040632900) | 바닐라 한국어를 덮어쓰므로 차량 메뉴 문구가 이 문서(바닐라 KO 기준)와 조금 다를 수 있다. 차이는 미확인. | `[웹]` 창작마당 설명 |
| Smarter Storage, Stack ALL, Mini Health Panel, WorldMap Name Symbols, 한글타이핑, Named VHS, Has Been Read, 라이브러리 2개 | 차량 사용에 영향 없음. Smarter Storage 는 차 보관함을 꾸미기 대상에서 뺀다(`isVehicleContainer`). Stack ALL 은 코드 미확인. | 웹 조사 + 받아진 모드 사본 |

- `<창작마당>` = `C:\Program Files (x86)\Steam\steamapps\workshop\content\108600`

## 8. 커뮤니티 꿀팁 (게임 파일과 대조)

| # | 팁 (사이트용) | 출처 | 게임 파일 대조 |
|---|---|---|---|
| 1 | 연비는 **올-터레인·랭 4000** 이 좋고 **다트**가 가장 나쁘다 | Reddit 2026-10-15 (B42.21.0 코드 분석) https://www.reddit.com/r/projectzomboid/comments/1x68czg/ | **일치**. 무게 배수 `Vehicles.lua:465`(1000 이 최적), 다트 650·품질 60 |
| 2 | 짐 많이 싣는 차: **스텝 승합차 160, 밴·구급차·불드라이버 130, D6 110**. 불드라이버는 가장 시끄럽다(120) | PZwiki Vehicle(42.16.0) https://pzwiki.net/wiki/Vehicle , Reddit 2026-08-03 https://www.reddit.com/r/projectzomboid/comments/1ve850d/ | **일치**. 각 차 `capacity`, `engineLoudness = 120`(`vehicle_pickupvan_template.txt`) |
| 3 | 배선 따기 전에 **점화장치·시체·주변**부터 열쇠를 찾아라 | PZwiki Survival Guide(42.20.4) https://pzwiki.net/wiki/Survival_Guide | **일치**. 2-2 의 배치 순서 |
| 4 | 열쇠는 **며칠 뒤에** 생기기도 한다. 단, 한 번 문을 연 차는 다시 안 생긴다 | Reddit 2026-10-06 https://www.reddit.com/r/projectzomboid/comments/1wyyrfo/ | **일치**. `BaseVehicle.addToWorld` 에서 다시 굴림, `isPreviouslyEntered` 면 제외 |
| 5 | **계산대**에서 차 열쇠가 자주 나온다 | Reddit 2026-08-09 https://www.reddit.com/r/projectzomboid/comments/1vjhk90/ | **일치**. `Distributions.lua:183-187` `"CarKey", 2`. 어느 차 열쇠인지는 미확인 |
| 6 | 창문은 **운전석 말고 조수석·뒷자리**를 깨라(운전석이 뚫리면 좀비에게 물린다) | PZwiki Vehicle, Reddit 2026-10-15 https://www.reddit.com/r/projectzomboid/comments/1x6cb6m/ | **코드와 모순 없음**. 깬 창의 문으로 잠금을 풀고(`canUnlockDoor`), 다른 문으로 타서 운전석으로 옮길 수 있음(`processEnter`). "운전석 창이 뚫리면 물린다"는 코드 미확인 |
| 7 | 배선 따기 성공률은 **엔진 품질과 전기공학**으로 정해진다. 좀도둑이라고 오르지 않는다 | PZwiki Vehicle#Hot-wiring | **일치**. `BaseVehicle.tryHotwire` |
| 8 | 단전 뒤 주유소는 **발전기를 연결**해야 쓴다. 쓸 때만 켜라 | Reddit 2026-01-10 https://www.reddit.com/r/projectzomboid/comments/1q8yhfx/ , PZwiki Gas pump | **일치**. `ISVehicleMenu.lua:1088` |
| 9 | 기름 빼기는 **고무 호스 + 통**이 필요하다. 호스는 차고·창고·헛간·정비소에서 나온다 | 로딩 화면 팁(PZwiki Quick tips 42.13.0), Reddit 2026-08-24 https://www.reddit.com/r/projectzomboid/comments/1vwohl1/ | 조건 **일치**(`ISVehicleMenu.lua:1070-1084`). 호스가 나오는 장소는 미확인 |
| 10 | 정비 레벨은 **폐차장의 여러 차**로 올려라(같은 차 같은 부품은 24시간에 한 번) | PZwiki Mechanics(42.18.0) https://pzwiki.net/wiki/Mechanics | **일치**. `IsoPlayer.addMechanicsItem`, `updateMechanicsItems`. PZwiki 의 "실패해도 0.25 XP"는 미확인 |
| 11 | 경보 달린 차는 열쇠 없이 처음 열면 **반드시** 울린다. 안 잠긴 차는 경보가 없다 | Reddit/PZwiki + 웹 조사 | **일치**. `ISOpenVehicleDoor.lua:80-92`, `Vehicles.lua:166-169` |
| 12 | 같이 다닐 땐 **차 한 대**로(기름 절반, 소음 절반) | PZwiki Survival Guide | 코드와 모순 없음(소음은 차마다 따로 남) |

- 버린 팁
  - "배선 따기가 점화장치를 망가뜨린다"(Reddit 댓글): 42.21 코드에서 망가짐 표시를 검사하지 않는다(2-3).
  - "호스는 기본 인벤토리에 있어야 한다"(Reddit 댓글): 코드가 가방 속까지 찾는다.
  - "빈 기름통만 있으면 기름을 뺄 수 있다": B41 자료.

## 9. 아이콘 위치 (아이템)

**사이트 한 줄**: (아이콘은 위 항목 옆에 작은 그림으로 쓰기 좋다.) 추출은 하지 않았다. 아이템 스크립트의 `Icon = X` 는 텍스처 `Item_X` 를 쓴다.

| 아이템 (한국어) | 아이템 ID | 텍스처 이름 | 위치 | 크기 |
|---|---|---|---|---|
| 차 열쇠 | `Base.CarKey` | `Item_CarKey` | `media\texturepacks\UI2.pack` | 28×26 |
| 열쇠고리 | `Base.KeyRing` | `Item_KeyRing` | UI2.pack | 31×29 |
| 기름통 | `Base.PetrolCan` | `Item_Petrol` | `media\texturepacks\UI.pack`(옛 형식 팩) | 미확인 |
| 제리캔 | `Base.JerryCan` | `Item_JerrycanMilitary` | UI2.pack | 18×32 |
| 고무 호스 | `Base.RubberHose` | `Item_RubberHose` | UI2.pack | 28×26 |
| 차량 배터리 | `Base.CarBattery1~3` | `Item_CarBattery` | UI2.pack | 32×28 |
| 차량 배터리 충전기 | `Base.CarBatteryCharger` | `Item_CarBatteryCharger` | UI2.pack | 32×30 |
| 타이어 | `Base.NormalTire1` 등 | `Item_CarTire` | UI2.pack | 23×30 |
| 렌치 | `Base.Wrench` | `Item_Wrench` | UI2.pack | 29×30 |
| 십자 휠 렌치 | `Base.LugWrench` | `Item_LugWrench` | UI2.pack | 29×29 |
| 잭 | `Base.Jack` | `Item_CarJack` | UI2.pack | 31×24 |
| 타이어 펌프 | `Base.TirePump` | `Item_TirePump` | UI2.pack | 25×32 |
| 스크류드라이버 | `Base.Screwdriver` | `Item_Screwdriver`(UI.pack), `Item_Screwdriver_Blue`(UI2.pack) | 두 팩 | 미확인 |
| 쇠지렛대 | `Base.Crowbar` | `Item_Crowbar`(UI.pack), `Item_Crowbar_Forged`(UI2.pack) | 두 팩 | 미확인 |
| 용접용 프로판 토치 | `Base.BlowTorch` | `Item_BlowTorch` | UI2.pack | 32×27 |
| 용접 마스크 | `Base.WeldingMask` | `Item_WeldingMask` | UI2.pack | 27×27 |
| 예비 엔진 부품 | `Base.EngineParts` | `Item_EngineParts` | UI2.pack | 32×32 |
| 라이네스 설명서 3종 | `Base.MechanicMag1~3` | `Item_MagazineMechanic1~3` | UI2.pack | 32×31 |
| 트렁크 / 연료 탱크 / 글러브박스 | `Base.NormalTrunk1` 등 | `Item_CarTrunk` / `Item_CarGastank` / `Item_GloveBox` | UI2.pack | 31×29 / 32×22 / 30×28 |
| 머플러 / 좌석 / 브레이크 / 서스펜션 / 문 | 각 부품 | `Item_CarMuffler` / `Item_CarSeat` / `Item_CarBrakes` / `Item_CarSuspension` / `Item_CarDoorFront` | UI2.pack | 29×27 / 25×32 / 27×29 / 31×32 / 24×25 |
| 발전기 | `Base.Generator` | `Item_Generator` | UI2.pack | 32×32 |

- 아이템 정의: `[스크립트] items\key.txt`(CarKey), `container.txt`(KeyRing), `normal.txt`, `drainable.txt`, `weapon.txt`, `clothing.txt`, `literature.txt`.
- UI2.pack 은 PZPK 형식이다. 저장소의 `scripts/extract-character.py` 의 `read_pack` 으로 이름과 크기를 읽었다(읽기만 함). UI.pack 과 Mechanics.pack 은 옛 형식이라 이 함수로 못 읽고, 이름만 문자열로 확인했다.

## 10. 확인 못 한 것

- Common Sense 3750253491 의 실제 코드(이 PC 에 없음): 차 문 따기의 성공 조건, 경보 발동 여부, 차 따기 전용 샌드박스 옵션, 한국어 메뉴 이름.
- Hx 통합 번역이 바꾸는 차량 문구. 이 문서의 한국어 표기는 바닐라 42.21 KO 기준이다.
- `SpeedLimit`(70) 의 정확한 효과.
- 일반 전리품(계산대·허리 가방)으로 나오는 차 열쇠가 어느 차 것인지.
- 니알라처럼 차 파일에 트렁크 용량이 없는 차의 정확한 용량(부품 아이템 선택 방식 미확인).
- 경보가 50초보다 일찍 끝나는 다른 조건(배터리 0 말고).
- 열쇠가 문짝에 꽂혀 생기는 경로(PZwiki 주장).
- 트레일러가 급커브에서 풀리는 조건(42.20.0 패치노트만 확인).
- PZwiki "정비 실패해도 0.25 XP", "호스가 나오는 장소" 같은 수치.
- 생존 가이드의 차량 페이지가 키 이름(%1 등)에 어떤 키를 넣는지(정의 위치를 못 찾음. 번역 문장만 확인).

## 그림 후보

### 라이선스 메모

- **게임 파일 그림**(표 A, B): The Indie Stone 저작물이다. 비상업 팬 사이트에서 쓰려면 TIS 약관 2.2 를 따른다(비상업, 정해진 감사 문구와 약관 링크 표시). https://projectzomboid.com/blog/support/terms-conditions/
- **PZwiki**: 글은 **CC BY-NC-SA 3.0** 이다. 요청서의 "CC BY-SA" 는 틀렸다. 그리고 "개발자 소유 그림·아트·설정은 제외"라고 적혀 있다. 확인: https://pzwiki.net/wiki/PZwiki:Copyrights (2025-09-25 수정판).
  - 게임 스크린샷 파일은 페이지마다 `The Indie Stone` 라이선스 틀이 붙어 있다("copyrighted by The Indie Stone and used freely on this wiki with permission"). CC 라이선스가 아니므로 TIS 약관을 따라야 한다.
- 버전 판단: B42 unstable 이 2024-12-17 에 나왔으니, 그 전에 올라온 화면은 B41 이전 화면이다.
- 이미지는 내려받지 않았다.

### A. 게임 파일 안의 UI 그림 (계기판·라디얼·정비)

| 쓸 곳 | 그림 | 위치 (팩 + 텍스처 이름, 또는 낱개 파일) | 크기 | 코드에서 쓰는 곳 |
|---|---|---|---|---|
| 계기판 전체 배경 | 계기판 | UI2.pack `dashboard` (Lua 경로 `media/ui/vehicles/dashboard.png`) | 552×121 | `ISVehicleDashboard.lua:587` |
| 연료 | 연료 게이지 가득/적음/빔 | UI2.pack `rj-vehicle_fuelguage-full`·`-low`·`-empty` | 80×80 | 같은 파일 588-590 |
| 엔진·속도 | 엔진 온도계, 속도계 | UI2.pack `rj-vehicle_engineguage`, `vehicle_spedometer` | 127×66 | 591-592 |
| 경고등 | 엔진 이상, 문 잠김, 전조등, 히터, 에어컨, 배터리 부족, 트렁크, 정속 주행 | UI2.pack `icon_enginetrouble_light`, `icon_doorslocked_light`, `icon_headlights_light`, `icon_heating_light`, `icon_airconditioning_light`, `icon_lowbattery_light`, `icon_trunk_light`, `speedregulator_light` (그 밖에 `icon_lowgas_light`, `icon_ignition_light`) | 14~28px | 575-586 |
| 시동·열쇠 | 열쇠 구멍(빔), 열쇠 꽂힘, 시동 켜짐, 배선 딴 상태 | UI2.pack `ignition`, `ignition_key_off`, `ignition_key_on`, `ignition_hotwired` | 35×34 (배선 35×61) | 580-583 |
| 열쇠 없음 표시 | 머리 위 "열쇠 없음" | UI2.pack `CarKey_none` (`media/ui/CarKey_none.png`) | 30×28 | `BaseVehicle.tryStartEngine` |
| 라디얼(차 안) | 좌석 이동, 시동 켜기/끄기, 전조등 켜기/끄기, 히터(뜨거움/차가움), 경적, 경광등, 사이렌, 라디오, 창문 열기/닫기, 문 잠그기, 정비, 잠자기, 내리기 | UI2.pack `vehicle_changeseats`, `vehicle_ignitionON`/`OFF`, `vehicle_lightsON`/`OFF`, `vehicle_temperatureHOT`/`COLD`, `vehicle_horn`, `vehicle_lightbar`, `vehicle_siren`, `vehicle_speakersON`, `vehicle_windowOPEN`/`CLOSED`, `vehicle_lockdoors`, `vehicle_repair`, `vehicle_sleep`, `vehicle_exit` | 43~64px | `ISVehicleMenu.lua:85-228` |
| 라디얼(차 밖) | 창문 부수기, 주유기로 넣기, 기름 넣기, 기름 빼기 | 낱개 `media\ui\vehicles\vehicle_smash_window.png`, `vehicle_refuel_from_pump.png`, `gas_refuel.png`, `gas_siphon.png` (그 밖에 `vehicle_add_gas.png`, `vehicle_siphon_gas.png`) | 64×64 | `ISVehicleMenu.lua:349, 1065, 1077, 1092` |
| 트레일러 | 연결 / 분리 | 낱개 `media\ui\ZoomIn.png` / `ZoomOut.png` | 64×64 | `ISVehicleMenu.lua:559, 565` |
| 정비 화면 | 차 위에서 본 부품 그림(차체·타이어·문 등 부위별 조각) | 낱개 `media\ui\vehicles\mechanic overlay\<접두어>_*.png` 314개. 예: `4door_base.png`(263×600), `suv_base.png`, `van_base.png`, `truck_base.png`. 같은 이름이 `Mechanics.pack` 에도 있음 | 263×600 등 | `ISCarMechanicsOverlay.lua:3-56`(니알라·대시 엘리트=`4door_`, 웨건=`stationwagon_`, 다트=`smallcar_`, 코세트·랭=`sportscar_`, 올-터레인=`suv_`, 랜처=`offroad_`, D6·불드라이버=`truck_`, 밴·스텝 승합차=`van_`, 트레일러=`utilitytrailer_`) |
| 생존 가이드 | 차량 장 그림, 분류 아이콘 | 낱개 `media\ui\survival_guide_spiffo\spiffo_vehicle.png`(309×350), `category_vehicles.png`(32×32) | – | `[번역] SurvivalGuide.json:182-183` |
| 키 안내 | 키보드 키 그림 | 게임 파일에서 찾지 못함. 사이트에서 키 모양을 직접 그리는 편이 낫다 | – | – |

### B. 게임 파일 안의 아이템 아이콘

9절 표 참고(차 열쇠, 기름통, 제리캔, 호스, 배터리, 충전기, 타이어, 렌치, 십자 휠 렌치, 잭, 타이어 펌프, 스크류드라이버, 쇠지렛대, 토치, 마스크, 엔진 부품, 잡지, 부품류, 발전기).

### C. 웹의 실제 게임 화면 (URL 만)

| 화면 | 파일 페이지 | 원본 이미지 URL | 버전 | 라이선스 | 비고 |
|---|---|---|---|---|---|
| 계기판(연료 게이지) | https://pzwiki.net/wiki/File:VehicleDashboard.png | https://pzwiki.net/w/images/c/cb/VehicleDashboard.png | 최신판 2023-11-26, B41 | TIS | 554×113. 42.21 텍스처(552×121)와 크기가 거의 같지만 같은 그림인지는 미확인 |
| 정비 화면 | https://pzwiki.net/wiki/File:VehicleMechanics.png | https://pzwiki.net/w/images/b/b7/VehicleMechanics.png | 2018-04, 구버전 | TIS | 800×600. B42 와 다를 가능성이 큼 |
| 라디얼(차 안) | https://pzwiki.net/wiki/File:VehicleRadialMenu.png | https://pzwiki.net/w/images/a/a6/VehicleRadialMenu.png | 2018-06, 구버전 | TIS | 250×250 |
| 라디얼(차 밖) | https://pzwiki.net/wiki/File:VehicleRadialMenuExterior.png | https://pzwiki.net/w/images/7/78/VehicleRadialMenuExterior.png | 2018-11, 구버전 | TIS | 250×250 |
| 주유기로 넣기 | https://pzwiki.net/wiki/File:VehicleGas1.png | https://pzwiki.net/w/images/d/de/VehicleGas1.png | 2024-09, B41 | TIS | 516×511 |
| 기름통으로 넣기 | https://pzwiki.net/wiki/File:VehicleGas2.png | https://pzwiki.net/w/images/8/82/VehicleGas2.png | 2024-09, B41 | TIS | 516×511 |
| 빈 주유기(품절 표지) | https://pzwiki.net/wiki/File:Out_of_gas_generic.png | https://pzwiki.net/w/images/8/88/Out_of_gas_generic.png | 2025-02, **B42** | TIS | 800×588 |
| 발전기 정보 창 | https://pzwiki.net/wiki/File:Generator_UI_B42.png | https://pzwiki.net/w/images/0/00/Generator_UI_B42.png | 2025-11, **B42** | TIS | 386×249 |
| 차로 차 끌기 | https://pzwiki.net/wiki/File:VehicleTow.png | https://pzwiki.net/w/images/8/80/VehicleTow.png | 2024-09, B41 | TIS | 800×509 |
| 가축 트레일러 | https://pzwiki.net/wiki/File:Cow-in-livestock-trailer.jpg | https://pzwiki.net/w/images/8/8f/Cow-in-livestock-trailer.jpg | 2026-09-21, **B42.2x** | TIS | 800×450 표시 |
| 차 열쇠가 보이는 장면 | https://pzwiki.net/wiki/File:VehicleKey.png | https://pzwiki.net/w/images/a/a6/VehicleKey.png | 최신판 2024-09, B41 | TIS | 800×517 |
| 차 열쇠 아이콘 | https://pzwiki.net/wiki/File:CarKey.png | https://pzwiki.net/w/images/8/81/CarKey.png | 2024-12-18, B42 | TIS | 게임 파일 `Item_CarKey` 와 같은 것 |
| 고무 호스 아이콘 | https://pzwiki.net/wiki/File:RubberHose.png | https://pzwiki.net/w/images/3/37/RubberHose.png | 2024-12-18, B42 | TIS | 32px |
| 배선 딴 시동 아이콘 | https://pzwiki.net/wiki/File:Ignition_hotwired.png | https://pzwiki.net/w/images/f/f8/Ignition_hotwired.png | 2024-08 | TIS | 게임 파일 `ignition_hotwired` 와 같은 것 |
| 트레일러 견인(외부 가이드) | https://steamcommunity.com/sharedfiles/filedetails/?id=3642693916 | https://images.steamusercontent.com/ugc/13373478841404482086/90DB7B49CA9DF585208D0CBADAAE256305E5D694/ | 2026-01, B42 | **라이선스 불명, 사용 전 허락 필요** | 가이드 끝에 치트 프로그램 홍보가 있어 출처로 부적합 |

- 표의 스크린샷 11개(계기판, 정비 화면, 라디얼 2개, 주유 2개, 빈 주유기, 발전기, 차 끌기, 가축 트레일러, 열쇠 장면)는 2026-10-18 에 파일 페이지를 직접 열어 원본 URL, 라이선스 틀, 업로드 날짜(최신판)를 확인했다. 아이콘 3개와 Steam 가이드는 하위 조사 결과다.
- 트렁크·글러브박스 인벤토리, 배선 따기 진행 화면은 PZwiki 에 쓸 만한 스크린샷이 없다.

### 메모: 직접 찍기를 권장

- 이 PC 에 42.21 이 깔려 있다. 정비 화면, V 메뉴(차 안·밖), 배선 따기, 주유 메뉴, 계기판, 트렁크 인벤토리는 직접 찍는 것이 가장 낫다. 버전이 맞고, 한국어 메뉴가 그대로 보이고, 라이선스도 TIS 감사 문구 하나로 정리된다.
- 기존 `web/src/data/shots.json` 방식(실제 화면 사진 목록)과도 맞다.
