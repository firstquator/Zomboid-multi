# 플레이 꿀팁 조사 기록 (42.21, 2026-10-18 확인)

사이트에 넣을 "플레이 꿀팁" 섹션의 재료다. Project Zomboid 를 처음 같이 하는 친구들이 읽는다고 보고 골랐다.

## 기준과 표기

- 게임: **42.21.0 (public stable)**. B42(특히 42.13 이후, 멀티가 들어간 42.20 이후) 기준이다. B41 에만 맞는 내용은 넣지 않았고, 바뀐 것은 "B41 에서 바뀜"이라고 적었다.
- 차량 팁과 직업·특성 조합은 다른 조사가 맡아서 넣지 않았다.
- 우리 서버 설정을 반영했다.
  - `data/mods.json` 의 `vanilla`: 미니맵 켜짐(`Map.AllowMiniMap=true`), 지도에 모든 플레이어 표시(`MapRemotePlayerVisibility=4`), 기술 서적 한 쪽당 0.1분(`MinutesPerPage=0.1`).
  - 모드 14개(주변 상자 보기, Common Sense, Mini Health Panel, Has Been Read, 스킬 보존 일지 등). 모드가 이미 풀어 주는 불편은 "모드로 해결됨"으로 적거나 모드 쓰는 요령으로 바꿨다.
  - 서버 ini: `PVP=false`, `PauseEmpty=true`, 잠 설정 꺼짐(`SleepAllowed=false`, `SleepNeeded=false`, 멀티 기본값). 나머지는 42.21 기본값(`docs/research/hosting.md` 부록 A).
  - 샌드박스: 위 세 가지 말고는 기본 프리셋 그대로. 게임의 기본 프리셋은 `PZ/media/lua/shared/Sandbox/SandboxVars.lua` 가 불러오는 `Apocalypse.lua` 다.
