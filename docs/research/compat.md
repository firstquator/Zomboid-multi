# 모드팩 호환성 점검 (v2, 14개, 2026-10-18 확인)

`data/mods.json` v2 의 모드 14개(Mod ID 15개)를 42.21.0 에서 함께 켰을 때 서로 부딪히거나
42.21 과 맞지 않는 곳이 있는지 확인한 기록이다.

## 결론

- **같이 켜도 막히는 문제는 찾지 못했다.** 격리한 폴더에서 이 PC 의 42.21.0 으로 전용 서버와
  클라이언트(한국어, 메인 메뉴까지)를 실제로 띄웠고, 바닐라 로그와 비교해 모드 때문에 새로 생긴
  오류는 0건이다. 서버 쪽에 새로 생긴 메시지는 "모드에 애니메이션 폴더가 없다"는 정보성 줄뿐이다.
- Lua 파일 경로가 다른 모드나 바닐라와 겹쳐서 통째로 덮이는 경우는 없다. 아이템·레시피 스크립트도
  겹치지 않는다. 샌드박스 옵션 이름도 겹치지 않는다.
- 같은 바닐라 함수를 둘 이상의 모드가 고치는 곳은 2곳이고, 둘 다 원래 함수를 이어 부르는 방식이라
  함께 동작한다.
- 주의할 점은 아래 "발견 사항"에 위험한 순서로 적었다. 지금 고쳐야 할 것은 없고, Stack All 은
  작성자 업데이트 때 다시 볼 필요가 있다.
- 게임 안(월드 접속 뒤)에서 인벤토리·우클릭·읽기 같은 실제 조작은 해 보지 않았다. 아래
  "확인 못 한 점" 참고.

## REA 에 대해

- REA(Reverse Engineer Anything): https://github.com/morluto/rea , npm 패키지 `rea-agents`.
  MIT 라이선스. 코딩 에이전트에 MCP 로 역공학 도구를 붙여 주는 CLI 다. 네이티브 바이너리(Ghidra·
  Hopper·IDA), JS/Electron, .NET, Android APK 등을 다룬다.
- 설치(2026-10-18): `npm install --global rea-agents@6.5.0`, 그리고 Claude Code 에만 MCP 와 스킬을 등록했다.
  - `rea setup --client claude_code --yes` → `~/.claude.json` 의 `mcpServers.rea`,
    `~/.claude/skills/reverse-engineer-anything`. 바꾸기 전 설정은 `~/.claude.json.rea.backup` 에 있다.
  - fnm 의 셸별 임시 경로(`fnm_multishells\...`)가 등록되지 않게, 고정 경로
    `%APPDATA%\fnm\node-versions\v22.23.1\installation\node.exe` 로 실행해서 등록했다. Node 기본 버전을
    바꾸면 `rea setup --client claude_code` 를 다시 돌려야 한다.
  - MCP 도구는 Claude Code 를 다시 켜야 보인다. 해제는 `rea uninstall`.
- **이 점검에는 REA 가 맞지 않았다.**
  - 좀보이드 모드는 Lua·텍스트 원문이라 역공학할 것이 없다.
  - 게임 본체는 Java(`projectzomboid.jar`)인데 REA 6.5.0 은 일반 JAR/class 를 분석하지 않는다.
    `rea inspect-artifact projectzomboid.jar` 결과는 ZIP 목록(format: zip)뿐이고 다음 단계 제안이 없었다.
    Windows 의 Ghidra 경로는 네이티브 PE 만 받는다(문서의 Windows Ghidra P0).
  - 그래서 게임 쪽 규칙은 CFR 0.152 로 jar 의 해당 클래스를 디컴파일해서 확인했다(아래).

## 확인 방법

1. **모드 실물**: SteamCMD 익명 로그인으로 14개를 모두 새로 받았다(2026-10-18). 받은 버전의 창작마당
   마지막 업데이트(UTC)는 `mods.json` 의 `lastUpdated` 와 같다.