- 사이트에 이미 있는 "시작 직후 할 일"(무기 먼저, 가방 챙기기, 물 받아 두기, 상처는 바로, 책은 보이는 대로, 스킬 보존 일지)과 겹치는 것은 빼거나 더 자세한 쪽으로 바꿨다.
- 줄임말
  - `PZ/` = `C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\` (42.21 설치본)
  - `KO/` = `PZ/media/lua/shared/Translate/KO/` (한국어 게임 표기), `EN/` = 같은 경로의 영어
  - `WS/<번호>/` = `C:\Program Files (x86)\Steam\steamapps\workshop\content\108600\<번호>\` (이 PC 에 받아진 창작마당 모드)
  - `Apocalypse.lua` = `PZ/media/lua/shared/Sandbox/Apocalypse.lua` (샌드박스 기본값)
  - `keyBinding.lua` = `PZ/media/lua/shared/keyBinding.lua` (기본 키)
  - `ini 기본값` = `docs/research/hosting.md` 부록 A (42.21 이 만든 servertest.ini)
- 키 표기: `기본 키` 「한국어 게임 표기」. 한국어 표기는 바닐라 `KO/` 기준이다. 우리 서버는 Hx 통합 번역을 쓰므로 실제 화면 문구가 조금 다를 수 있다.
- 아이콘: 아이템 스크립트 이름 · 스크립트의 `Icon` 값 → 텍스처 이름 `Item_<Icon>`. `Icon` 이 없고 `IconsForTexture` 만 있는 아이템은 그 첫 값을 적었다. 텍스처는 모두 `PZ/media/texturepacks/UI.pack` 또는 `UI2.pack` 안에 있는 것을 확인했다. 무들·버튼 그림은 `PZ/media/ui/` 아래 PNG 경로를 적었다.
- B42 확인 칸: "확인(게임 파일)"은 42.21 설치본에서 직접 봤다는 뜻, "확인(웹)"은 B42 버전이 적힌 웹 자료로 확인했다는 뜻, "미확인"은 못 했다는 뜻이다.

---

## 1. 기본 조작과 단축키

### 1-1. 걷기, 달리기, 전력 질주
- **설명**: 그냥 걸으면 가장 조용하다. `Shift` 를 누르고 있으면 달리고, `Alt` 를 누르고 있으면 전력 질주한다. 전력 질주는 지구력이 빨리 닳고 발소리도 걷기의 두 배라서 도망칠 때만 쓴다. 두꺼운 옷을 많이 껴입으면 "전력질주할 수 없음" 무들이 뜬다.
- **키**: `W` `A` `S` `D` 「앞으로/뒤로/왼쪽으로/오른쪽으로 이동」, `왼쪽 Shift` 「달리기」, `왼쪽 Alt` 「전력질주」
- **아이콘**: 무들 `PZ/media/ui/Moodle_Icon_CantSprint.png`(전력질주할 수 없음), 지구력 무들 `PZ/media/ui/Moodles/64/Status_DifficultyBreathing.png`
- **근거**: `keyBinding.lua`(RUN = KEY_LSHIFT, SPRINT = KEY_LMENU), `KO/UI.json`(UI_optionscreen_binding_Run, _Sprint), `KO/Moodles.json`(Moodles_CantSprint "전력질주할 수 없음", 설명 "무거운 옷을 벗는 것을 고려해보세요."). 발소리 크기(전력질주 14, 걷기 7, 웅크려 걷기 3.5): https://pzwiki.net/wiki/Noise (42.13.1)
- **B42**: 확인(게임 파일). 소음 수치는 확인(웹, 42.13.1)

### 1-2. 공격은 "조준한 채 클릭", 밀치기는 Space
- **설명**: 무기를 들고 마우스 오른쪽(또는 `Ctrl`)을 누른 채 왼쪽을 클릭하면 휘두른다. `Space` 는 조준 없이 바로 밀친다. 쓰러진 좀비 위에서 `Space` 를 누르면 밟는다. 쓰러진 좀비 쪽으로 휘두르면 기본 설정에서 알아서 바닥 공격이 된다.
- **키**: `마우스 오른쪽` 또는 `왼쪽 Ctrl` 「조준하기」, `마우스 왼쪽` 「공격/선택」, `Space` 「밀치기/밟기」, `왼쪽 Alt` 「수동으로 바닥 공격」(설정 「엎드리거나 서 있는 공격 자동으로 인지」를 껐을 때만 필요)
- **아이콘**: `Base.BaseballBat` · Icon `BaseballBat` → `Item_BaseballBat`
- **근거**: `keyBinding.lua`(AIM = KEY_LCONTROL, alt = Mouse.RMB / ATTACK_CLICK = Mouse.LMB / MELEE = KEY_SPACE / MANUAL_FLOOR_ATTACK = KEY_LMENU), `KO/UI.json`(binding_Melee "밀치기/밟기"), `KO/IG_UI.json`(IGUI_ToggleAutoProneAtk, _Tooltip), `PZ/media/lua/client/OptionScreens/MainOptions.lua`(2201행 근처). 자동 바닥 공격: https://pzwiki.net/wiki/Survival_Guide (42.20.4)
- **B42**: 확인(게임 파일)

### 1-3. 웅크리기(C)로 살금살금
- **설명**: `C` 를 누르면 웅크려 걷는다. 느리지만 발소리가 걷기의 절반이고 좀비가 알아채는 거리도 줄어든다. 안에 뭐가 있는지 모르는 집에 들어갈 때, 좀비 무리 옆을 지나갈 때 쓴다.
- **키**: `C` 「웅크리기」
- **아이콘**: (아이템 없음) 화면 캡처 후보 없음
- **근거**: `keyBinding.lua`(CROUCH = KEY_C), `KO/UI.json`(binding_Crouch). 소음과 감지 거리: https://pzwiki.net/wiki/Noise (42.13.1), https://pzwiki.net/wiki/Sneaking (42.18)
- **B42**: 확인(게임 파일, 웹)

### 1-4. 무기는 벨트에 차고 숫자 키로 꺼내기
- **설명**: 무기나 손전등을 우클릭해서 「부착하기」로 벨트나 등에 걸어 두면 화면 아래 단축키 칸에 들어간다. 그다음부터는 `1`~`8` 로 바로 꺼내 든다. 싸움이 붙었을 때 가방을 뒤질 필요가 없다.
- **키**: `1`~`8` 「단축키 칸 1~8」, 우클릭 메뉴 「부착하기」, 칸 이름 「왼쪽 벨트」「오른쪽 벨트」「등 뒤」
- **아이콘**: `Base.Belt2` · Icon `Belt` → `Item_Belt`, `Base.Hammer` · IconsForTexture `Hammer` → `Item_Hammer`
- **근거**: `keyBinding.lua`(HOTBAR_1~8 = KEY_1~8), `PZ/media/lua/client/Hotbar/ISHotbar.lua`(ContextMenu_Attach), `KO/ContextMenu.json`(ContextMenu_Attach "부착하기"), `KO/IG_UI.json`(IGUI_HotbarAttachment_SmallBeltLeft/Right, _Back)
- **B42**: 확인(게임 파일)

### 1-5. 자주 여는 창과 E·F 키
- **설명**: `I` 소지품, `H` 상태창(다친 곳과 치료), `L` 기술, `J` 정보, `P` 옷 방어도, `B` 제작창, `F1` 생존 지침서. 건축 창은 기본 키가 없어서 화면 왼쪽 아이콘 줄의 건축 버튼(망치 그림)으로 연다. `E` 는 문·창문 열기인데, 창문 앞에서 길게 누르면 넘는다. `F` 는 손전등을 꺼내 들거나 켜고 끈다.
- **키**: `I` 「소지품 창 전환」, `H` 「상태 창 전환」, `L` 「기술 창 전환」, `J` 「정보 창 전환」, `P` 「옷 방어도 창 전환」, `B` 「제작 창 전환」, `F1` 「생존 지침서 전환」, `E` 「상호작용」, `F` 「조명 아이템 장착/켬/끔」. 「건축 창 전환」은 기본 키 없음
- **아이콘**: 왼쪽 아이콘 줄 그림 `PZ/media/ui/Sidebar/64/` 의 `Inventory_On_64.png`(소지품창), `Heart_On_64.png`(상태창), `Carpentry_On_64.png`(제작창), `Build_On_64.png`(건축), `Map_On_64.png`(지도), `Search_On_64.png`(구역 탐색)
- **근거**: `keyBinding.lua`(TOGGLE_INVENTORY I, TOGGLE_HEALTH_PANEL H, TOGGLE_SKILL_PANEL L, TOGGLE_INFO_PANEL J, TOGGLE_CLOTHING_PROTECTION_PANEL P, CRAFTING_UI B, BUILDING_UI 없음, TOGGLE_SURVIVAL_GUIDE F1, INTERACT E, LIGHT_SOURCE F), `PZ/media/lua/server/XpSystem/XpUpdate.lua`(132~149행, B 로 제작창), `PZ/media/lua/client/ISUI/ISEquippedItem.lua`(왼쪽 아이콘 줄 버튼), `KO/UI.json`, `KO/IG_UI.json`(IGUI_CraftingTooltip "제작창"). E 짧게 열기·길게 넘기: https://pzwiki.net/wiki/Survival_Guide (42.20.4)
- **B42**: 확인(게임 파일). E 길게 누르기는 확인(웹)

### 1-6. 지도(M)와 미니맵, 밤에는 불빛이 있어야 보인다
- **설명**: `M` 을 짧게 누르면 세계 지도가 열린다. 0.5초 넘게 누르고 있으면 원형 메뉴가 뜨고 「보기 / 숨기기 - 지도창」으로 미니맵을 켜고 끈다(우리 서버는 미니맵을 켜 둠). 기본 설정상 광원이 없으면 지도도 미니맵도 못 읽는다. 밤이나 어두운 방에서는 손전등을 켜고 본다.
- **키**: `M` 「지도 열고 닫기」(길게 누르면 원형 메뉴: 「보기 / 숨기기 - 세계 지도」「보기 / 숨기기 - 지도창」)
- **아이콘**: `Base.MuldraughMap` · Icon `Map` → `Item_Map`, 지도 버튼 `PZ/media/textures/worldMap/Map_On.png`
- **근거**: `PZ/media/lua/client/ISUI/Maps/ISWorldMap.lua`(1633~1720행: 누른 지 500ms 가 지나면 원형 메뉴, 떼면 세계 지도), `PZ/media/lua/client/ISUI/Maps/ISMiniMap.lua`(690행 NeedsLight), `Apocalypse.lua`(Map.MapNeedsLight = true), `KO/Sandbox.json`(Sandbox_MapNeedsLight "지도 읽기에 광원 필요"), `KO/IG_UI.json`(IGUI_WorldMap_Toggle, IGUI_MiniMap_Toggle), `data/mods.json`(Map.AllowMiniMap = true). `docs/research/hosting.md` 가 "미니맵 단축키 미확인"으로 남긴 항목의 답이다.
- **B42**: 확인(게임 파일)

---

## 2. 전투

### 2-1. 한 마리는 밀쳐 넘어뜨리고 밟는다
- **설명**: 혼자 오는 좀비는 `Space` 로 밀쳐 넘어뜨리고, 머리 쪽에 서서 `Space` 로 밟는다. 무기가 닳지 않고, 밟는 동안 좀비는 못 일어난다. 다리 쪽에서 밟으면 잘 안 죽는다. 신발이 튼튼할수록 세게 밟는다(작업화·등산화·군화가 가장 셈). 근처에 다른 좀비가 있으면 밟는 사이에 물리니 한 마리일 때만 쓴다.
- **키**: `Space` 「밀치기/밟기」
- **아이콘**: `Base.BaseballBat` → `Item_BaseballBat` (밟기 전용 아이템 없음)
- **근거**: `keyBinding.lua`(MELEE = KEY_SPACE), https://pzwiki.net/wiki/Bare_Hands (42.10, 밀치기 피해 0·밟기 위치 판정), https://pzwiki.net/wiki/Clothing (42.18, 신발별 StompPower: 운동화 1.8, 일반 신발 2.1, 작업·등산·군화 2.5), https://pzwiki.net/wiki/Health (42.15.3, 밟기는 근육 긴장 0.3배)
- **B42**: 확인(웹, 42.10~42.18)

### 2-2. "지침" 무들이 뜨면 물러나서 숨 돌리기
- **설명**: 휘두를 때마다 지구력이 준다. 화면 오른쪽에 「지침」 무들이 뜨면 공격이 확 약해진다(1단계부터 근접 피해 절반). 싸우다 지치면 뒤로 빠져 바닥이나 의자에 앉아 쉰다. 걸으면서는 거의 회복이 안 된다. 짐이 무게 한도를 넘으면 회복이 줄고, 1.5배를 넘으면 아예 멈춘다.
- **키**: (없음)
- **아이콘**: 지구력 무들 `PZ/media/ui/Moodles/64/Status_DifficultyBreathing.png`, 무거움 무들 `PZ/media/ui/Moodles/64/Status_HeavyLoad.png`
- **근거**: `KO/Moodles.json`(Moodles_Endurance_lvl1~4 "지침~기진맥진", Moodles_HeavyLoad), 무들 그림 대응은 `PZ/projectzomboid.jar` 의 `zombie/ui/MoodleTextureSet.class` 문자열 순서. 단계별 효과(1단계 근접 피해 -50%, 2단계 전력질주 불가, 3단계 달리기 불가): https://pzwiki.net/wiki/Endurance (42.12.3). 짐 무게: https://pzwiki.net/wiki/Heavy_load (42.12.3)
- **B42**: 확인(웹, 42.12.3)

### 2-3. 무기는 닳는다: 여분, 수리, 날 갈기
- **설명**: 무기는 맞힐 때마다 조금씩 상태가 떨어지고 0이 되면 부서진다. 여분 무기를 하나 더 차고 다닌다. 상한 무기는 제작창에서 「강력 접착 테이프로 수리하기」 같은 수리 제작법으로 고친다(실패하면 오히려 상한다). 칼·도끼 같은 날 무기는 무뎌지면 약해지니, 숫돌을 갖고 다니면서 무기를 든 채 `R` 로 날을 간다. 「물건관리」 기술이 오르면 덜 닳고 수리도 잘 된다.
- **키**: `R` 「무기 날 갈기」(날 무기를 손에 들었을 때)
- **아이콘**: `Base.Whetstone` · Icon `Whetstone2` → `Item_Whetstone2`, `Base.DuctTape` · Icon `DuctTape` → `Item_DuctTape`, `Base.Glue` · Icon `Glue` → `Item_Glue`
- **근거**: `PZ/media/scripts/generated/recipes/recipes_fixing.txt`(FixWithDuctTape 외 수리 7종, SharpenBlade = 숫돌, SharpenBladePoorlyWithFile = 줄, MakeCrudeWhetstone = 돌 2개로 간이 숫돌·물건관리 2에 자동 습득), `PZ/media/lua/client/ISUI/ISFirearmRadialMenu.lua`(385행, R 로 날 갈기), `keyBinding.lua`(SHARPEN_WEAPON = KEY_R), `KO/Recipes.json`(FixWithDuctTape "강력 접착 테이프로 수리하기", SharpenBlade "날 갈기", MakeCrudeWhetstone "간이 숫돌 만들기"), `KO/Tooltip.json`(Tooltip_weapon_Sharpness "날카로움"). 닳는 확률과 수리 실패 공식: https://pzwiki.net/wiki/Condition (42.20.4), https://pzwiki.net/wiki/Maintenance (42.20.4). R 키는 42.13 에 생김: https://pzwiki.net/wiki/Build_42.13.0
- **B42**: 확인(게임 파일, 웹). 날카로움과 R 키는 B42 에서 생김

### 2-4. 여러 마리는 줄 세워서, 등 뒤는 비우지 않기
- **설명**: 둘 이상이 오면 뒷걸음질 치며 하나씩 밀치고 친다. 문간·열린 창·울타리 너머처럼 한 줄로만 올 수 있는 곳으로 끌고 간다. 여러 방향에서 잡히면 끌려 넘어져 바로 죽을 수 있고(서버 「끌려가기」 켜짐), 뒤에서 공격당하면 물릴 확률이 「높음」이다. 절대 무리 속으로 걸어 들어가지 않는다. 기본 설정에선 좀비마다 속도·시력·청력이 달라서 느린 좀비 사이에 조금 빠른 좀비가 섞여 있다(전력질주 좀비는 없음). 거리를 넉넉히 둔다.
- **키**: (없음)
- **아이콘**: (없음) 화면 캡처 후보는 맨 아래 표 참고
- **근거**: `Apocalypse.lua`(ZombieLore.ZombiesDragDown = true, RearVulnerability = 3, MultiHitZombies = false, Speed = 4, SprinterPercentage = 0, Sight = 5, Hearing = 5), `KO/Sandbox.json`(Sandbox_ZSpeed_option4 "무작위"), `EN/Sandbox.json`(ZSprinterPercentage 툴팁 "If Random Speed is enabled, this controls what percentage of zombies are Sprinters.", ZSight/ZHearing option5 "Random between Normal and Poor"), https://pzwiki.net/wiki/Build_42.10.0 (시력·청력 기본값 변경), `KO/Sandbox.json`(Sandbox_ZombiesDragDown "끌려가기": "다수의 좀비에게 공격당하면 플레이어가 끌어내려지고 즉사합니다", Sandbox_RearVulnerability "취약한 등 뒤", option3 "높음"), https://pzwiki.net/wiki/Zombie (42.21), https://pzwiki.net/wiki/Survival_Guide (42.20.4). 뒷걸음질 요령: https://www.reddit.com/r/projectzomboid/comments/1v8dboc/ (2026-07, 커뮤니티)
- **B42**: 확인(게임 파일, 웹)

### 2-5. 문은 닫고, 창문 바로 앞에는 서 있지 않기
- **설명**: 기본 설정의 좀비는 문을 열지 못한다. 대신 두드려서 부순다. 들어간 건물의 문은 닫아 둔다. 창문은 깨고 넘어오고, 울타리나 창문을 막 넘은 좀비는 가까이 있는 사람에게 몸을 날려 넘어뜨린다. 창문 너머 좀비를 상대할 땐 한 발 떨어져서 친다.
- **키**: `E` 「상호작용」(문 열고 닫기)
- **아이콘**: (없음)
- **근거**: `Apocalypse.lua`(ZombieLore.Cognition = 3, DoorOpeningPercentage = 0, ZombiesFenceLunge = true), `KO/Sandbox.json`(Sandbox_ZCognition_option3 "기본적인 추적", Sandbox_ZombiesFenceLunge "울타리 돌진하기"), https://pzwiki.net/wiki/Zombie (42.21), https://pzwiki.net/wiki/Build_42.14.0 (문 여는 비율 설정 추가)
- **B42**: 확인(게임 파일)

### 2-6. 소리가 좀비를 부른다
- **설명**: 망치질(바리케이드 포함)은 20칸 밖까지 들린다. 창문 깨기, 총, 집·차 경보도 좀비를 모은다. 총소리는 권총도 반경 60~120칸, 산탄총은 200칸까지 퍼진다. `Q` 는 「외치기」라서 짧게 누르면 소리쳐 좀비를 부른다(길게 누르면 감정표현 원형 창). 집 경보가 울리면 바로 그 동네를 뜬다. 6~9일째 낮에 헬리콥터가 한 번 지나가며 좀비를 끌고 다니니 그날은 실내에 숨는다.
- **키**: `Q` 「외치기」/「감정표현 원형 창 (길게 누르기)」
- **아이콘**: `Base.Hammer` → `Item_Hammer`
- **근거**: `PZ/media/lua/shared/TimedActions/ISBarricadeAction.lua`(소리 반경 20 × 망치 소리 배율), `keyBinding.lua`(SHOUT = KEY_Q, EMOTE = KEY_Q), `KO/UI.json`(binding_Shout "외치기", binding_Emote), `Apocalypse.lua`(Alarm = 4, CarAlarm = 3, ZombieLore.TriggerHouseAlarm = true, Helicopter = 2). 소음 수치(외치기 30, 집 경보 600, 헬기 500): https://pzwiki.net/wiki/Noise (42.13.1). 총 소음: https://pzwiki.net/wiki/Firearm (42.21). 헬기 일정: https://pzwiki.net/wiki/Helicopter (42.17)
- **B42**: 확인(게임 파일, 웹)

---

## 3. 루팅과 이동

### 3-1. B42 실내는 어둡다: 손전등은 허리에
- **설명**: B42 는 조명이 바뀌어서 불 꺼진 집 안과 밤이 훨씬 어둡다. 손전등을 단축키 칸(1-4)에 걸어 두고 `F` 로 꺼내 켠다. 바닐라에서는 42.13 부터 손에서 빼면 꺼진다. Common Sense 모드가 손전등을 허리띠에 다는 기능을 더해 준다. 건전지가 닳으니 여분을 챙긴다. 42.13 부터 커튼과 판자 바리케이드도 빛을 조금 새게 해서, 위키는 밤에 실내등을 끄라고 권한다.
- **키**: `F` 「조명 아이템 장착/켬/끔」
- **아이콘**: `Base.HandTorch` · Icon `Flashlight2` → `Item_Flashlight2`(소형 손전등), `Base.Torch` · Icon `Flashlight` → `Item_Flashlight`(손전등 - 고성능), `Base.Battery` · Icon `Battery` → `Item_Battery`
- **근거**: 공식 개요 "조명 전면 개편, 밤이 훨씬 어둡다": https://projectzomboid.com/blog/features-overview-build-42-20/ , 손전등은 손에서 빼면 꺼짐(42.13)·커튼은 빛을 일부 통과: https://pzwiki.net/wiki/Build_42.13.0 , 손전등 비추는 거리: https://pzwiki.net/wiki/Flashlight (42.11). `keyBinding.lua`(LIGHT_SOURCE = KEY_F), `data/mods.json`(Common Sense 요약 "손전등 허리에 차기")
- **B42**: 확인(웹). 불빛이 좀비를 끌어들이는지는 미확인

### 3-2. 깨진 창문은 유리부터 치우고 넘기
- **설명**: 창문을 깨면 소리가 크다. 깨진 창틀을 그냥 넘으면 유리에 베이거나 「유리 조각이 박힘」 상처가 생긴다. 무기를 든 채 창문을 우클릭해서 「부서진 유리 치우기」를 먼저 하고 「창문 넘기」. 잠긴 문이나 창문은 Common Sense 모드로 쇠지렛대를 써서 조용히 딸 수 있다(모드로 해결됨).
- **키**: `E` 길게 「상호작용」(창문 넘기), 우클릭 메뉴 「부서진 유리 치우기」「창문 넘기」「창문 부수기」
- **아이콘**: `Base.Crowbar` · IconsForTexture `Crowbar` → `Item_Crowbar`
- **근거**: `KO/ContextMenu.json`(ContextMenu_RemoveBrokenGlass "부서진 유리 치우기", ContextMenu_Climb_through "창문 넘기", ContextMenu_Smash_window "창문 부수기"), `KO/IG_UI.json`(IGUI_health_LodgedGlassShards "유리 조각이 박힘"), https://pzwiki.net/wiki/Survival_Guide (42.20.4), `data/mods.json`(Common Sense "쇠지렛대로 문·창문·차 문 따기")
- **B42**: 확인(게임 파일, 웹)

### 3-3. 집 하나 터는 순서
- **설명**: 들어가기 전에 빠져나갈 길을 두 개 정해 둔다. 문을 열고 한 걸음 물러나 안에서 뭐가 나오는지 본다. 안에 여럿이면 밖으로 끌어내서 처리한다. 들어가면 문을 닫고 방을 하나씩 확인한다. 바닥에 누워 있는 좀비도 일부는 죽은 척하다 일어나니 밟아서 확인한다. 다 턴 집은 지도에 표시해 둔다(7-1 지도 표식 공유 참고).
- **키**: (없음)
- **아이콘**: `Base.MuldraughMap` → `Item_Map`
- **근거**: https://pzwiki.net/wiki/Survival_Guide (42.20.4, 출구 2개·문 열고 물러서기·지도 표시), `Apocalypse.lua`(ZombieLore.DisableFakeDead = 1), `KO/Sandbox.json`(Sandbox_DisableFakeDead "죽은 척하는 좀비", option1 "세상에 있는 일부 좀비들만 죽은 척함.")
- **B42**: 확인(게임 파일, 웹). "문을 열어 두어 턴 집 표시" 같은 커뮤니티 관습은 B42 에서 문 상태가 무작위라 헷갈려서 넣지 않았다(https://pzwiki.net/wiki/Build_42.4.0)

### 3-4. 주변 상자 한 번에 보기(모드) 쓰는 법
- **설명**: 루팅 창 오른쪽 버튼 줄에 생기는 "주변" 버튼을 누르면 근처 상자·시체·바닥 물건이 한 목록에 모인다. 이 버튼을 `Shift`+클릭(또는 숫자패드 `0`)하면 "강제 선택"이 켜져서 루팅 창이 늘 이 목록으로 열린다. 숫자패드 `1` 은 모드 전체를 켜고 끈다. 쓰고 있는 상자는 테두리가 반짝여 어디 물건인지 보인다.
- **키**: `Shift`+클릭 또는 `숫자패드 0`(강제 선택 켜고 끄기), `숫자패드 1`(모드 켜고 끄기)
- **아이콘**: 모드 그림 `WS/2847184718/mods/ProximityInventory/common/media/ui/ProximityInventory.png`
- **근거**: `WS/2847184718/mods/ProximityInventory/common/media/lua/client/ProximityInventory/ProximityInventory.lua`(키 기본값 KEY_NUMPAD1, KEY_NUMPAD0, 테두리 표시 기본 켜짐), `.../ISInventoryPage.lua`(Shift+클릭으로 강제 선택), 모드 페이지 https://steamcommunity.com/sharedfiles/filedetails/?id=2847184718
- **B42**: 확인(모드 파일, B42.20+ 판)

### 3-5. 시간이 갈수록 털린 집이 늘어난다
- **설명**: 우리 서버(기본값)는 날이 갈수록 "이미 약탈당한 건물"이 늘어나서 90일째 최대 25%가 된다. 털린 집은 문이나 창이 부서져 있다. 시골은 그 절반이고, 방이 50개 넘는 큰 건물은 해당이 없다. 초반에 가까운 집부터 빨리 터는 게 이득이다. 90일쯤부터는 쥐가 들끓는 건물도 생긴다(사람을 공격하지는 않는다).
- **키**: (없음)
- **아이콘**: (없음)
- **근거**: `Apocalypse.lua`(MaximumLooted = 25, DaysUntilMaximumLooted = 90, RuralLooted = 0.5, MaximumLootedBuildingRooms = 50, MaximumRatIndex = 25, DaysUntilMaximumRatIndex = 90), `KO/Sandbox.json`(Sandbox_MaximumLooted "약탈당한 건물 확률 최대치", Sandbox_MaximumRatIndex "설치류 창궐 최고조"), `EN/Sandbox.json`(MaximumLootedBuildingRooms 툴팁 "If a building has more than this amount of rooms it will not be looted."), https://pzwiki.net/wiki/Build_42.4.0 (털린 집 모습, 56일 → 90일), https://pzwiki.net/wiki/Rat (42.20.4)
- **B42**: 확인(게임 파일, 웹). 25 를 퍼센트로 읽는 것은 팬 위키 해석이라 단위는 미확인

### 3-6. 가방은 등·어깨·허리에 같이 멘다
- **설명**: B42 는 등 가방, 어깨에 메는 책가방(사첼), 허리 가방 앞·뒤를 한꺼번에 찰 수 있다. 가방 안 물건은 무게가 줄어든다(큰 여행용 배낭은 용량 22·무게 80% 감소, 군용 배낭은 28·85%). 손에 든 가방은 양손 무기를 못 쓰게 하고 공격을 느리게 하니, 쫓기면 손에 든 가방부터 버린다. 무게가 한도의 1.5배를 넘으면 체력이 깎인다.
- **키**: (없음)
- **아이콘**: `Base.Bag_BigHikingBag` · IconsForTexture `BigHiking_Blue` → `Item_BigHiking_Blue`, `Base.Bag_ALICEpack` · Icon `AliceBag` → `Item_AliceBag`, `Base.Bag_FannyPackFront` · IconsForTexture `FannyPack` → `Item_FannyPack`, `Base.Bag_Satchel` · IconsForTexture `Satchel_Leather` → `Item_Satchel_Leather`
- **근거**: `PZ/media/scripts/generated/items/container.txt`(Bag_BigHikingBag Capacity 22·WeightReduction 80, Bag_ALICEpack 28·85, Bag_Schoolbag 15·70, Bag_DuffelBag 18·65, Bag_FannyPackFront 1·85, Bag_Satchel 12·65), `PZ/media/lua/shared/NPCs/BodyLocations.lua`(BACK, SATCHEL, FANNY_PACK_FRONT, FANNY_PACK_BACK 이 서로 겹치지 않는 자리), `KO/ItemName.json`(Bag_Satchel "책가방"), `KO/Moodles.json`(Moodles_HeavyLoad_lvl4 "용량 초과"). 손에 든 가방·과적: https://pzwiki.net/wiki/Container (42.20), https://pzwiki.net/wiki/Heavy_load (42.12.3), https://pzwiki.net/wiki/Survival_Guide (42.20.4)
- **B42**: 확인(게임 파일, 웹). 허리 가방 2개·사첼 동시 착용과 걸으면서 가방 메기(42.13)는 B42 에서 생김

---

## 4. 건강과 생존

### 4-1. 상처는 상태창 괄호 안에 치료법이 적혀 있다
- **설명**: `H` 로 상태창을 열면 다친 부위 옆 괄호에 할 일이 나온다. 「긁힌 상처 [소독, 붕대]」, 「물림 [소독, 붕대]」, 「깊은 상처 [봉합]」, 「뼈가 부러짐 [소독, 부목]」, 「화상 입음 [소독, 붕대]」. 「유리 조각이 박힘」, 「총알이 박힘」은 핀셋(또는 겸자)으로 먼저 빼낸다. 부위를 우클릭하면 치료 메뉴가 뜬다. 화면 구석의 Mini Health Panel 이 다친 곳을 빨갛게 깜빡여 주고, 왼쪽 클릭하면 상태창, 우클릭하면 상처 목록이 열린다(모드로 해결됨).
- **키**: `H` 「상태 창 전환」, 부위 우클릭(「마우스 우클릭으로 상처 치료」), 메뉴 「소독하기」「붕대 감기」「봉합하기」「유리 조각 제거하기」「부목 대기」「덴 상처 닦기」
- **아이콘**: `Base.Bandage` · Icon `Bandage` → `Item_Bandage`, `Base.AlcoholWipes` · Icon `AlcoholWipes` → `Item_AlcoholWipes`, `Base.Disinfectant` · Icon `Alcohol` → `Item_Alcohol`, `Base.SutureNeedle` · Icon `SutureNeedle` → `Item_SutureNeedle`, `Base.Tweezers` · Icon `Tweezers` → `Item_Tweezers`, `Base.Splint` · Icon `Splint` → `Item_Splint`, 왼쪽 아이콘 줄 `PZ/media/ui/Sidebar/64/Heart_On_64.png`
- **근거**: `KO/IG_UI.json`(IGUI_health_Scratched, _Bitten, _DeepWound, _Fracture, _Burned, _LodgedGlassShards, _LodgedBullet, _Cut "찢어진 상처", _RightClickTreatement), `KO/ContextMenu.json`(ContextMenu_Disinfect, _Bandage, _Stitch, _Remove_Glass, _Splint, _Clean_Burn), `WS/2866258937/mods/MiniHealthPanel/42/media/lua/client/MiniHealth/ISMiniHealth.lua`(onMouseUp = 상태창, onRightMouseUp = 상처 목록), 색 뜻(빨강 깜빡임 = 치료 필요, 주황 = 더러운 붕대): https://steamcommunity.com/sharedfiles/filedetails/?id=2866258937
- **B42**: 확인(게임 파일, 모드 파일)

### 4-2. 붕대는 갈고, 씻고, 소독해서 다시 쓴다
- **설명**: 「붕대가 오염됨」이 뜨면 새 붕대로 간다. 더러운 붕대를 그대로 두면 상처가 「세균 감염 됨」이 되는데, 이건 좀비 감염이 아니라 상처가 곪은 것이다. 소독하고 항생제를 먹으면 낫는다. 더러운 붕대는 「붕대 씻기」(물 0.5)로 빨고, 아주 뜨거운 물로 「붕대 소독하기」를 하거나 소독용 알코올·보드카·위스키로 「천 조각 소독하기」를 하면 「붕대 [살균됨]」이 된다. 부목은 판자나 나뭇가지에 천을 감아 직접 만든다.
- **키**: 제작창 「붕대 씻기」「붕대 소독하기」「천 조각 소독하기」「부목 만들기」
- **아이콘**: `Base.BandageDirty` · Icon `BandageDirty` → `Item_BandageDirty`, `Base.AlcoholBandage` · Icon `Bandage` → `Item_Bandage`, `Base.Antibiotics` · Icon `Antibiotics` → `Item_Antibiotics`, `Base.RippedSheets` · Icon `Rag` → `Item_Rag`, `Base.Whiskey` · Icon `Whiskey` → `Item_Whiskey`
- **근거**: `PZ/media/scripts/generated/recipes/recipes_medical.txt`(CleanBandage: 더러운 붕대 + 물 0.5 / DisinfectBandage: 물 0.5, OnTest = hotFluidContainer / DisinfectRag: RubbingAlcohol·Vodka·Whiskey 0.1 / MakeSplint: 천·데님·가죽 조각 + 판자·나뭇가지·나무 막대), `KO/Recipes.json`(CleanBandage "붕대 씻기", DisinfectBandage "붕대 소독하기", DisinfectRag "천 조각 소독하기", MakeSplint "부목 만들기"), `KO/Tooltip.json`(Tooltip_needsToBeHot "물을 담은 용기가 매우 뜨거워야 합니다."), `KO/IG_UI.json`(IGUI_health_DirtyBandage "붕대가 오염됨", IGUI_health_Infected "세균 감염 됨"), `KO/ItemName.json`(Base.AlcoholBandage "붕대 [살균됨]"), `Apocalypse.lua`(WoundInfectionFactor = 1.0)
- **B42**: 확인(게임 파일)

### 4-3. 좀비 감염인지, 감기·식중독·시체 냄새인지 구별하기
- **설명**: 좀비에게 물리면 100% 감염되고, 긁히면 7%, 찢어지면 25% 확률이다. 감염은 치료법이 없다. 감염되면 몇 시간 안에 이유 없이 불안해지고 열이 오르다가 「속이 안 좋음 → 메스꺼움 → 병듬 → 고열」 순으로 나빠져 약 3일 뒤 죽는다. 헷갈리기 쉬운 것들: 감기는 「콧물이 남 → 코를 훌쩍임」처럼 콧물 무들이 뜨고 재채기를 한다(재채기 소리가 좀비를 부르니 휴지를 쓴다). 식중독은 날음식·상한 음식·오염된 물을 먹은 뒤에 속이 안 좋아진다. 시체가 많이 쌓인 곳에선 「불쾌한 냄새」 무들과 함께 속이 안 좋아지는데 그 자리를 떠나면 낫는다. 다친 부위에 「세균 감염 됨」이 뜨는 건 상처가 곪은 것이다(4-2).
- **키**: `H` 「상태 창 전환」
- **아이콘**: 무들 `PZ/media/ui/Moodles/64/Mood_Nauseous.png`(속이 안 좋음~고열), `Mood_Ill.png`(감기), `Mood_NoxiousSmell.png`(불쾌한 냄새), `Mood_Zombified.png`(좀비화)
- **근거**: 감염 확률과 진행 단계: https://pzwiki.net/wiki/Knox_Infection (42.13.1). 웹 조사 중 `PZ/projectzomboid.jar` 의 `BodyPart.class` 에서 긁힘 7·찢어짐 25·물림 무조건 감염을 확인했다는 보고가 있다(내가 직접 다시 보지는 않음). `Apocalypse.lua`(ZombieLore.Transmission = 1, Mortality = 5, DecayingCorpseHealthImpact = 3), `KO/Sandbox.json`(Sandbox_ZTransmission_option1 "혈액과 타액", Sandbox_ZInfectionMortality_option5 "2-3일", Sandbox_DecayingCorpseHealthImpact "썩어가는 시체로 인한 건강 피해 영향"), `KO/Moodles.json`(Moodles_Sick_lvl1~4, Moodles_HasACold_lvl1~4, Moodles_NoxiousSmell_lvl1~4), 무들 그림 대응은 `zombie/ui/MoodleTextureSet.class`. 감기: https://pzwiki.net/wiki/Has_a_cold (42.7.0), 식중독: https://pzwiki.net/wiki/Sick (42.12.3), 시체 냄새(시체 5구 넘게 쌓이고 파리가 꼬일 때): https://pzwiki.net/wiki/Noxious_smell (42.13.1)
- **B42**: 확인(게임 파일, 웹)

### 4-4. 음식은 "신선한 → 신선하지 않은 → 상한", 통조림은 따기 전엔 안 상한다
- **설명**: 음식에 마우스를 올리면 상태가 나온다. 신선한 것부터 먹는다. 냉장고에 넣으면 5배 느리게 상하고, 완전히 얼면 상하지 않는다. 단전(14~30일 사이, 라디오가 최대 이틀 전에 알려 준다) 뒤에는 발전기가 없으면 냉장고가 꺼지고 언 음식이 녹기 시작한다. 통조림은 따기 전에는 상하지 않으니 오래 둘 식량으로 남긴다. 통조림은 깡통 따개로 연다. B42 는 칼이나 날카로운 부싯돌 조각으로도 열 수 있지만 날이 상하고 손을 다칠 수 있다. 날고기는 꼭 익혀 먹는다.
- **키**: 우클릭 메뉴(제작) 「통조림 열기」「날붙이로 통조림 열기」
- **아이콘**: `Base.TinnedBeans` · Icon `Beans` → `Item_Beans`, `Base.TinOpener` · Icon `CanOpener` → `Item_CanOpener`, `Base.KitchenKnife` · IconsForTexture `KnifeChopping` → `Item_KnifeChopping`
- **근거**: `KO/Tooltip.json`(Tooltip_food_Fresh "신선한", _Stale "신선하지 않은", _Rotten "상한", _Frozen "냉동된", _Dangerous_uncooked "요리되지 않아 식중독 위험이 있습니다.", Tooltip_Recipe_OpenCanWithKnife "날이 손상됩니다. 손을 다칠 수 있습니다."), `PZ/media/scripts/generated/recipes/recipes_cannedFood.txt`(OpenCannedFood = canopener 태그, OpenCannedFoodWithKnifeOrSharpStoneFlake = sharpknife 태그), `KO/Recipes.json`(OpenCannedFood "통조림 열기", OpenCannedFoodWithKnifeOrSharpStoneFlake "날붙이로 통조림 열기"), `Apocalypse.lua`(ElecShut = 2, FoodRotSpeed = 3, FridgeFactor = 3), `KO/Sandbox.json`(Sandbox_ElecShut_option2 "14일-30일"). 냉장 5배·통조림: https://pzwiki.net/wiki/Food (42.20.0), 단전 예고: https://pzwiki.net/wiki/Metagame (42.13.2)
- **B42**: 확인(게임 파일, 웹). 칼로 통조림 따기는 B42 에서 생김

### 4-5. 단수 뒤 물은 끓이거나 알약으로, 요리는 모닥불·바비큐로
- **설명**: 단수(0~30일 사이, 예고 없음) 뒤에 강·호수·웅덩이·빗물에서 뜬 물은 모두 「오염된 물」로 나온다. 냄비나 주전자에 담아 불이나 오븐에 끓이거나(플라스틱 통은 전자레인지), 「물 정수 알약」 하나로 1리터를 정수한다. 오염된 물이 조금이라도 섞이면 통 전체가 오염되니 깨끗한 물 통에 붓지 않는다. 단전 뒤엔 오븐을 못 쓰니(발전기 제외) 건축 창 「실외」에서 돌 3개로 모닥불을 짓거나 바비큐를 쓴다. 바비큐는 실내에서도 안전하지만 실내 모닥불은 바닥으로 불이 번진다. 에크론 근처 농장의 우물은 처음부터 깨끗한 물이 나온다(양은 한정).
- **키**: 제작창 「물 정수하기」, 건축 창 「모닥불」
- **아이콘**: `Base.Pot` · Icon `Pot` → `Item_Pot`, `Base.WaterPurificationTablets` · Icon `WaterPurificationTablets` → `Item_WaterPurificationTablets`, `Base.WaterBottle` · Icon `WaterBottle` → `Item_WaterBottle`, `Base.Stone2` · Icon `Rock` → `Item_Rock`, `Base.Matches` · Icon `Matches` → `Item_Matches`
- **근거**: `KO/Tooltip.json`(Tooltip_item_TaintedWater "오염된 물. 마시기엔 안전하지 않습니다.<br>오븐에 넣거나 불로 끓이세요.", Tooltip_item_TaintedWater_Plastic, Tooltip_craft_campfireDesc "따뜻하고, 요리도 할 수 있고, 시체도 태울 수 있습니다.", Tooltip_Recipe_PurifyWater), `KO/Fluids.json`(Fluid_Name_TaintedWater "오염된 물"), `recipes_medical.txt`(PurifyWater), `KO/Recipes.json`(PurifyWater "물 정수하기", Campfire "모닥불"), `PZ/media/scripts/generated/entities/outdoors/entity_campfire.txt`(category = Outdoors, 재료 Base.Stone2 3개), `Apocalypse.lua`(WaterShut = 2), `KO/Sandbox.json`(Sandbox_Shutoff_option2 "0-30일 사이"), `projectzomboid.jar` `zombie/entity/components/fluids/FluidContainerUpdateSystem.class`(빗물 처리에 TaintedWater 참조). 알약 1리터: https://pzwiki.net/wiki/Water_Purification_Tablets (42.11.0), 섞이면 오염: https://pzwiki.net/wiki/Water_(Tainted)_(fluid) , 바비큐·오븐: https://pzwiki.net/wiki/Heat_source (42.5.1), 모닥불 번짐: https://pzwiki.net/wiki/Campfire (42.20.4), 우물: https://pzwiki.net/wiki/Well (42.20.4)
- **B42**: 확인(게임 파일, 웹). 유체(리터 단위 물) 체계와 돌 3개 모닥불, 유한한 우물은 B42 에서 바뀜. "단전 뒤 프로판으로 쓰는 가스레인지"는 바닐라에 없다(프로판은 바비큐만)

### 4-6. 지루함은 쌓이기 전에 푼다
- **설명**: 같은 일만 계속하면 「지루함」이 쌓이고, 2단계부터는 「우울함」이 올라간다. 우울하면 모든 행동이 느려진다(최대 2배). 책(지루함 -50)·만화책(-30)·잡지(-20)를 읽고, TV·라디오를 틀고, 단 음식이나 술을 먹고, 같이 하는 사람과 이야기하면 풀린다. 이미 읽은 책·만화는 45일이 지나야 다시 효과가 있다. 우리 서버의 빠른 독서(한 쪽 0.1분)는 기술 서적에만 적용되니 만화·잡지는 원래 시간만큼 걸린다. 담배는 스트레스를 줄여 준다.
- **키**: 우클릭 메뉴 「읽기」
- **아이콘**: 무들 `PZ/media/ui/Moodles/64/Mood_Bored.png`, `Mood_Sad.png`, `Base.ComicBook` · Icon `ComicBook` → `Item_ComicBook`, `Base.Magazine` · Icon `Magazine` → `Item_Magazine`, `Base.CigarettePack` · Icon `IckySticks` → `Item_IckySticks`, `Base.PillsAntiDep` · Icon `PillsAntidepressant` → `Item_PillsAntidepressant`
- **근거**: `PZ/media/scripts/generated/items/literature.txt`(Book BoredomChange -50·StressChange -40·UnhappyChange -40, ComicBook -30·-20·-20, Magazine -20·-15), `Apocalypse.lua`(LiteratureCooldown = 45, MinutesPerPage 기본 2.0), `KO/Sandbox.json`(Sandbox_LiteratureCooldown "서적 쿨다운 일수", Sandbox_MinutesPerPage "기술 서적 한 쪽당 독서 시간"), `KO/Moodles.json`(Moodles_Bored_lvl1~4, Moodles_Unhappy_lvl1~4), `data/mods.json`(MinutesPerPage = 0.1). 우울 불이익·해소법: https://pzwiki.net/wiki/Unhappy (42.20.0), https://pzwiki.net/wiki/Bored (42.12.3)
- **B42**: 확인(게임 파일, 웹)

## 5. 기지 만들기

### 5-1. 기지 자리 고르기와 주변 정리
- **설명**: 정확한 동네보다 울타리가 있고, 드나드는 곳이 두 군데 이하이고, 여럿이 상자를 놓을 넓은 창고나 방이 있는 곳이 중요하다는 의견이 많다. 물가는 낚시, 숲 근처는 채집·땔감에 좋다. 에크론 근처 농장은 우물이 있어 단수 뒤에도 깨끗한 물을 얻는다. 기지 근처에 좀비 시체를 쌓아 두면 냄새로 병이 나니(시체 9일 뒤 사라짐), 「시체 들기」로 멀리 옮기거나 모닥불에 태운다.
- **키**: 시체 우클릭 「시체 들기」(「시체 잡기」 키는 기본으로 비어 있음)
- **아이콘**: `Base.Stone2` → `Item_Rock`(모닥불 재료), 무들 `PZ/media/ui/Moodles/64/Mood_NoxiousSmell.png`
- **근거**: B42 기지 위치 토론(2025-01-15): https://steamcommunity.com/app/108600/discussions/0/598515896185541386 , 우물: https://pzwiki.net/wiki/Well (42.20.4), 시체 냄새: https://pzwiki.net/wiki/Noxious_smell (42.13.1), `Apocalypse.lua`(HoursForCorpseRemoval = 216.0), `KO/ContextMenu.json`(ContextMenu_Grab_Corpse "시체 들기"), `keyBinding.lua`(GRAB_CORPSE = KEY_NONE), `KO/Tooltip.json`(Tooltip_craft_campfireDesc "…시체도 태울 수 있습니다.")
- **B42**: 확인(게임 파일). 위치 의견은 커뮤니티 의견이고, 여럿이 할 때 시골이 나은지 마을이 나은지는 정리된 의견을 못 찾음

### 5-2. 바리케이드는 안쪽에서 친다
- **설명**: 망치를 들고 다른 손에 판자를 든 채 창문이나 닫힌 문을 우클릭해서 「바리케이드 설치 (판자)」. 판자 1장에 못 2개가 들고, 한 면에 4장까지 붙는다. 바리케이드는 내가 서 있는 쪽 면에 붙으니 안에서 쳐야 안에서 뗄 수 있다. 판자 2장까지는 틈으로 밖이 보인다. 목공 레벨이 높을수록 튼튼하다(10레벨이면 1.5배). 망치질 소리는 20칸까지 들린다. 금속판·강철 봉 바리케이드는 금속용접 3과 용접용 프로판 토치가 필요하다. 좀비는 바리케이드와 지은 구조물을 부술 수 있다(서버 「건축물 파괴」 켜짐). 높은 울타리는 좀비가 못 넘고, 25마리가 몰려야 부서지기 시작한다.
- **키**: 우클릭 메뉴 「바리케이드 설치 (판자)」「바리케이드 제거」
- **아이콘**: `Base.Plank` · Icon `Plank` → `Item_Plank`, `Base.Nails` · Icon `Nails` → `Item_Nails`, `Base.Hammer` · IconsForTexture `Hammer` → `Item_Hammer`, `Base.SheetMetal` · Icon `SheetMetal` → `Item_SheetMetal`, `Base.BlowTorch` · Icon `BlowTorch` → `Item_BlowTorch`
- **근거**: `PZ/media/lua/shared/TimedActions/ISBarricadeAction.lua`(isValid: 망치 장착·판자 장착·못 2개 이상, complete: Plank 1·Nails 2 제거, start: 소리 반경 20 × 망치 소리 배율, getBarricadeForCharacter = 캐릭터가 선 쪽), `PZ/media/scripts/generated/entities/barricades/entity_barricade_planks.txt`(건축 창 제작법은 판자 1·못 1), `KO/ContextMenu.json`(ContextMenu_Barricade "바리케이드 설치 (판자)", ContextMenu_Unbarricade), `Apocalypse.lua`(ZombieLore.ThumpOnConstruction = true, FenceThumpersRequired = 25), `KO/Sandbox.json`(Sandbox_ThumpOnConstruction "건축물 파괴"). 4장·2장까지 보임·목공 보정·금속 바리케이드 조건: https://pzwiki.net/wiki/Barricade (위키 표는 B41 표기이나 42.21 코드와 맞다는 웹 조사 보고)
- **B42**: 확인(게임 파일). 우클릭 메뉴(못 2개)와 건축 창(못 1개)의 못 개수가 다르다

### 5-3. 계단을 부수고 천 밧줄로 오르내리기
- **설명**: 2층을 기지로 쓰면 대형 망치로 계단을 「철거하기」 해서 좀비가 못 올라오게 하고, 2층 창문에 「천 밧줄 설치」를 해서 오르내린다. 천 밧줄은 내려가는 층마다 1개(지금 층 포함)와 못 1개, 망치가 든다. 천 밧줄은 천(침대 시트) 1장으로 「천 밧줄 묶기」를 하면 1개 나온다. 좀비는 밧줄을 타지 못한다. 오를 때 미끄러질 수 있고(서버 「간단한 오르기」 꺼짐) 팔 근육이 지친다. 밧줄을 먼저 걸어 시험해 본 뒤에 계단을 부순다. 다시 놓으려면 나무 계단은 목공 6(판자 13, 못 8)이 든다. 사다리는 장식이라 못 오른다.
- **키**: 우클릭 메뉴 「철거하기」「천 밧줄 설치」「천 밧줄 타고 오르기」, 제작 「천 밧줄 묶기」
- **아이콘**: `Base.Sledgehammer` · Icon `Sledgehamer` → `Item_Sledgehamer`, `Base.SheetRope` · Icon `SheetRope` → `Item_SheetRope`, `Base.Sheet` · Icon `Sheet` → `Item_Sheet`, `Base.Nails` → `Item_Nails`
- **근거**: `PZ/media/lua/server/BuildingObjects/ISDestroyCursor.lua`(183행 계단 전체 강조, 328~331행 계단 꼭대기 바닥 타일은 못 부숨), ini 기본값(AllowDestructionBySledgehammer = true, SledgehammerOnlyInSafehouse = false), `KO/ContextMenu.json`(ContextMenu_Destroy "철거하기", ContextMenu_Add_sheet_rope "천 밧줄 설치", ContextMenu_Climb_Sheet_Rope "천 밧줄 타고 오르기"), `Apocalypse.lua`(EasyClimbing = false), `KO/Sandbox.json`(Sandbox_EasyClimbing "간단한 오르기"), `EN/Sandbox.json`(EasyClimbing 툴팁 "Disables the failure chances when climbing sheet ropes or over walls."), `PZ/media/scripts/generated/recipes/recipes.txt`(CraftSheetRope: Base.Sheet 1 → Base.SheetRope 1), `KO/Recipes.json`(CraftSheetRope "천 밧줄 묶기"). 천 밧줄 개수: https://pzwiki.net/wiki/Sheet_Rope (42.10.0). 계단 재료: `PZ/media/scripts/generated/entities/stairs/entity_carpentry_stairs.txt`(Woodwork 6, Plank 13, Nails 8). 좀비가 못 타는 것(`ClimbSheetRopeState` 를 플레이어만 씀)과 사다리 없음은 웹 조사 중 jar 확인 보고(내가 다시 보지는 않음)
- **B42**: 확인(게임 파일). 좀비가 밧줄을 뜯어낼 수 있는지는 자료가 엇갈려 미확인(42.21 위키 변경 기록에 관련 수정이 있다는 보고가 있으나 Steam 42.21 공지 두 개에는 "rope" 언급이 없음)

### 5-4. 빗물받이로 물 걱정 덜기
- **설명**: 목공 3이면 「빗물받이 상자」(판자 4, 못 4, 쓰레기 봉투 4 또는 방수포 1 → 400리터), 목공 5면 「빗물받이 통」(판자 6, 못 5, 쓰레기 봉투 4 또는 방수포 1 → 600리터)을 건축 창 「실외」에서 지을 수 있다. 지붕 없는 바깥에 둔다. 받은 빗물은 「오염된 물」이라 끓이거나 정수해서 마신다(작물 물 주기·씻기는 그대로). 빗물받이와 물받이 홈통(gutter)을 잇는 기능은 바닐라에 없다.
- **키**: 건축 창 「실외」
- **아이콘**: `Base.Garbagebag` · Icon `Garbagebag` → `Item_Garbagebag`, `Base.Tarp` · Icon `TentMaterial` → `Item_TentMaterial`, `Base.Plank` → `Item_Plank`, `Base.Nails` → `Item_Nails`
- **근거**: `PZ/media/scripts/generated/entities/outdoors/entity_raincollector.txt`(RainCollector: Woodwork 3, Plank 4·Nails 4·garbagebag 4, Capacity 400 / RainCollectorRound: Woodwork 5, Plank 6·Nails 5·garbagebag 4, Capacity 600, category = Outdoors), `entity_raincollector_tarp.txt`(같은 구성에 Tarp 1), 물병 Capacity 1.0 과 비교해 단위가 리터임을 확인(`items/normal.txt` WaterBottle), `KO/Recipes.json`(RainCollectorCrate "빗물받이 상자 (쓰레기 봉투)", RainCollectorBarrel "빗물받이 통 (쓰레기 봉투)" 등), `KO/Tooltip.json`(Tooltip_craft_rainCollectorDesc "실외에 두면 빗물을 받을 수 있는 뚜껑 없는 보관함입니다."), `FluidContainerUpdateSystem.class`(TaintedWater 참조). 빗물 오염: https://pzwiki.net/wiki/Rain_Collector_Barrel_(Tarp) (42.12.3). 홈통은 모드 기능: https://steamcommunity.com/sharedfiles/filedetails/?id=3439305933
- **B42**: 확인(게임 파일, 웹)

### 5-5. 발전기: 연결 조건, 실내 금지, 범위
- **설명**: 발전기를 「발전기 연결하기」 하려면 「잡지: 발전기 사용법」을 읽었거나, 전기공학 3 이상이거나, 전기 기사여야 한다. 건물 안에서 돌리면 건물 전체에 유독 가스가 차서 「불쾌한 냄새 … 치명적인 매연」 무들이 뜨고 죽을 수 있다. 게임 설명에도 "실내에서 작동시키지 마세요"라고 적혀 있다. 바깥에 두면 가로 반경 20칸, 위아래 3층까지 전기가 간다. 연료통은 10리터이고 꺼진 상태에서만 휘발유를 넣을 수 있다. 소리가 반경 20칸쯤 들려 좀비를 부른다. 고장 나면 「전기 회로 부속」으로 고친다. 무게가 40이라 양손으로 든다.
- **키**: 우클릭 메뉴 「발전기 연결하기」「연료 넣기」「켜기」「발전기 정보」
- **아이콘**: `Base.Generator` · Icon `Generator` → `Item_Generator`, `Base.ElectronicsMag4` · Icon `MagazineElectronics02` → `Item_MagazineElectronics02`, `Base.PetrolCan` · Icon `Petrol` → `Item_Petrol`, `Base.ElectronicsScrap` · Icon `ElectronicsScrap` → `Item_ElectronicsScrap`, 무들 `PZ/media/ui/Moodles/64/Mood_NoxiousSmell.png`
- **근거**: `KO/Tooltip.json`(Tooltip_Generator "이동식 전력 공급원입니다. 은신처 주변에 놓고 연결하세요.<br>전기공학 지식이 필요하며, 휘발유를 넣어야 합니다.<br>실내에서 작동시키지 마세요."), `KO/ContextMenu.json`(ContextMenu_GeneratorPlug "발전기 연결하기", ContextMenu_GeneratorPlugTT "…전기 기사 직업을 가지고 있거나, 관련 지식을 배우거나, 전기공학 3단계 이상이어야 합니다.", ContextMenu_GeneratorAddFuel "연료 넣기", ContextMenu_GeneratorInfo "발전기 정보"), `items/literature.txt`(ElectronicsMag4 LearnedRecipes = Generator), `PZ/projectzomboid.jar` `zombie/iso/objects/IsoGenerator.class`(IsoBuilding.setToxic 호출), `KO/Moodles.json`(Moodles_NoxiousSmell_lvl4 "치명적인 매연"), `Apocalypse.lua`(GeneratorTileRange = 20, GeneratorVerticalPowerRange = 3, AllowExteriorGenerator = true), `items/normal.txt`(Generator Weight 40, RequiresEquippedBothHands, SoundRadius 20), `PZ/media/lua/client/ISUI/ISWorldObjectContextMenu.lua`(onFixGenerator: ElectronicsScrap). 연료 10리터·소비량·매연 피해: https://pzwiki.net/wiki/Generator (42.13.1), https://pzwiki.net/wiki/Noxious_smell (42.13.1)
- **B42**: 확인(게임 파일, 웹). 위아래 3층 범위와 발전기 종류 4가지(렉트로맥스·프리미엄 테크놀로지스·밸류테크·구형, `items/normal.txt`)는 B42 에서 바뀜

### 5-6. B42 지하실
- **설명**: B42 는 일부 건물에 지하실이 있다. 지도에 고정된 지하실과, 세계마다 무작위로 생기는 지하실이 있다(서버 「지하실 등장 빈도: 가끔」). 같은 집이라도 세계가 다르면 지하실이 없을 수 있다. 입구가 집 안 계단인 곳도, 집 밖 출입구인 곳도 있다. 입구가 하나라 막기 쉽지만 막히면 빠져나갈 데가 없다. 지하 벽은 부술 수 없다. 발전기는 위아래 3층까지 전기를 보내니 지상 바깥에 둔 발전기로 지하에도 전기를 넣는다(지하에 발전기를 두면 실내라 위험할 것으로 보인다).
- **키**: (없음)
- **아이콘**: (없음) 화면 캡처 후보는 맨 아래 표의 지하실 그림
- **근거**: `Apocalypse.lua`(Basement.SpawnFrequency = 4), `KO/Sandbox.json`(Sandbox_BasementSpawnFrequency "지하실 등장 빈도"), `EN/Sandbox.json`(option4 "Sometimes"), `PZ/media/lua/shared/ProceduralBasements/`, https://pzwiki.net/wiki/Basement (42.12.3), 고정 지하실 지도: https://map.projectzomboid.com , `KO/IG_UI.json`(IGUI_Moveables_BasementWallAdjacentToTheVoid "지하 벽은 없앨 수 없습니다."), `PZ/media/basement_access/`(입구 모양 파일 147개, 이름에 exterior 74개·interior 24개)
- **B42**: 확인(게임 파일, 웹). 지하실은 B42 에서 생김. "막기 쉽다/갇힌다"는 커뮤니티 의견과 추론, 지하 발전기 위험은 추론이라 미확인

## 6. B42 에서 새로 생긴 것

### 6-1. 제작은 B, 건축은 왼쪽 망치 버튼
- **설명**: B42 는 제작 화면이 새로 바뀌었다. `B` 로 제작창을 열면 분류별 제작법과 필요한 재료가 보인다. 우리 서버(기본값)는 아직 못 배운 제작법도 목록에 보여서 무엇이 필요한지 미리 알 수 있다. 벽·가구·빗물받이 같은 건축물은 왼쪽 아이콘 줄의 건축 버튼으로 연 건축 창에서 만든다. 일부 제작은 작업대·화덕 같은 시설 옆에서만 된다.
- **키**: `B` 「제작 창 전환」, 「건축 창 전환」은 기본 키 없음(왼쪽 아이콘 줄 버튼)
- **아이콘**: `PZ/media/ui/Sidebar/64/Carpentry_On_64.png`(제작창), `PZ/media/ui/Sidebar/64/Build_On_64.png`(건축)
- **근거**: `keyBinding.lua`(CRAFTING_UI = KEY_B, BUILDING_UI = KEY_NONE), `PZ/media/lua/server/XpSystem/XpUpdate.lua`(132~149행), `PZ/media/lua/client/ISUI/ISEquippedItem.lua`(craftingBtn, buildBtn), `Apocalypse.lua`(SeeNotLearntRecipe = true), `KO/Sandbox.json`(Sandbox_SeeNotLearntRecipe "배우지 못한 제작법 보임")
- **B42**: 확인(게임 파일)

### 6-2. 제작법은 잡지, 기술 레벨, "제작법 연구하기"로 배운다
- **설명**: 42.21 제작법 약 970개 중 약 380개는 배워야 쓸 수 있다. 배우는 길은 셋이다. 잡지(예: 「잡지: 발전기 사용법」)를 읽거나, 관련 기술이 일정 레벨에 오르면 저절로 배우거나(예: 「간이 숫돌 만들기」는 물건관리 2), 처음 보는 도구·무기를 우클릭해서 「제작법 연구하기」를 하면 그 물건으로 만드는 법을 배운다(물건은 안 없어진다). 배운 제작법은 캐릭터마다 따로라서 잡지는 같이 하는 사람이 각자 읽는다. Has Been Read 모드가 아이콘에 "?"(안 읽음), "!"(읽다 만 것) 표시를 붙이니 루팅할 때 표시 붙은 것만 챙긴다(모드로 해결됨). 레시피 잡지는 우편함에서 가장 많이 나온다.
- **키**: 우클릭 메뉴 「제작법 연구하기」
- **아이콘**: `Base.ElectronicsMag4` · Icon `MagazineElectronics02` → `Item_MagazineElectronics02`, `Base.Magazine` · Icon `Magazine` → `Item_Magazine`
- **근거**: `PZ/media/scripts` 아래 `.txt` 전체에서 센 값: `craftRecipe` 969개, `NeedToBeLearn = true` 377개, `AutoLearnAny` 126개, `AutoLearnAll` 160개. `PZ/media/scripts/generated/items/literature.txt`(ElectronicsMag4 LearnedRecipes = Generator), `recipes_fixing.txt`(MakeCrudeWhetstone AutoLearnAny = Maintenance:2), `PZ/media/lua/client/ISUI/ISInventoryPaneContextMenu.lua`(557행 ContextMenu_ResearchCraft), `KO/ContextMenu.json`(ContextMenu_ResearchCraft "제작법 연구하기"), `KO/ItemName.json`(Base.ElectronicsMag4 "잡지: 발전기 사용법"), https://pzwiki.net/wiki/Crafting (42.21.0, 배우는 경로), https://pzwiki.net/wiki/Recipe_magazine (42.11.0, 우편함), Has Been Read 표시 뜻: https://steamcommunity.com/sharedfiles/filedetails/?id=2544353492
- **B42**: 확인(게임 파일, 웹)

### 6-3. TV·비디오테이프로는 기술 3레벨까지만
- **설명**: TV 교양 프로그램이나 비디오테이프(VHS)로 기술 경험치를 얻을 수 있지만, 그 기술이 3레벨이 되면 더는 안 오른다(서버 기본값). 초반에 기술을 조금 올리는 용도다. Named skill VHS tapes 모드가 테이프 이름에 기술 이름을 붙여 준다. 스킬 보존 일지에는 TV·VHS 로 얻은 경험치가 기록되지 않는다(모드 기본값).
- **키**: (없음)
- **아이콘**: `Base.VHS_Retail` · Icon `Cassette3` → `Item_Cassette3`, `Base.TvAntique` · Icon `Television` → `Item_Television`
- **근거**: `Apocalypse.lua`(LevelForMediaXPCutoff = 3), `KO/Sandbox.json`(Sandbox_LevelForMediaXPCutoff "매체 경험치 획득 단계 제한", 툴팁 "…경험치 획득이 불가능해지기 시작하는 기술 단계"), `WS/2503622437/mods/Skill Recovery Journal/42.20.1/media/sandbox-options.txt`(TranscribeTVXP 기본 false), `data/mods.json`(Named skill VHS tapes)
- **B42**: 확인(게임 파일)

### 6-4. 채집은 End 키, 밤에는 불빛, 버섯은 조심
- **설명**: `End` 를 누르면 탐색 모드가 켜지고, 걷는 동안 주변의 먹을거리·나뭇가지·돌 같은 것이 표시된다. 채집 레벨이 오를수록 넓게 보인다. 어두우면 거의 못 찾으니 손전등이나 라이터를 손에 든다. 비 올 땐 우산이 도움이 된다. 겨울(12~2월)에는 열매·버섯이 거의 없다. 버섯은 독일 확률이 높고 생김새로는 못 가린다. 블랙베리·블루베리는 늘 안전하다. 동물 발자국도 탐색 모드에서 찾는다.
- **키**: `End` 「탐색 모드 전환」, 왼쪽 아이콘 줄 「구역 탐색」 버튼
- **아이콘**: `PZ/media/ui/Sidebar/64/Search_On_64.png`, `Base.Twigs` · Icon `Twigs` → `Item_Twigs`, `Base.Stone2` · Icon `Rock` → `Item_Rock`, `Base.BerryBlack` · Icon `BerryBlack` → `Item_BerryBlack`
- **근거**: `PZ/media/lua/client/Foraging/ISSearchManager.lua`(1473~1474행, TOGGLE_SEARCH_MODE 키 207 = End), `KO/UI.json`(binding_Toggle Search Mode "탐색 모드 전환", UI_investigate_area_window_title "구역 탐색"), `KO/IG_UI.json`(IGUI_SearchMode_Tip_Darkness_Text "어둠 속에서는 채집이 힘듭니다. 손전등을 켜 밝게 유지하세요!", _Mushrooms_Text, _Weather_Text, _Seasons_Text), https://pzwiki.net/wiki/Foraging (42.18.0, 범위·어둠·독 확률. 위키가 B41/B42 내용이 섞였다고 표기), https://pzwiki.net/wiki/Tracking (42.19.0)
- **B42**: 확인(게임 파일). 수치는 확인(웹)이지만 위키가 일부 오래된 내용이라고 경고함

### 6-5. 동물은 목장에서, 처음엔 닭부터
- **설명**: 닭·소·양 같은 가축은 지도에 정해진 목장·농장 구역에서 나온다(서버 기본 「가축 생성 확률: 자주」). 동물 옆에서 `V` 를 누르면 동물 원형 메뉴가 뜬다. 처음엔 닭이 쉽다. 들어서 가방에 넣을 수 있고 도망가지 않으며 암탉은 하루 한 알을 낳는다. 키우려면 왼쪽 아이콘 줄의 구역 버튼으로 가축 구역을 정하고 그 안에 여물통을 둔다(여물통 하나엔 먹이와 물 중 하나만). 동물 울음소리에 좀비가 끌려온다(서버 기본값 켜짐).
- **키**: `V` 「동물 원형 메뉴」
- **아이콘**: `Base.Egg` · Icon `Egg` → `Item_Egg`, 구역 버튼 `PZ/media/ui/Sidebar/64/AnimalZone_On_64.png`
- **근거**: `keyBinding.lua`(ANIMAL_RADIAL_MENU = KEY_V), `KO/UI.json`(binding_AnimalRadialMenu "동물 원형 메뉴"), `Apocalypse.lua`(AnimalRanchChance = 5, AnimalSoundAttractZombies = true), `KO/Sandbox.json`(Sandbox_AnimalRanchChance "가축 생성 확률", Sandbox_AnimalSoundAttractZombies "좀비의 동물 소리 반응"), `EN/Sandbox.json`(AnimalRanchChance_option5 "Often"), `PZ/media/lua/client/ISUI/ISEquippedItem.lua`(zoneBtn). 닭·여물통·구역: https://pzwiki.net/wiki/Chicken (42.20.4), https://pzwiki.net/wiki/Animal (42.20.4). 도축 고리(목공 3, 고기·가죽 더 많이): https://pzwiki.net/wiki/Butcher_Hook (42.12.3)
- **B42**: 확인(게임 파일, 웹). 동물·축산은 B42 에서 생김

### 6-6. 도구가 없으면 돌로 만든다
- **설명**: 칼이나 도끼를 못 구했으면 돌 도구로 버틴다. 부싯돌 덩어리를 돌 망치로 쳐서 「날카로운 부싯돌 조각」을 만들고(칼 대신 통조림 따기 등에 쓰인다), 나뭇가지 + 날카로운 부싯돌 조각 + 묶을 것 2개(찢어진 천, 노끈, 강력 접착 테이프 등)로 「조잡한 돌 도끼」를 만든다. 돌 도끼는 따로 배울 필요 없이 물건관리 1이면 된다. 대장장이(금속세공)는 시설과 책이 많이 필요한 후반 기술이라 초반엔 신경 쓰지 않아도 된다.
- **키**: (없음)
- **아이콘**: `Base.SharpedStone` · Icon `RockSharpened` → `Item_RockSharpened`, `Base.AxeStone` · Icon `AxeStone` → `Item_AxeStone`, `Base.FlintNodule` · Icon `FlintAngular` → `Item_FlintAngular`, `Base.HammerStone` · Icon `HammerStone` → `Item_HammerStone`
- **근거**: `PZ/media/scripts/generated/recipes/recipes_knapping.txt`(MakeSharpFlintFlake: FlintNodule + hammerstone 태그 / MakeCrudeStoneAxe: NeedToBeLearn = false, SkillRequired = Maintenance:1, TreeBranch2 + SharpedStone + simpleweaponbinding 2), `recipes_cannedFood.txt`(OpenCannedFoodWithKnifeOrSharpStoneFlake), `PZ/media/scripts/generated/items/*.txt`(simpleweaponbinding 태그: DuctTape, Twine, RippedSheets, DenimStrips, LeatherStrips 등), `KO/Recipes.json`(MakeCrudeStoneAxe "조잡한 돌 도끼 만들기"), `KO/ItemName.json`(SharpedStone "날카로운 부싯돌 조각", FlintNodule "부싯돌 덩어리", HammerStone "돌 망치"), https://pzwiki.net/wiki/Crude_Stone_Axe (42.10.0, "초반에 좋은 도구"), https://pzwiki.net/wiki/Blacksmithing (42.18.0)
- **B42**: 확인(게임 파일, 웹). 석기 제작은 B42 에서 생김

## 7. 멀티에서 같이 할 때

### 7-1. 지도에서 친구 찾기, 표식은 "전체 공개"로
- **설명**: 우리 서버는 지도와 미니맵에 모든 플레이어가 표시된다. 게임 화면에서는 내 시야 밖(등 뒤, 벽 너머)에 있는 사람이 좀비처럼 안 보이고, 이름은 마우스를 올려야 보인다. 길을 잃으면 화면보다 지도를 본다. 지도의 「기호」 도구로 기지·털린 집·위험 지역에 표식을 찍고, 「공유하기」에서 「전체 공개」로 바꾸면 다 같이 볼 수 있다.
- **키**: `M` 「지도 열고 닫기」, 지도 안 「기호」→「기호 추가」「기록 작성」「공유하기」
- **아이콘**: `Base.MuldraughMap` → `Item_Map`, `Base.Pen` · Icon `Pen` → `Item_Pen`(지도에 쓰려면 필기구)
- **근거**: `data/mods.json`(MapRemotePlayerVisibility = 4), `KO/UI.json`(UI_ServerOption_MapRemotePlayerVisibility_tooltip "4=모두 보임", UI_ServerOption_HidePlayersBehindYou_tooltip "시야에 없는 플레이어를 화면에 표시하지 않습니다(좀비처럼).", UI_ServerOption_MouseOverToSeeDisplayName_tooltip), ini 기본값(HidePlayersBehindYou = true, MouseOverToSeeDisplayName = true), `PZ/media/lua/client/ISUI/Maps/ISWorldMapSharing.lua`, `ISWorldMapSymbols.lua`(991행), `KO/IG_UI.json`(IGUI_Map_Symbols "기호", IGUI_Map_AddSymbol "기호 추가", IGUI_Map_AddNote "기록 작성", IGUI_Map_Sharing "공유하기", IGUI_Map_Sharing_Everyone "전체 공개"), `KO/Tooltip.json`(Tooltip_Map_CantWrite "펜이나 연필이 필요합니다.")
- **B42**: 확인(게임 파일). 공유 표식이 42.21 멀티에서 실제로 보이는지는 직접 해 보지 않아 미확인

### 7-2. 채팅: 그냥 치면 근처, /all 은 전체, 한글은 \ 키
- **설명**: `T`(또는 `Enter`)로 채팅을 연다. 그냥 치면 근처 사람에게만 말한다(`/s`). `/all` 은 접속한 모두에게, `/y` 는 멀리 외치기(좀비도 끌린다), `/w 이름` 은 거리와 상관없는 귓속말이다. 입력 중 `Tab` 으로 채널을 바꾸고, 이름 앞부분을 치고 `Tab` 을 누르면 이름이 자동 완성된다. 한글은 「개선된 한글타이핑」 모드라서 윈도우를 영문 상태로 둔 채 `\` 로 한/영을 바꾼다. 음성 채팅 기본 키는 왼쪽 `Alt` 인데 전력질주와 같은 키라서, 음성을 쓰면 설정에서 하나를 바꾼다.
- **키**: `T` 「대화 창」, `Enter` 「대화 창 (보조)」, `Tab` 「대화 표시 전환」, `왼쪽 Alt` 「눌러서 말하기 키」, `\` 한/영(모드)
- **아이콘**: (없음)
- **근거**: `keyBinding.lua`(TOGGLE_CHAT = KEY_T, ALT_TOGGLE_CHAT = KEY_RETURN, SWITCH_CHAT_STREAM = KEY_TAB, ENABLE_VOICE_TRANSMIT = KEY_LMENU, SPRINT = KEY_LMENU), `PZ/media/lua/client/Chat/ISChat.lua`(10~16행: /say /s, /yell /y, /whisper /w, /faction /f, /safehouse /sh, /all, /admin /a), `KO/UI.json`(binding_Toggle chat 등), ini 기본값(GlobalChat = true, ChatStreams = s,r,a,w,y,sh,f,all), `data/mods.json`(개선된 한글타이핑). 채널 범위 설명: https://pzwiki.net/wiki/Server_settings (42.20.0)
- **B42**: 확인(게임 파일)

### 7-3. 역할 나누기와 같이 쓰는 기지
- **설명**: 의료·목공·요리·전기(발전기)·채집처럼 담당을 나누면 빨리 자리 잡는다. 기술 서적은 우리 서버에서 거의 바로 읽히고 읽어도 없어지지 않으니 한 권을 돌려 읽는다. 벽·문 같은 구조물은 목공 레벨이 높은 사람이 지어야 튼튼하다(레벨당 체력 +100). PvP 가 꺼져 있고 일반 플레이어는 은신처(안전가옥)를 지정할 수 없는 기본값이라, 기지 상자는 누구나 연다. 상자 버튼을 우클릭해서 「이름 바꾸기」로 "음식", "의료", "공구"라고 붙이고, 보관함 이름표 모드의 「수정」으로 아이콘·색까지 바꾸면 서로 찾기 쉽다.
- **키**: 상자 버튼 우클릭 「이름 바꾸기」(바닐라), 「수정」(Smarter Storage)
- **아이콘**: `Base.Hammer` → `Item_Hammer`, 상자 버튼 그림은 화면 캡처로
- **근거**: `data/mods.json`(MinutesPerPage = 0.1), `web/src/lib/server-config.mjs`(PVP = "false"), ini 기본값(PlayerSafehouse = false, AdminSafehouse = false), `KO/UI.json`(UI_ServerOption_PlayerSafehouse_tooltip "관리자와 플레이어가 은신처를 설정할 수 있습니다."), `PZ/media/lua/client/ISUI/ISInventoryPage.lua`(1383행 ContextMenu_RenameBag), `KO/ContextMenu.json`(ContextMenu_RenameBag "이름 바꾸기"), `WS/3290232938/mods/SmarterStorage/42/media/lua/client/SmarterStorage.lua`(131행, 419행), `.../Translate/KO/ContextMenu.json`(ContextMenu_SmarterStorage_Edit "수정"), 구조물 체력: https://pzwiki.net/wiki/Building (42.11.0). 역할 나누기 권장: https://games.gg/project-zomboid/guides/project-zomboid-how-to-play-with-friends/ (B42 한정 아님)
- **B42**: 확인(게임 파일). 역할 나누기는 일반론이라 B42 여부와 무관

### 7-4. 죽었을 때: 내 시체 찾아가기
- **설명**: 죽으면 가방과 소지품은 시체에 남고, 플레이어 시체는 시간이 지나도 자동으로 치워지지 않는다(서버 기본값). 감염된 채 죽었다면 사인과 상관없이 곧(0~1분) 좀비로 일어난다. 친구와 같이 가서 그 좀비를 처리하고 짐을 되찾는다. 새 캐릭터는 처음처럼 스폰 지역을 골라 시작한다(죽은 자리에서 부활은 꺼짐). 죽어도 채팅 알림이 안 뜨니 직접 알린다.
- **키**: (없음)
- **아이콘**: 무들 `PZ/media/ui/Moodles/64/Mood_Zombified.png`(좀비화), `PZ/media/ui/Moodles/64/Mood_Dead.png`
- **근거**: ini 기본값(RemovePlayerCorpsesOnCorpseRemoval = false, PlayerRespawnWithSelf = false, AnnounceDeath = false, DropOffWhiteListAfterDeath = false), `KO/UI.json`(각 키의 UI_ServerOption_*_tooltip), `Apocalypse.lua`(ZombieLore.Reanimate = 3), `KO/Sandbox.json`(Sandbox_ZReanimateTime "변이 시간", option3 "0-1분"), https://pzwiki.net/wiki/Knox_Infection (42.13.1, 감염된 채 죽으면 좀비로 일어남), Steam 42.20.0 패치노트(좀비가 된 플레이어 관련 수정): https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1839676055882259
- **B42**: 확인(게임 파일, 웹)

### 7-5. 스킬 보존 일지 제대로 쓰기
- **설명**: 제작창의 「스킬 회복 일지」 분류에서 「바인드 스킬 회복 일지」로 만든다(따로 배울 필요 없음). 재료는 공책·일기장·수첩 중 하나 + 접착제(또는 목공풀) + 가죽 조각 3 + 실(노끈·낚싯줄·치실도 됨). 가죽 조각은 입지 않은 가죽 장갑·가죽 재킷을 우클릭해서 「옷 찢기」로 얻는다(도구 필요 없음). 일지를 우클릭해서 「저널에 전사」로 기록하는데 펜이나 연필이 있어야 한다. 자동으로 기록되지 않으니 자주 한다. 기본값으로 기술 경험치와 배운 제작법은 다 돌아오지만, 근력·체력, TV·VHS 로 얻은 경험치, 직업·특성 시작 레벨, 처치 수는 안 남는다. 일지는 쓴 사람만 읽을 수 있고 몇 번이고 다시 읽을 수 있다. 들고 다니다 죽으면 좀비가 된 내 몸에서 꺼내야 하니 기지 상자에 둔다.
- **키**: 우클릭 메뉴 「저널에 전사」(기록), 「읽기」, 「옷 찢기」
- **아이콘**: 모드 그림 `WS/2503622437/mods/Skill Recovery Journal/common/media/textures/Item_SkillRecoveryJournal.png`(아이템 `Base.SkillRecoveryBoundJournal` · Icon `SkillRecoveryJournal`), `Base.Notebook` · Icon `Notebook` → `Item_Notebook`, `Base.LeatherStrips` · Icon `LeatherStrips` → `Item_LeatherStrips`, `Base.Thread` · Icon `Thread` → `Item_Thread`, `Base.Gloves_LeatherGloves` · IconsForTexture `GlovesLeatherBlackpng` → `Item_GlovesLeatherBlackpng`
- **근거**: `WS/2503622437/mods/Skill Recovery Journal/42.20.1/media/scripts/recipes/recipe_SRJ.txt`(BindSkillRecoveryJournal 재료), `.../42.20.1/media/sandbox-options.txt`(RecoveryPercentage 100, RecoverPassiveSkills 0, TranscribeTVXP false, RecoverProfessionAndTraitsBonuses false, KillsTrack 0, RecoverRecipes true, RecoveryJournalUsed false, SecurityFeatures 1), `.../42.20.1/media/lua/client/Skill Recovery Journal Context.lua`(100~110행, 필기구 필요·다른 사람 일지 막음), `.../common/media/lua/shared/Translate/KO/IG_UI.json`(IGUI_TranscribeIntoJournal "저널에 전사", IGUI_CraftCategory_SkillJournal "스킬 회복 일지"), `.../Translate/KO/Recipes.json`(BindSkillRecoveryJournal "바인드 스킬 회복 일지"), sandbox-options.txt(CraftRecipeNeedLearn 기본 false), `.../Translate/EN/Sandbox.json`(RecoverPassiveSkills = "Fitness + Strength"), `PZ/media/lua/shared/Definitions/ClothingRecipesDefinitions.lua`(Leather → Base.LeatherStrips, 도구 지정 없음), `PZ/media/lua/client/ISUI/ISInventoryPaneContextMenu.lua`(canRipItem: 입고 있으면 못 찢음), `KO/ContextMenu.json`(ContextMenu_RipClothing "옷 찢기"), `KO/ItemName.json`(Base.LeatherStrips "가죽 조각"), 모드 FAQ(기지에 보관 권장): https://steamcommunity.com/workshop/filedetails/discussion/2503622437/3198119216812488644/
- **B42**: 확인(모드 파일 42.20.1 판). 모드 아이템 이름은 모드 자체 번역으로 「바운드 저널」이고, Hx 통합 번역이 다르게 바꿀 수 있다

### 7-6. 서버 시간과 저장, 나갈 때
- **설명**: 아무도 접속해 있지 않으면 서버 시간이 멈춘다. 한 명이라도 있으면 시간이 흐르고 단수·단전 날짜도 다가온다. 맵은 사람이 그 구역을 떠날 때 저장된다(주기 저장 꺼짐). 끝낼 때는 하던 행동을 마치고 안전한 실내에서 `Esc` → 나가기로 나간다. 우리 서버는 호스트 PC 의 「서버 만들기」로 열기 때문에 호스트가 나가면 서버가 저장하고 꺼진다. 호스트는 다른 사람이 다 나간 뒤 마지막에 나간다.
- **키**: `Esc` 「주 메뉴」
- **아이콘**: (없음)
- **근거**: `web/src/lib/server-config.mjs`(PauseEmpty = "true"), ini 기본값(SaveWorldEveryMinutes = 0), `KO/UI.json`(UI_ServerOption_PauseEmpty_tooltip "서버에 접속해 있는 플레이어가 없을 때, 게임 세계의 시간이 정지됩니다.", UI_ServerOption_SaveWorldEveryMinutes_tooltip "…기본적으로 맵은 클라이언트가 불러와진 구역을 떠날 때에만 저장됩니다"), `docs/research/hosting.md`(86행 "호스트가 나가면 꺼짐", 352행 "호스트가 나가면 서버가 저장하고 꺼진다", 실측 로그 근거), https://pzwiki.net/wiki/Server_settings (42.20.0)
- **B42**: 확인(게임 파일). 접속이 갑자기 끊겼을 때 무엇까지 저장되는지는 미확인

---

## 그림 후보

### 쓰는 조건 (먼저 읽기)

- 게임 안 아이콘(`Item_*` 텍스처, `PZ/media/ui/` PNG)과 게임 화면 캡처는 모두 The Indie Stone 저작물이다. 비상업 팬 제작물이면 쓸 수 있고, 아래 문구를 잘 보이게 붙여야 한다(`PZ/terms and conditions.txt` 2.2항, 2022-10-06판. 최신판은 https://projectzomboid.com/blog/support/terms-conditions/ ).
  > "Thanks to The Indie Stone for creating Project Zomboid (https://projectzomboid.com/), which made this possible. This is an unofficial fan production for non-commercial purposes made under the Indie Stone Terms [약관 링크]"
- 지금 사이트 캐릭터 페이지의 문구("아이콘의 저작권은 The Indie Stone 에 있습니다")에는 위 문구가 없다. 꿀팁 페이지에 그림을 넣으면 위 문구를 함께 넣는 것이 안전하다(판단).
- pzwiki.net 본문 라이선스는 CC BY-SA 가 아니라 **CC BY-NC-SA 3.0** 이다(https://pzwiki.net/wiki/PZwiki:Copyrights ). 아래 표의 파일은 거의 모두 파일 페이지에 `{{License|The Indie Stone}}` 가 붙어 있어 위키 라이선스가 아니라 위 TIS 약관을 따른다. 표에서는 "TIS"로 줄였다.
- 이미지는 내려받지 않았고 URL 만 모았다. 버전은 파일 설명·업로드 메모·쓰인 문서 캡션으로 판단했고, 없으면 업로드 날짜로 추정했다(B42 unstable 공개일 2024-12-17 이전 = B41 이하).
- B42 화면이 위키에 없는 주제(상태창, 건축 창, 빗물받이, 도축, 웅크리기, 채팅, B42 바리케이드, B42 모닥불)는 우리 서버에서 `F10`(「스크린샷 찍기」)으로 직접 찍는 편이 낫다. 같은 TIS 약관이 적용된다.

### 화면 캡처 후보 표

| 팁 | 주제 | 파일 페이지 | 원본 이미지 URL | 업로드 | 게임 버전 | 라이선스 | 보이는 것 |
|---|---|---|---|---|---|---|---|
| 1-5, 6-1 | B42 화면 전체 안내 | https://pzwiki.net/wiki/File:InterfaceGuideB42.png | https://pzwiki.net/w/images/6/6e/InterfaceGuideB42.png | 2026-09-17 | B42 (확인, 설명) | TIS | 번호 붙은 B42 화면 안내(소지품, 상태창, 제작, 건축, 가구 옮기기, 탐색 모드, 동물, 지도, 무들, 단축키 칸). 1600x900. 꿀팁 첫 그림으로 좋음 |
| 6-1 | B42 제작창 | https://pzwiki.net/wiki/File:Crafting-menu-B42-recipe-details.png | https://pzwiki.net/w/images/8/88/Crafting-menu-B42-recipe-details.png | 2026-09-24 | B42 (확인, 파일명) | TIS | 분류, 검색·정렬, 필요 재료, 결과물. 1318x714 |
| 1-6, 7-1 | 지도 | https://pzwiki.net/wiki/File:Spawning_map.png | https://pzwiki.net/w/images/a/ac/Spawning_map.png | 2025-03-12 | B42 (확인, 캡션) | TIS | 시작 지역 고르는 지도. 게임 안 세계 지도·미니맵 캡처는 위키에 없음 |
| 1-6, 7-1 | 지도 | https://pzwiki.net/wiki/File:Knox_Country_42.11.png | https://pzwiki.net/w/images/0/09/Knox_Country_42.11.png | 2025-11-19 | 42.11 (확인, 캡션) | TIS | 녹스 카운티 전체 지도. 게임 화면인지 지도 사이트인지 출처 미기재 |
| 3-4, 3-6 | 루팅 창 | https://pzwiki.net/wiki/File:Looting.png | https://pzwiki.net/w/images/2/20/Looting.png | 2026-09-11 | B42 (추정) | TIS | 찬장에서 소지품으로 옮기는 중, 진행 막대. 1920x1080 |
| 4-1 | 상태창 붕대 | https://pzwiki.net/wiki/File:Bandage-Clean-to-Dirty.png | https://pzwiki.net/w/images/a/a8/Bandage-Clean-to-Dirty.png | 2023-10-20 | B41 (추정) | TIS | 깨끗한 붕대와 더러운 붕대 비교. B42 상태창 캡처는 위키에 없음 |
| 4-1 | 상태창 붕대 | https://pzwiki.net/wiki/File:Health-Article-Bandaging.png | https://pzwiki.net/w/images/b/b8/Health-Article-Bandaging.png | 2016-08-30 | 구버전 (추정) | TIS | 영어 UI 상태창, 붕대 감은 팔과 갈아야 할 붕대. 오래된 화면 |
| 4-3 | 무들: 메스꺼움(감염·식중독) | https://pzwiki.net/wiki/File:Mood_Nauseous.png | https://pzwiki.net/w/images/0/0a/Mood_Nauseous.png | 2025-01-23 | 42.1.0 (확인) | TIS | 아이콘. 게임 파일 `PZ/media/ui/Moodles/64/Mood_Nauseous.png` 와 같은 그림 |
| 4-3 | 무들: 감기 | https://pzwiki.net/wiki/File:Mood_Ill.png | https://pzwiki.net/w/images/9/9e/Mood_Ill.png | 2025-01-23 | 42.1.0 (확인) | TIS | 파일명은 Ill 이지만 감기 무들 그림(게임 파일에서도 감기 = Mood_Ill) |
| 4-3, 7-4 | 무들: 좀비화 | https://pzwiki.net/wiki/File:Mood_Zombified.png | https://pzwiki.net/w/images/0/0d/Mood_Zombified.png | 2025-01-23 | 42.1.0 (확인) | TIS | 아이콘 |
| 4-6 | 무들: 지루함 | https://pzwiki.net/wiki/File:Mood_Bored.png | https://pzwiki.net/w/images/b/b1/Mood_Bored.png | 2025-01-23 | 42.1.0 (확인) | TIS | 아이콘 |
| 4-6 | 무들: 우울 | https://pzwiki.net/wiki/File:Mood_Sad.png | https://pzwiki.net/w/images/1/13/Mood_Sad.png | 2025-01-23 | 42.1.0 (확인) | TIS | 아이콘 |
| 2-1 | 밟기 | https://pzwiki.net/wiki/File:Standing_on_zombie_neck.jpg | https://pzwiki.net/w/images/a/a8/Standing_on_zombie_neck.jpg | 2024-07-21 | B41 (추정) | TIS | 넘어뜨린 좀비를 밟고 서 있는 장면 |
| 3-1 | 손전등 | https://pzwiki.net/wiki/File:Flashlight_Example.png | https://pzwiki.net/w/images/e/e7/Flashlight_Example.png | 2024-01-10 | B41 (추정) | TIS | 밤에 손전등을 든 캐릭터. B42 조명 화면은 위키에 없음 |
| 3-1 | 손전등 | https://pzwiki.net/wiki/File:Hand_Torch_Example.png | https://pzwiki.net/w/images/4/46/Hand_Torch_Example.png | 2024-01-10 | B41 (추정) | TIS | 소형 손전등 사용 예 |
| 5-2 | 바리케이드 | https://pzwiki.net/wiki/File:WindowBarricades.png | https://pzwiki.net/w/images/3/31/WindowBarricades.png | 2017-02-18 | 36.4 (확인) | TIS | 판자·금속 바리케이드 종류. 오래된 화면 |
| 5-2 | 바리케이드 | https://pzwiki.net/wiki/File:KBHouseBarricaded.png | https://pzwiki.net/w/images/3/32/KBHouseBarricaded.png | 2024-05-28 | B41 (추정) | TIS | 바리케이드 친 집 |
| 5-4 | 빗물받이 | 없음 | 없음 | | | | 위키에 스크린샷이 없음. 직접 캡처 필요 |
| 5-5 | 발전기 정보 창 | https://pzwiki.net/wiki/File:Generator_UI_B42.png | https://pzwiki.net/w/images/0/00/Generator_UI_B42.png | 2025-11-08 | B42 (확인, 파일명) | TIS | 「발전기 정보」 창. 386x249 로 작음 |
| 5-5 | 발전기 범위 | https://pzwiki.net/wiki/File:Generator_Range.png | https://pzwiki.net/w/images/c/ca/Generator_Range.png | 2020-01-09 | B41 (추정) | TIS | 타일로 범위를 표시한 게임 화면. B42 는 위아래 3층까지 가므로 설명을 덧붙여야 함 |
| 5-5 | 발전기 범위 도식 | https://pzwiki.net/wiki/File:Generator_scheme.jpg | https://pzwiki.net/w/images/d/d3/Generator_scheme.jpg | 2022-08-28 | B41 (추정) | CC BY-NC-SA 3.0 | 팬이 그린 도식(위에서 본 범위) |
| 5-6 | 지하실 | https://pzwiki.net/wiki/File:Kentucky_State_Prison_Basement.png | https://pzwiki.net/w/images/9/9c/Kentucky_State_Prison_Basement.png | 2026-08-28 | B42 (확인, 업로드 메모) | TIS | 교도소 지하 내부. 2549x1417 |
| 5-6 | 지하실 | https://pzwiki.net/wiki/File:Riverside_Suites_Basement.PNG | https://pzwiki.net/w/images/d/d7/Riverside_Suites_Basement.PNG | 2026-08-30 | B42 (지하실은 B42 요소) | TIS | 리버사이드 호텔 지하 |
| 5-6 | 지하실 | https://pzwiki.net/wiki/File:Riverside_DT_Abandoned_Basement.PNG | https://pzwiki.net/w/images/1/15/Riverside_DT_Abandoned_Basement.PNG | 2026-09-01 | B42 (같은 이유) | TIS | 버려진 건물 지하 |
| 6-4 | 채집 탐색 모드 | https://pzwiki.net/wiki/File:Foraging_ru.png | https://pzwiki.net/w/images/9/96/Foraging_ru.png | 2026-08-02 | 42.20 (확인, 업로드 메모) | TIS | 러시아어 UI 채집 창. 영어·한국어 B42 캡처는 없음 |
| 6-4 | 채집 | https://pzwiki.net/wiki/File:Seed_Foraging.jpg | https://pzwiki.net/w/images/f/fc/Seed_Foraging.jpg | 2025-05-13 | B42 (추정) | TIS | 채집하다 씨앗을 찾은 장면. 321x219 로 작음 |
| 6-5 | 가축 구역 | https://pzwiki.net/wiki/File:Cattle-livestock-zone.jpg | https://pzwiki.net/w/images/c/c1/Cattle-livestock-zone.jpg | 2026-09-21 | B42 (동물은 B42 요소) | TIS | 소와 축사. 1920x1080 |
| 6-5 | 닭장 | https://pzwiki.net/wiki/File:Chicken-eggs-in-henhouse.jpg | https://pzwiki.net/w/images/4/43/Chicken-eggs-in-henhouse.jpg | 2026-09-21 | B42 (같은 이유) | TIS | 닭장 안 달걀 |
| 6-5 | 동물 스트레스 | https://pzwiki.net/wiki/File:Cow-stressed-by-zombies.jpg | https://pzwiki.net/w/images/b/ba/Cow-stressed-by-zombies.jpg | 2026-09-21 | B42 (같은 이유) | TIS | 근처 좀비 때문에 스트레스 받는 소 |
| 4-5, 5-1 | 모닥불 | https://pzwiki.net/wiki/File:Fire_project_zomboid.png | https://pzwiki.net/w/images/8/86/Fire_project_zomboid.png | 2023-11-29 | B41 (추정) | TIS | 불 붙은 모닥불. B42 모닥불(돌 3개)과 모양이 다를 수 있음 |
| 7 | 멀티·채팅 | 없음 | 없음 | | | | 채팅 화면 캡처가 위키에 없음. `Add_server_window.png` 는 라이선스 표기가 없어 뺐다 |

- 파일 페이지·원본 URL, 업로드 날짜, 라이선스 표기는 pzwiki MediaWiki API 와 파일 페이지로 확인했다(2026-10-18). 그림을 직접 열어 보지는 않아서 "보이는 것"은 파일 설명과 캡션을 옮긴 것이다.

### 게임 파일 그림 (아이콘) 정리

- 아이템 아이콘: 텍스처 이름 `Item_<Icon>`, `PZ/media/texturepacks/UI.pack`·`UI2.pack` 안. 팩 파일이라 꺼내려면 도구가 필요하다. 각 팁의 **아이콘** 줄에 이름을 적었다.
- 무들 그림: `PZ/media/ui/Moodles/<32|48|64|80|96|128>/` 의 PNG. 무들과 파일의 대응은 `PZ/projectzomboid.jar` 의 `zombie/ui/MoodleTextureSet.class` 안 순서로 확인했다. 지구력 = `Status_DifficultyBreathing.png`, 졸림 = `Mood_Sleepy.png`, 메스꺼움(감염·식중독) = `Mood_Nauseous.png`, 지루함 = `Mood_Bored.png`, 우울 = `Mood_Sad.png`, 감기 = `Mood_Ill.png`, 무거움 = `Status_HeavyLoad.png`, 좀비화 = `Mood_Zombified.png`, 악취(매연) = `Mood_NoxiousSmell.png`.
- 왼쪽 아이콘 줄 버튼: `PZ/media/ui/Sidebar/<48|64|80|96|128>/` 의 `Inventory_On`, `Heart_On`, `Carpentry_On`(제작창), `Build_On`(건축), `Map_On`, `Search_On`(구역 탐색), `AnimalZone_On`.

---

## 확인 못 한 것

1. 불빛(실내등·손전등)이 좀비를 끌어들이는지. 공식 패치노트와 위키에 근거가 없고 팬 자료가 엇갈린다(3-1).
2. 「약탈당한 건물 확률 최대치」 25 의 단위가 퍼센트인지. 퍼센트 해석은 팬 위키 근거다(3-5).
3. 좀비가 천 밧줄을 뜯어낼 수 있는지. 42.21 위키 변경 기록에 관련 수정이 있다는 보고와 "B41 댓글뿐"이라는 보고가 엇갈리고, Steam 42.21 공지(unstable·stable)에는 "rope" 가 없다(5-3).
4. 지도 표식을 「전체 공개」로 공유했을 때 42.21 멀티에서 실제로 다른 사람 지도에 보이는지. 코드와 번역만 봤다(7-1).
5. 접속이 갑자기 끊겼을 때 캐릭터와 맵이 어디까지 저장되는지(7-6).
6. 음성 채팅의 기본 동작(누르고 말하기인지 항상 켜짐인지). 기본 키가 왼쪽 Alt 로 전력질주와 겹친다는 것까지만 확인했다(7-2).
7. 좀비 감염 확률(긁힘 7·찢어짐 25·물림 100)을 jar 바이트코드에서 봤다는 것은 웹 조사 보고이고 내가 다시 보지는 않았다. 위키(42.13.1)와는 일치한다(4-3).
8. 지하실이 "막기 쉽다/막히면 갇힌다"는 커뮤니티 의견, 지하실에 둔 발전기도 유독 가스를 내는지는 추론이다(5-6).
9. 여럿이 할 때 기지로 시골이 나은지 마을이 나은지 정리된 의견을 찾지 못했다(5-1).
10. 기본 설정의 느린 좀비와 빠른 좀비 비율. 전력질주 좀비가 없다는 것만 설정으로 확인했다(2-4).
11. 실제 화면 문구. 한국어 표기는 바닐라 `KO/` 기준이고 우리 서버의 Hx 통합 번역이 바꿨을 수 있다. 스킬 보존 일지 아이템 이름(모드 자체 번역 「바운드 저널」)도 마찬가지다.
12. 한국 커뮤니티 근거. 아카라이브 좀보이드 채널, 디시 좀보이드 갤러리, 네이버·티스토리에서 B42 초보 팁으로 쓸 글을 찾지 못해(디시 목록 주소는 404) 한국 커뮤니티를 출처로 한 팁은 없다.
13. B42 게임 화면 캡처. 상태창, 건축 창, 빗물받이, 도축, 웅크리기, 채팅, B42 바리케이드, B42 모닥불은 pzwiki 에 B42 화면이 없다(그림 후보 표 참고).

## 조사 방법 메모

- 게임 파일은 42.21 설치본을 읽기만 했다. 아이템 아이콘은 `PZ/media/scripts` 의 모든 `item` 정의에서 `Icon`/`IconsForTexture` 와 `KO/ItemName.json` 이름을 뽑아 대조했다(임시 표는 scratchpad 에만 둠).
- pzwiki.net 은 일반 요청이 403 이라 MediaWiki API 와 브라우저로 읽었다. 페이지마다 적힌 버전(Page version)을 괄호에 적었다.
- 이 PC 에 받아진 창작마당 모드(Skill Recovery Journal 42.20.1 판, Proximity Inventory, Mini Health Panel, Has Been Read, Smarter Storage)의 파일을 직접 읽었다. Common Sense(3750253491)는 받아져 있지 않아 Steam 페이지로만 확인했다.