2. **게임 규칙**(42.21.0 `projectzomboid.jar` 디컴파일):
   - 버전 폴더: 이름을 `주*1000 + 부` 로 읽어 게임 버전(42.21 → 42021) 이하 중 가장 큰 폴더를 쓴다.
     패치 자리(42.20.**1**)는 무시한다. `common` 은 늘 함께 읽고, 같은 경로면 버전 폴더가 이긴다
     (`ZomboidFileSystem.getModVersionDirName`, `loadMod`).
   - `mod.info` 의 `require` 는 요구한 모드 앞에 자동으로 끼워 넣는다(`loadModAndRequired`).
     그래서 `Mods=` 줄 순서와 실제 순서가 다를 수 있다.
   - 파일 덮어쓰기: 모드 순서대로 같은 상대 경로를 나중 모드가 덮는다. Lua 는 바닐라 파일을 먼저,
     그다음 모드별로(모드 안에서는 경로 알파벳순) 실행한다(`LuaManager.LoadDirBase`).
   - 번역 JSON 과 `sandbox-options.txt` 는 모드마다 따로 읽는다. 경로가 같아도 서로 지우지 않고,
     번역은 키 단위로 나중 모드 값이 이긴다(`Translator.tryFillMapFromMods`, `CustomSandboxOptions`).
     로그의 `mod "X" overrides media/lua/shared/translate/...` 줄은 이 경우라 무시해도 된다.
3. **정적 분석**(스크립트, 바닐라 Lua 1,395개와 모드 Lua 101개 대조):
   파일 덮어쓰기, 같은 바닐라 함수를 고치는 모드, 원래 함수를 이어 부르는지, 감싸려는 함수가 42.21 에
   있는지, `Events.X` 이벤트 이름(게임 등록 262개 + Lua 등록), `require` 대상 파일, `instanceof` 클래스,
   게임이 Lua 에 노출한 Java 메서드 이름, 아이템·레시피 정의, 번역 키 충돌과 `%1` 자리표시, 샌드박스 옵션 이름.
   걸린 항목은 코드를 열어 하나씩 확인했다(지역 변수를 바닐라 함수로 잘못 잡은 것 등은 뺐다).
4. **실제 실행**(사용자 `Zomboid` 폴더와 Steam 은 건드리지 않음, `-nosteam -cachedir=<임시 폴더>`):
   - 전용 서버: `Mods=` 를 설치 스크립트와 같은 순서로 넣고 새 월드 생성 → `*** SERVER STARTED ***`.
     Lua 스택 트레이스 0건. 바닐라 호스트 로그(`coop-console.txt`)에 없는 오류는
     `AdvancedAnimator$1.visitFileFailed`(모드에 `AnimSets`/`actiongroups` 폴더가 없다는 알림, 모든 모드 공통)뿐.
   - 클라이언트: 창 모드·한국어로 메인 메뉴까지 → 바닐라 `console.txt` 에 없는 오류·경고 0건.
     `[Improved-KorChat] loaded`, `[ErrorMagnifier] Registered debug report for: SkillRecoveryJournal`,
     `[HxKO] UIText: 17 strings for active mods`, `ISStackAllMod: B42.17 consolidate chain patch active` 확인.
   - 처음 서버를 짧은 경로(`SANGHY~1`)로 띄웠을 때는 `couldn't find ...transcribejournal.xml` 로
     초기화가 멈췄다. 같은 파일을 긴 경로로 다시 띄우면 정상이라 테스트 환경 문제로 판단했다.
     실제 호스트는 창작마당 폴더(`C:\Program Files (x86)\Steam\...`)에서 읽으므로 해당 없다.

## 실제 로드 순서

`require` 때문에 앞의 두 라이브러리 순서가 바뀐다. 문제는 아니고, 게임이 알아서 맞춘다.

| # | Mod ID | 쓰는 버전 폴더 | require |
|---|---|---|---|
| 1 | ChuckleberryFinnAlertSystem | 42.0 | |
| 2 | errorMagnifier | 42.15 | ChuckleberryFinnAlertSystem |
| 3 | BetterSortCC | 42 | |
| 4 | SmarterStorage | 42 | |
| 5 | ProximityInventory | 42 | |
| 6 | stack_all_42Roy | 42 | |
| 7 | VB_CommonSense | common 만 있음 | |
| 8 | P4HasBeenRead | 42.15 | |
| 9 | MiniHealthPanel | 42 | |
| 10 | WorldMapNameSymbols | 42.0 | |
| 11 | Improved-KorChat | 42 | |
| 12 | SkillRecoveryJournal | 42.20.1 | ChuckleberryFinnAlertSystem, errorMagnifier |
| 13 | Hx_KR_Vanilla | 42 | |
| 14 | Hx_KR_Mod | 42 | |
| 15 | NamedSkillVHSTapes | 42 | |

- 서로를 `incompatible` 로 적은 모드는 없다. Smarter Storage(LetMeThink 등), Skill Recovery Journal
  (BurdSurvivalJournals 등), Common Sense(BB_CommonSense), Hx_KR_Vanilla(42buildTranslateKorean)가
  적은 모드는 이 팩에 없다.

## 발견 사항 (위험한 순서)

### 1. Stack All Fix/revamp: 옛 파일이 남아 함께 실행된다 (지금은 동작, 업데이트 때 재확인)

- `42/media/lua/client/New folder/` 에 옛 Lua 4개(`ISStackAllMod.lua`, `ISStackAllMod_public.lua`,
  `StackAll.lua`, `StackAll_public.lua`)가 남아 있다. 게임은 하위 폴더까지 모든 `.lua` 를 실행한다.
- 실행 순서(경로 알파벳순)가 `ISStackAllMod.lua` → `New folder/*` 4개 → `StackAll.lua` 라서 지금은 이렇게 된다.
  - 시간 행동 클래스 `ISStackAllMod` 는 `New folder/ISStackAllMod_public.lua` 판이 최종이다(루트 판을 덮음).
    둘 다 "B42.17 compatibility controller" 계열이라 동작은 같은 방향이다.
  - 바닐라 합치기 행동 패치는 `_stackAllChainFixPatched` 표시 덕에 한 번만 걸린다.
  - 우클릭 "모두 합치기" 항목은 옛 `New folder/StackAll.lua` 가 먼저 넣고, 나머지 둘은 같은 이름이 있으면
    건너뛰어서 한 번만 뜬다. 실제 실행 함수(`ConsolidateAll`)는 마지막에 정의된 루트 판이다.
  - 옛 파일의 "행동 시간 0" 주입(`LuaTimedActionNew.new` 패치)은 파일마다 따로 둔 지역 표시를 보는데,
    그 표시를 켜는 옛 함수가 루트 판으로 덮여서 실제로는 켜지지 않는다.
- 이 모드는 바닐라 `ISConsolidateDrainable`(소모품 합치기)의 `nextItem`·`runAgain`·`perform` 을
  클라이언트에서 통째로 바꾼다. 42.21 바닐라와 함수 구성이 같고, 모드가 고치려는 `perform` 의 문제(빈
  원본을 아직 안 지운 상태에서 `self.drainable` 만 확인)도 42.21 에 그대로 있다. 바닐라의 "합치기"도
  이 코드를 탄다.
- 위험: 작성자가 파일을 정리하거나 일부만 고치면 순서가 바뀌어 메뉴가 두 번 뜨거나 옛 코드가 이길 수 있다.
  업데이트가 올라오면 다시 확인한다. 깨지면 대안은 `docs/research/mods.md` 의 Stack All [B42 MP](3816647906).

### 2. Hx 통합 번역: 바닐라 함수 몇 개를 통째로 바꾼다 (42.21 과 일치)

- `Hx_KR_Vanilla` 가 한국어 어순 때문에 아래 바닐라 함수를 복사해서 바꾼다. 문자열을 뺀 구조를 42.21 원본과
  비교했다.
  - `ISBaseIcon:doContextMenu`(채집 아이콘 우클릭): 42.21 과 같다. 옛 버전에 있던 "버리기" 항목 코드가
    남아 있지만 `if self.onClickDiscard then` 안이고, 42.21 에는 `onClickDiscard` 가 없어서 실행되지 않는다.
  - `ISWorldObjectContextMenu.doBrushToolOptions`, `BrushToolManager`, `FireBrushUI`,
    `ISSearchManager.createDebugContextMenu`: 디버그·관리자 도구라 일반 플레이와 무관하다. 구조는 42.21 과 같다.
  - `MapUtils.initDirectoryStreetData` 는 원래 함수를 이어 부른다(한국어 거리 이름 추가).
- 위험: 바닐라가 이 함수들을 바꾸는 패치가 나오면 Hx 업데이트 전까지 옛 동작이 남는다.

### 3. 한글 폰트 설정: WorldMap Name Symbols 것을 Hx 가 덮는다 (문제 없음)

- 둘 다 `media/fonts/KO/fonts.txt` 를 넣고, 나중에 로드되는 Hx_KR_Vanilla 판이 쓰인다.
- Hx 판이 WorldMap Name Symbols 판의 SDF 글꼴 항목을 모두 포함한다. 다른 점은 `SdfCaveat` 하나로
  WorldMap Name Symbols 는 작은 한글 글꼴, Hx 는 큰 한글 글꼴을 쓴다.

### 4. 번역 키: Hx_KR_Mod 가 모드 자체 한국어를 덮는다 (의도된 동작)

- 키 단위로 나중 모드가 이긴다. 값이 다른 KO 키 수:
  Hx_KR_Vanilla→Hx_KR_Mod 174, Skill Recovery Journal→Hx_KR_Mod 64, Hx_KR_Vanilla→Named skill VHS tapes 62,
  Common Sense→Hx_KR_Mod 40, Better Sorting→Hx_KR_Mod 37, 그 밖 2~6개씩.
- Named skill VHS tapes 가 맨 뒤라 테이프 이름은 이 모드 것이 쓰인다(작성자 안내와 같다).
- 위험: 모드가 업데이트로 문구 뜻을 바꾸면 Hx 쪽 옛 번역이 남을 수 있다. `%1` 같은 자리표시 개수가
  EN 과 다른 키는 0개라 깨진 문장은 없다.

### 5. 같은 바닐라 함수를 둘 이상이 고치는 곳 (함께 동작)

| 함수 | 모드 | 방식 |
|---|---|---|
| `ISInventoryPage:onBackpackRightMouseDown`(보관함 버튼 우클릭) | Smarter Storage, Proximity Inventory | 둘 다 원래 함수를 먼저 부르고 덧붙인다 |
| `MainScreen:onEnterFromGame` | Mod Update and Alert System(교체), errorMagnifier(감쌈) | 알림 시스템의 교체본이 42.21 원본과 내용이 같다 |

- 나머지는 모드마다 다른 함수를 고친다. 인벤토리 쪽만 보면 Better Sorting 은 아이템 분류값, Has Been Read 는
  `ISInventoryPane:renderdetails`, Proximity 는 `ISInventoryPage` 의 다른 함수들과 `ISLootWindowContainerControls`,
  Smarter Storage 는 `ISInventoryPage`·`ISContextMenu` 의 다른 함수들이다.

### 6. 그 밖에 확인하고 문제없다고 본 것

- **Common Sense**: `ISCampingMenu.onAddAllFuel` / `onAddMultipleFuel` 를 교체하지만 42.21 원본에서 공용
  `fuelItemList` 를 지역 변수로 바꾼 것뿐이다. `ISHandcraftAction.complete` 등은 원래 함수를 이어 부른다.
  `common/` 에만 `mod.info` 가 있는데, 게임은 `common/mod.info` 만 있어도 모드로 인정한다.
- **Mini Health Panel**: 체력 패널의 치료 처리기를 복사해 쓰지만 `local BaseHandler` 라 바닐라와 섞이지 않는다.
  B41 용 `ModOptions:loadFile()` 호출은 `ModOptions` 가 있을 때만 실행된다.
- **Better Sorting**: GameNight, New Music 지원 파일의 `require` 대상이 없지만 해당 모드가 켜져 있을 때만 실행된다.
- **Has Been Read**: Inventory Tetris 용 `require` 도 `if TetrisEvents then` 안이다.
- **Proximity Inventory**: `self:isPageLeft()` 는 CleanUI 용이고 `if self.isPageLeft then` 안이다.
- **WorldMap Name Symbols**: KO 번역 JSON 3개(`ContextMenu`, `Sandbox`, `UI`)에 끝 쉼표가 있다. 엄격한 JSON 은
  아니지만 게임은 정식판에서 비엄격 모드(`Core.IS_DEV` 가 아닐 때)로 읽고, 실제 클라이언트에서
  `JSON Error` 없이 올라왔다. 지도 API(`getSymbolsAPIv2`, `getAPIv3` 등) 호출은 모두 42.21 jar 에 있다.
- **Skill Recovery Journal**: 42.20.1 폴더(versionMin 42.20.2)를 쓴다. 바닐라 함수는 감싸기만 한다.
  루트 `media/` 는 B41 용이라 B42 에서 읽지 않는다.
- 모든 모드의 `Events.X` 이름이 42.21 에 있다. `instanceof` 클래스 이름도 모두 있다.

## 한국어 (실물 파일 기준)

모드의 EN 번역 키가 최종 KO(바닐라 → 로드 순서대로 모드)에서 채워지는 비율.

| 모드 | KO 로 채워짐 | 출처 | mods.json 과 다른 점 |
|---|---|---|---|
| Mod Update and Alert System | 6/6 | 모드 자체 | `none` 으로 적혀 있지만 UI 키 6개는 KO 가 있다. 소식 본문은 영어일 수 있다 |
| errorMagnifier | 번역 키 없음 | | 그대로(영어 하드코딩) |
| Better Sorting | 92/92 | 모드 + Hx | |
| Smarter Storage | 63/63 | 모드 + Hx | |
| Proximity Inventory | 18/19 | Hx | 빠진 1개는 키 설정 화면 이름 |
| Stack All Fix | 7/7 | 모드 자체 | `none`·"확인 못 함" → KO 들어 있음(`IG_UI.json`, `Sandbox.json`) |
| Common Sense | 65/66 | 모드 + Hx | 빠진 1개는 샌드박스 쪽 모드 이름 |
| Has Been Read | 42/44 | 모드 + Hx | 빠진 2개는 CD·VHS 대상 옵션 |
| Mini Health Panel | 5/5 | Hx | "확인 못 했다" → 현재 문구 5개 모두 번역됨 |
| Skill Recovery Journal | 77/78 | 모드 + Hx | 빠진 1개는 샌드박스 쪽 모드 이름 |
| Named skill VHS tapes | 164/166 | 모드 | |

- 번역 품질(기계번역 여부)은 보지 않았다.

## 확인 못 한 점

- 월드에 들어가서의 실제 조작: 보관함 이름표, 주변 상자 탭, 모두 합치기, 읽음 표시, 일지 쓰기·읽기,
  미니 체력 창, 한글 채팅 입력. 서버·클라이언트 모두 "불러오기까지 오류 없음"만 확인했다.
- Steam 으로 호스트하고 다른 PC 가 접속하는 흐름(체크섬 일치 포함). 테스트는 `-nosteam` 이었다.
- 오래 플레이할 때의 성능, 저장 파일 크기(Hx 의 `map_symbols.bin` 보고 등).
- 정적 분석은 정규식 기반이라 동적으로 만든 함수 이름이나 문자열로 부르는 함수는 놓칠 수 있다.
