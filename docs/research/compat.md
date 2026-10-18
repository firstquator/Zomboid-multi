# 모드팩 호환성 점검 (v2 14개 → v3 27개, 2026-10-18 확인)

`data/mods.json` v2 의 모드 14개(Mod ID 15개)를 42.21.0 에서 함께 켰을 때 서로 부딪히거나
42.21 과 맞지 않는 곳이 있는지 확인한 기록이다. v3 에서 13개를 더한 점검은 아래 "v3 추가 점검" 절에 있다.

## 결론

- **같이 켜도 막히는 문제는 찾지 못했다.** 격리한 폴더에서 이 PC 의 42.21.0 으로 전용 서버와
  클라이언트(한국어, 메인 메뉴까지)를 실제로 띄웠고, 바닐라 로그와 비교해 모드 때문에 새로 생긴
  오류는 0건이다. 서버 쪽에 새로 생긴 메시지는 "모드에 애니메이션 폴더가 없다"는 정보성 줄뿐이다.
- Lua 파일 경로가 다른 모드나 바닐라와 겹쳐서 통째로 덮이는 경우는 없다. 아이템·레시피 스크립트도
  겹치지 않는다. 샌드박스 옵션 이름도 겹치지 않는다.
- 같은 바닐라 함수를 둘 이상의 모드가 고치는 곳은 2곳이고, 둘 다 원래 함수를 이어 부르는 방식이라
  함께 동작한다.
- **다만 Skill Recovery Journal 은 우리 그룹에서 핵심 기능이 깨진다.** 한글이 들어간 Steam 닉네임으로 접속하면
  호스트가 게임을 다시 켠 뒤 일지 기록을 못 찾는다. 커뮤니티 이슈 #154 를 이 PC 의 실제 게임 엔진에서 재현했다
  (아래 "커뮤니티 보고" 1번). 42.21 멀티에서 신체 스킬이 안 적힌다는 보고도 10월에 여러 건이고, 09-04 뒤 업데이트가 없다.
  모두 영문 닉네임으로 바꾸지 않을 거라면 빼는 편이 낫다.
- 그다음은 Proximity Inventory 의 지구본 탭이 Better Sorting 과 함께 쓰면 사라진다는 보고(10-15)다.
  두 모드 코드에 겹치는 곳은 없어서 원인은 모르고, 게임 안에서 확인해야 한다.
- 정적 분석으로 찾은 주의점은 "발견 사항"에, 커뮤니티 보고는 "커뮤니티 보고"에 위험한 순서로 적었다.
- 게임 안(월드 접속 뒤)에서 인벤토리·우클릭·읽기 같은 실제 조작은 해 보지 않았다. 시작 전에 할 시험은
  "확인 못 한 점"에 우선순위대로 적었다.

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

## 커뮤니티 보고 (2026-10-18 조사, 위험한 순서)

창작마당 댓글·변경 기록·토론과 GitHub 이슈를 서브에이전트가 읽었다. steamcommunity.com 이 429 를 자주 돌려줘서
Mini Health Panel, Has Been Read, 한글타이핑은 페이지를 거의 읽지 못했다. 인용은 요약 모델을 거친 것이다.

### 1. Skill Recovery Journal: 42.21 멀티에서 핵심 기능이 안 된다는 보고가 많다

- 신체 스킬이 일지에 안 적힘: 10-13 "On MP B42.21, having same issue with physical skills like Running, Aiming, Reloading",
  10-12 "physical abilities are not transcribing to journal". 일부 XP 가 빨간 막대로 남는다는 보고(10-10, 10-13).
- 42.21 에서 안 됨: 10-08 "it doesnt work in last stable 42.21", 10-13 "broken for stable", 10-14 두 건.
- 멀티에서 일지가 비거나 지워짐: 09-26 "the journal contents get wiped after death", 10-05, 10-07.
- 작성자: 10-02 "I'm getting 0 errors testing", 10-14 "Mod works fine on my end". 마지막 업데이트 09-04.
- GitHub 에 답 없이 열린 이슈: #156(10-04, 42.21 멀티 "nothing else to add"), #155(09-10, **"hosted multiplayer server,
  not dedicated"** — 우리 방식), #154(09-09, 비ASCII(한중일) ID·사용자 이름이 깨져 키가 겹치고 저장된 XP 가 가려지거나 지워짐), #152(옮겨 적을 때마다 XP 증가).
- **우리 쪽에서 재현함 (#154, 한글 닉네임)**:
  - 우리 방식(Host + Steam 초대)에서는 Steam 닉네임이 그대로 접속 이름이 되고 한글도 막지 않는다
    (`hosting.md` 의 `GameClient.doConnectCoop` → `SteamFriends.GetPersonaName`, Host 경로는 `AllowNonAsciiUsername` 검사 없음).
  - SRJ 는 멀티에서 일지 장부 ID 를 `접속이름-시각-난수` 로 만들고(`Skill Recovery Journal Ledger.lua` 의 `mintJournalID`),
    장부를 자체 JSON 코덱으로 파일에 저장한다. 이 코덱은 문자열을 UTF-8 바이트로 가정하는데(`utf8Codepoints` 의 `s:byte`),
    Kahlua 문자열은 Java 문자열이라 한글이 한 글자로 들어온다. 저장은 `한` 로 맞게 쓰지만 불러올 때
    `string.char(0xED,0x95,0x9C)` 세 글자로 되돌려서 원래 이름과 달라진다.
  - 격리 서버(42.21.0, 실제 Kahlua)에서 SRJ 의 `jsonEncode` → `jsonDecode` 를 돌린 결과:
    `PlayerOne` 은 `roundtrip=true`, `한글닉네임`·`Kim민수` 는 **`roundtrip=false`, `usernameSame=false`**.
  - 장부는 프로세스가 뜬 뒤 처음 쓸 때 한 번만 디스크에서 읽는다(`ensureUserLoaded` 의 `loadedUsers` 캐시).
    그래서 **같은 세션 안에서는 멀쩡하다가, 호스트가 게임을 다시 켠 뒤부터 한글이 들어간 닉네임의 일지 기록을 못 찾고**,
    다음 저장 때 깨진 키로 덮어쓴다. 우리는 놀 때마다 호스트가 새로 여니 사실상 매번 해당한다.
  - 닉네임이 영문·숫자뿐인 사람은 해당하지 않는다. 다만 위의 "신체 스킬 안 적힘" 보고는 이름과 무관하다.
- 출처: https://steamcommunity.com/sharedfiles/filedetails/comments/2503622437 ,
  https://github.com/Chuckleberry-Finn/Skill-Recovery-Journal/issues/154
- 판단: **지금 그대로는 넣지 않는 편이 낫다.** 쓰려면 함께 하는 사람 모두 Steam 닉네임을 영문·숫자로 바꾸고 놀아야 하고,
  그래도 신체 스킬 문제는 시작 전 시험 1번으로 따로 확인해야 한다. 빼면 errorMagnifier·Alert System 도 SRJ 때문에 넣은 것이라
  같이 뺄 수 있다(둘은 SRJ 를 빼면 필요한 모드가 없다).

### 2. Proximity Inventory + Better Sorting: 지구본 탭이 사라진다는 보고

- 10-15 junhugun(Proximity 댓글): "안되시는 분 들은 "Better Sorting" 이라는 모드를 구독 하고 있지 않은지 확인해보세요." /
  "전 저걸 지우니까 지구본이 다시 보였습니다." 작성자는 한국어 글이라 답하지 못했다.
- Proximity 의 42.21 멀티 보고는 엇갈린다. 안 됨(09-29, 10-02, 10-04, 09-12 호스트 서버), 됨(10-06 "120+ mods" 서버,
  10-13 작성자 "The mod still works as usual").
- 우리 쪽 근거: Better Sorting 은 `ISInventoryPage`·`ISInventoryPane`·`ISLootWindow` 를 건드리지 않고(바닐라 함수는 유체 행동
  `complete`/`stop` 만 감쌈), 두 모드가 함께 고치는 함수도 없다. 불러오기 오류도 없다. 코드로는 설명이 안 된다.
- 출처: https://steamcommunity.com/sharedfiles/filedetails/comments/2847184718
- 판단: 시작 전 시험 2번으로 확인한다. 지구본이 안 보이면 둘 중 하나를 뺀다.

### 3. Common Sense: 가구 배치 불가 보고, Smarter Storage 이름표가 사라진다는 보고

- 09-29 "cannot place furniture with this mod? i think the new update/hotfix broke it", 10-03 같은 보고. 작성자 답과 변경 기록 언급이 없다.
- 09-20 Smarter Storage 버그 스레드: "'common sense' & 'reload all magazines' … remove the icons and names given to containers
  from smart storage". 어느 Common Sense 인지 링크가 없다.
- 둘 다 10-12 v3.6.0(서버 권한 방식으로 개편) 전 보고다. 현재 3.6.1 에는 인벤토리 보관함 버튼(`ISInventoryPage`)이나
  가구 배치(`ISMoveable*`)를 건드리는 코드가 없다.
- 출처: https://steamcommunity.com/sharedfiles/filedetails/comments/3750253491 ,
  https://steamcommunity.com/workshop/filedetails/discussion/3290232938/4522260786595826312/?ctp=5
- 판단: 낮음~중간. 시작 전 시험 3번에서 가구 하나 옮겨 보고 이름표 붙인 상자를 확인한다.

### 4. 접속 때 "doesn't exist on the client" (Mod Update and Alert System)

- 09-18 직접 호스팅 멀티: "doesn't exist on the client: chuckleberryfinnmodding_modchangelog.lua". 작성자: "There's a bug with
  luachecksum, you most likely need to disable that. It's not related to any particular mod." 08-22 "disable LuaCheckSum, just ask
  your friends to make sure they unsub/resub".
- 42.21 서버 설정에 `DoLuaChecksum` 이 있다(`zombie/network/ServerOptions`, 기본 `true`).
- 판단: 지금 설치 스크립트는 그대로 둔다. 친구가 이 오류로 못 들어오면 그 사람이 모드 구독을 풀었다 다시 하고, 그래도 안 되면
  호스트 ini 에서 `DoLuaChecksum=false` 로 바꾼다(친구끼리 비공개 서버라 치트 검사가 꺼지는 손해는 작다).

### 5. 그 밖

- Hx 통합 번역: 09-27 "멀티 서버 만들 때 '서버가 시작 과정에서 중단되었습니다'" 보고(답 없음, 42.21 정식 하루 전).
  우리 격리 서버 테스트는 Hx 를 넣고 정상 시작했다. map_symbols.bin 증가(08-21)와 전단지 흰 화면(08-26)은 09-07·08-27 수정 뒤 재보고가 없다.
  09-28 GitHub 커밋 "42.21 EN 원문 기준 번역 갱신".
- errorMagnifier: 09-28 "errors 가 나는데 열어 보면 0개" 보고 2건. 표시 문제라 플레이에는 영향이 없다.
- Smarter Storage: 이름표는 보관함 오브젝트의 ModData 에 쓰고 `transmitModData()` 로 보낸다. 멀티에서 다른 사람에게도 보이는 구조다
  (`mods.md` 의 "확인 못 한 점" 하나에 대한 답, 실제 화면은 확인 못 함).
- Stack ALL Fix: 마지막 업데이트 05-14, 42.20.2·42.20.3 멀티 정상 보고(08-06, 08-22), 42.21 언급 없음.
- Named skill VHS tapes: 작성자 "번역을 바꾸는 모드보다 뒤에 로드"(09-17). 지금 순서가 맞다.
- Has Been Read: 42.13 시기 "표시를 많이 하면 ModData 가 커져 롤백" 토론이 있었다(오래된 보고).
- Better Sorting: 아이템 분류값을 바꿔서 샌드박스 "카테고리별 전리품 희귀도"가 바닐라 아이템 1,284개에 덜 먹는다(GitHub #105, 열림). 기존에 알던 내용.

## 시작 전 시험 (우선순위)

격리 테스트로는 볼 수 없는 것들이다. 호스트 PC 에서 실제로 "서버 만들기"로 열고 한 명이 Steam 초대로 들어와서 한다.

1. **Skill Recovery Journal**(남기기로 했다면): 모두 영문 Steam 닉네임으로 접속한 상태에서, 달리기·조준 같은 신체 스킬과
   목공 같은 일반 스킬을 조금씩 올린 뒤 일지에 옮겨 적기 → 일지 툴팁에 모두 나오는지 → **호스트가 게임을 껐다 다시 연 뒤**
   캐릭터를 죽이고 새 캐릭터로 읽어서 돌아오는지.
2. **Proximity Inventory**: 상자 근처에서 인벤토리 창에 지구본 탭이 보이는지, 거기서 꺼내지는지.
3. **Common Sense / Smarter Storage**: 가구 하나 들어 옮기기, 상자에 이름표 붙이고 다른 사람 화면에서도 보이는지.
4. Stack All(반쯤 쓴 소모품 두 개 이상 → 우클릭 "모두 합치기"가 한 번만 뜨고 합쳐지는지), Has Been Read(읽은 책 표시),
   한글 채팅 입력, 미니 체력 창, 미니맵 한국어 지명.

## 확인 못 한 점

- 월드에 들어가서의 실제 조작(위 "시작 전 시험"). 서버·클라이언트 모두 "불러오기까지 오류 없음"만 확인했다.
- Steam 으로 호스트하고 다른 PC 가 접속하는 흐름(체크섬 일치 포함). 테스트는 `-nosteam` 이었다.
- 오래 플레이할 때의 성능, 저장 파일 크기(Hx 의 `map_symbols.bin` 보고 등).
- Mini Health Panel, Has Been Read, 한글타이핑의 최근 커뮤니티 보고(429 로 거의 못 읽음).
- 정적 분석은 정규식 기반이라 동적으로 만든 함수 이름이나 문자열로 부르는 함수는 놓칠 수 있다.

## v3 추가 점검 (후보 15개 → 13개 넣음, 27개, 2026-10-18)

"무기 내구도 보이기, 상태를 쉽게 보는 UI, 그 밖에 있으면 좋을 모드" 요청으로 고른 후보 15개를 위와 같은 방법으로 점검했다.
고른 과정과 뺀 후보는 `mods.md` 의 "2026-10-18 추가: 화면·편의 모드 13개" 절에 있다.

### 판정

| 모드 | 판정 | 근거 |
|---|---|---|
| NeatUI Framework (3508537032) | 넣는다 | Neat Crafting 필수. 바닐라 함수는 없을 때만 채운다 |
| Clean HotBar (3461263912) | 넣는다 | 새 오류 0. `ISHotbar:render` 교체는 이 모드의 목적(그리기), 나머지는 감쌈 |
| CH Status HUD (3776182375) | 넣는다 | 바닐라 함수 안 고침, 이벤트만 씀 |
| Moodle Quarters (2854030563) | 넣는다 | Lua 1개, 바닐라 함수 안 고침 |
| Neat Crafting (3502080466) | 넣는다 | 교체로 잡힌 3곳 모두 원래 함수를 부름. 빼기 어렵다는 관리 위험은 기록 |
| Better Generator Info (3576056135) | 넣는다 | 발전기 창 함수 모두 감쌈 |
| Swap It (2366717227) | 넣는다 | 교체 3곳이 42.21 원본 + 추가분 |
| Picking Meister (3422220305) | 넣는다 | 모두 감쌈 |
| Drag Bodies Faster (3393821407, `DBFaster50`) | 넣는다 | 애니메이션 속도 값만 다름(jar 로 확인) |
| Map Symbol Size Slider (2734705913) | 넣는다 | 모두 감쌈 |
| MGRS (2928660831) | 넣는다 | 모두 감쌈, 띄어쓰기 든 Mod ID 도 실제로 로드됨 |
| Rain Cleans Blood (2956146279) | 조건부 | 옷 툴팁 수치가 안 바뀌는 것을 코드로 확인(보기만 어긋남). 장착 불가 보고 1건은 코드 경로 없음 |
| Combat Text (2286124931) | 조건부 | 좀비가 많으면 렉(작성자 인정), B42 멀티 검증 기록 없음. 화면만 바꾸는 모드라 언제든 뺄 수 있음 |
| Show Wall Health (3002666175) | **뺀다** | 서버가 클라이언트가 보낸 벽 체력을 믿고 낮춘다(아래 "뺀 모드") |
| Show Weapon Stats (2762715872) | **뺀다** | 무기 툴팁을 영어로 통째로 다시 그린다, 멀티 탄약 표시 버그 미해결 |

### 확인 방법

1. 받기: SteamCMD 로 후보 15개와 팩 14개를 모두 새로 받았다. Required items: Neat Crafting → NeatUI Framework,
   Swap It·MGRS → errorMagnifier + Mod Update and Alert System(둘 다 이미 팩에 있음).
2. 정적 분석: `mod_analyze.py --add` 15개. Drag Bodies Faster 는 한 아이템에 25·50·60·70·80% 다섯 Mod ID 가 있고 서로
   `incompatible` 이라 `DBFaster50` 만 넣었다.
3. 바닐라 교체 비교와 jar 확인(CFR 0.152 로 42.21.0 `projectzomboid.jar` 디컴파일):
   `PlayerDraggingCorpse`, `ChooseGameInfo$Mod`·`GameVersion`, `Clothing`·`InventoryItem`·`BloodClothingType`.
4. 로딩 테스트: 후보 15개를 모두 넣은 29개 팩(Mod ID 30개)과, 2개를 뺀 최종 27개 팩(Mod ID 28개)을 각각 격리 서버·클라이언트로
   띄웠다. 결과는 아래 "로딩 테스트".
5. 커뮤니티: 서브에이전트가 창작마당 댓글·변경 기록·토론을 읽었지만 429 로 Moodle Quarters, Better Generator Info,
   Map Symbol Size Slider, Picking Meister, Drag Bodies Faster, MGRS 는 못 읽었다. 이 6개는 후보를 고를 때 직접 읽은
   페이지의 최근 댓글(모드마다 6~10개)만 근거다.

### 로드 순서

- NeatUI Framework 를 라이브러리 바로 뒤(3번)에 둔다. Mini Health Panel 이 NeatUI 보다 먼저 로드되면 서버가 시작 중 꺼진다는
  보고가 있었고(08-13, Mini Health Panel 댓글), NeatUI 작성자도 "쓰는 모드보다 먼저"라고 한다. 이 순서로 서버가 정상 시작했다.
  Mini Health Panel 은 10-04 업데이트로 NeatUI 계열과 부딪히던 알림 창을 없앴다.
- Clean HotBar 는 작성자 권장대로 아래쪽(25번). 42.21 직후 "차에 못 타고 총을 못 쏨" 보고가 로드 순서를 맨 아래로 옮겨 풀렸다는 댓글이 있다.
- Hx 통합 번역과 Named skill VHS tapes 는 그대로 맨 끝.

| # | Mod ID | # | Mod ID | # | Mod ID |
|---|---|---|---|---|---|
| 1 | errorMagnifier | 10 | P4HasBeenRead | 19 | RainCleansBlood |
| 2 | ChuckleberryFinnAlertSystem | 11 | MiniHealthPanel | 20 | WorldMapNameSymbols |
| 3 | NeatUI_Framework | 12 | CHStatusHUD | 21 | MapSymbolSizeSlider |
| 4 | BetterSortCC | 13 | moodle_quarters | 22 | MGRS (FMCCYAYFGLE) |
| 5 | SmarterStorage | 14 | Neat_Crafting | 23 | Improved-KorChat |
| 6 | ProximityInventory | 15 | BetterGeneratorInfo | 24 | SkillRecoveryJournal |
| 7 | stack_all_42Roy | 16 | CombatText | 25 | CleanHotBar |
| 8 | P4PickingMeister | 17 | SwapIt | 26 | Hx_KR_Vanilla, Hx_KR_Mod |
| 9 | VB_CommonSense | 18 | DBFaster50 | 27 | NamedSkillVHSTapes |

`require` 로 실제 순서가 바뀌는 것은 v2 와 같다(Alert System 이 errorMagnifier 앞으로).

### 발견 사항 (넣은 모드)

1. **Clean HotBar 가 Common Sense 의 총 탄약 표시를 끈다.** `commonsense_patch.lua` 가 게임 시작 때 클라이언트에서
   `SandboxVars.CommonSense.GunStats = false` 로 바꾼다. 탄약 수는 Clean HotBar 의 핫바·손 칸 표시로 대신 본다. 의도된 호환 처리다.
   - `ISHotbar:render` 는 통째로 교체(핫바 그리기가 이 모드의 목적), `refresh`·`update`·`attachItem`·`canBeAttached` 등은 감싼다.
     핫바를 고치는 다른 모드는 Swap It 뿐이고 고치는 함수가 겹치지 않는다.
   - "감싸려는 함수가 없음"으로 잡힌 `CEWeaponDurabilityAlert.displayTime` 은 함수가 아니라 숫자 필드다(오탐).
2. **Swap It**: `ISHotbar:activateSlot`·`equipItem`·`isAllowedToActivateSlot` 를 통째로 바꾸지만, 42.21 원본을 문자열까지 그대로
   옮기고 맞바꾸기·빈 칸에 걸기만 더했다. 안에서 부르는 `attachItem`·`canBeAttached` 는 Clean HotBar 가 감싼 판을 탄다.
   Clean HotBar 버그 게시판에 "Swap It 과 충돌하는 것 같다"는 질문(08-26)이 있지만 답은 확인하지 못했다(시작 전 시험 6번).
   모드 안 `KO/UI.json` 은 UTF-16 을 잘못 바꿔 키가 깨져 있어 안 쓰이고, Hx_KR_Mod 가 키 7개를 모두 번역한다.
3. **Neat Crafting**: "교체"로 잡힌 `ISEntityUI.GetWindowClass`·`GetComponentPanelClass`·`ISWidgetCraftLogicInputControl:createDynamicChildren`
   은 모두 원래 함수를 먼저 부르고 결과만 바꾼다(오탐). xuiskin `Base.default` 를 덮어 작업대 창도 Neat 창으로 열리고,
   모드 옵션에서 끄면 바닐라 창 클래스로 되돌린다. **한 번 넣은 저장에서 빼면 접속이 안 될 수 있다**는 보고(10-04)가 있으니
   뺄 때는 작성자가 안내하는 Safe Uninstall Support 를 쓴다.
4. **NeatUI Framework**: `ISUIElement` 중심 좌표 함수 7개는 `if not ISUIElement.X then` 안에서만 정의한다. 42.21 에는 모두 있어 바꾸지 않는다.
5. **Drag Bodies Faster**: Lua 없이 바닐라 애니메이션 XML 12개를 덮는다. 42.21 원본과 비교하면 BOM 과 `m_SpeedScale` 만 다르다.
   - 끌기 4개: `WalkSpeedGrapple` → `1.20`. jar 의 `PlayerDraggingCorpse.enter` 가 이 변수를 해골 1.2, 그 밖 0.8 로 정한다.
     그래서 일반 시체만 0.8 → 1.2(50% 빠름)이고 해골은 그대로다. 바닐라 규칙이 깨지지 않는다.
   - 들어 올리기 4개: 0.80 → 1.20/1.00. 내려놓기 4개는 BOM 만 다르다.
6. **Rain Cleans Blood (조건부)**: 입은 옷은 부위별 피·때(`item:setBlood/setDirt`, 그림 값)만 낮춘다. jar 를 보면 툴팁의
   "피투성이·더러움" 막대는 `Clothing.bloodLevel`·`dirtyness` 필드이고, 게임은 피가 새로 묻을 때 `BloodClothingType.calcTotalBloodLevel`
   로 다시 계산한다. 이 모드는 다시 계산하지 않아서 **비가 온 뒤 모습은 깨끗해도 툴팁 막대는 남는다**(다음에 피가 묻으면 맞춰진다).
   바닐라 빨래 메뉴는 이 필드로 뜨므로 빨래는 그대로 된다. 10-10 댓글의 설명과 방향은 다르지만 "화면과 수치가 어긋난다"는 점은 맞다.
   10-04 "장비를 벗고 입지 못함"은 1건이고, 코드는 피·때 값과 `resetModelNextFrame`·`syncVisuals` 만 건드려 장착 경로가 없다.
7. **Combat Text (조건부)**: `onCreatePlayer` 같은 이벤트 처리 함수를 `local` 없이 전역으로 정의한다. Mini Health Panel 도 전역
   `onCreatePlayer` 를 정의해서 나중에 로드되는 Combat Text 가 전역 이름을 덮는다. 하지만 두 모드 모두 정의 직후
   `Events.OnCreatePlayer.Add(onCreatePlayer)` 로 그때의 함수를 등록하므로 둘 다 실행된다. 이 이름을 직접 부르는 곳은
   Skill Recovery Journal 뿐인데 SRJ 것은 같은 파일의 `local` 함수다. 무해.
   - 체력바는 클라이언트의 `zombie:getHealth()` 로 그린다. 멀티 참가자 화면에서 좀비 체력이 갱신되는지는 확인하지 못했다(시작 전 시험 9번).
8. **CH Status HUD**: 글자를 자를 때 UTF-8 바이트를 가정한다(`dropLastChar`). Kahlua 에서 한글은 한 글자(0xAC00 이상)로 들어와
   한 글자씩 정상으로 지워진다. 끝 글자가 0x80~0xBF(°, · 등)면 앞 글자까지 같이 지워질 수 있지만 표시용이라 무해.
   `;` 키는 채팅 입력 중(`ISChat.instance.isTyping`)에는 무시한다.
9. 같은 바닐라 함수를 여러 모드가 고치는 곳이 3곳 늘었고 모두 감싸기다: `ISContextMenu.onJoypadDown`(Smarter Storage, Picking Meister),
   `ISInventoryPane:renderdetails`(Has Been Read, Picking Meister), `MainOptions.apply`(Has Been Read, Combat Text).
10. Better Generator Info 의 `getGenOffColor`, Map Symbol Size Slider 의 `ExtraMapSymbolsUI:OnEvent` 는 조건문 안이다.
    MGRS 와 Map Symbol Size Slider 는 서로 다른 지도 함수를 감싸고, WorldMap Name Symbols·Hx 와 겹치는 함수가 없다.

### 뺀 모드

- **Show Wall Health (3002666175)**: 우클릭 메뉴가 열릴 때마다 클라이언트가 근처 벽·문의 자기 쪽 체력과 오브젝트 순번
  (`getObjectIndex`)을 서버로 보낸다. 서버(`WallHealthServer.lua`)는 그 칸의 같은 순번 오브젝트를 꺼내, 클라이언트 값이 더 낮으면
  실제 체력을 그 값으로 낮추고 모두에게 알린다. 클라이언트 값이 오래됐거나 순번이 어긋나면 수리한 벽이 도로 깎이거나 다른 벽·문
  체력이 바뀔 수 있다. 커뮤니티의 서버 `InvocationTargetException`(7번째 줄, 2025-05·12)이 바로 이 순번 조회 줄이다.
  42.21 업데이트(09-28) 뒤 "창이 안 뜬다"(10-13)에 답이 없다. `versionMax=42.21.0` 은 주·부 번호만 비교하므로
  (`ChooseGameInfo$Mod.isAvailableSelf`, `GameVersion.getInt = 주*1000+부`) 42.21.x 핫픽스에서는 켜진다. 문제는 그쪽이 아니다.
- **Show Weapon Stats (2762715872)**: 모드 옵션 `compatibilityMode` 의 기본값이 `false` 라, 무기 툴팁을 원래 함수를 부르지 않고
  "Condition:", "Damage:" 같은 영어 문구로 통째로 다시 그린다. 한국어 게임에서 무기 툴팁이 영어가 된다. 멀티에서 탄약 수가 안 보인다는
  보고(09-18)를 작성자가 "다음 패치에 고치겠다"(10-08)고 했지만 08-16 뒤 업데이트가 없다.

### 한국어 (v3 추가분)

| 모드 | KO 로 채워짐 | 출처 |
|---|---|---|
| Clean HotBar | 9/10 | 모드 + Hx (빠진 1개는 모드 옵션 제목) |
| CH Status HUD | 72/74 | 모드 + Hx (빠진 2개는 샌드박스 쪽 모드 이름, 키 설정 화면 이름) |
| Neat Crafting | 117/118 | 모드 + Hx |
| Better Generator Info | 25/26 | 모드 |
| Map Symbol Size Slider | 1/1 | 모드 + Hx |
| Swap It | 7/7 | Hx (모드 KO 파일은 깨짐) |
| Picking Meister | 18/18 | Hx |
| Rain Cleans Blood | 21/21 | Hx |
| MGRS | 5/5 | Hx (샌드박스 문구) |
| Combat Text | 35/35 | Hx |
| NeatUI Framework, Moodle Quarters, Drag Bodies Faster | 번역 키 없음 | 화면 글자 없음(`no-text`) |

- `%1` 자리표시 개수가 EN 과 다른 KO 키는 0개다.

### 로딩 테스트

- 후보 15개를 모두 넣은 29개 팩(Mod ID 30개): 서버 `ok`(스택 트레이스 0, 새 오류·경고 0, 알려진 무해 1종:
  `AdvancedAnimator$1.visitFileFailed` 104줄), 클라이언트 `ok`(새 오류·경고 0). 두 로그 모두 30개 Mod ID 의 `loading`/`overrides` 줄이 있다.
- 최종 27개 팩(Mod ID 28개): 서버 `ok`(스택 트레이스 0, 새 오류·경고 0, 알려진 무해 1종), 클라이언트 `ok`(새 오류·경고 0).
  두 로그 모두 `loading` 줄 28개, 뺀 두 모드(`KAMER_WallHealth`, `showweaponstats`) 줄은 0개.
- 불러오기까지만 본 것이다. 월드 안 조작은 아래 "시작 전 시험"으로 한다.

### 커뮤니티 보고 (v3, 위험한 순서)

1. Rain Cleans Blood: 42.21 정식 뒤 업데이트 없음. "장비를 벗고 입지 못함, 모드를 빼도 그대로"(10-04, 1건, 답 없음),
   옷 피·때 수치 어긋남(10-10, 위 6번에서 코드로 확인), 폭우에도 차 피가 안 씻김(10-04, 답 없음).
2. Combat Text: 좀비가 많을수록 렉·튕김(09-01, 09-03, 10-10, 작성자 09-11 인정), "로컬 서버에서 안 된다"(09-24, 답 없음).
3. Neat Crafting / NeatUI: 호스트 서버에서 "Missing dictionary string"·"file doesn't exist on the client" 로 튕긴 보고(09-17)에
   작성자가 서버·클라이언트 파일이 달라서라고 답했다. 모드가 업데이트되면 호스트가 게임을 다시 켜고 모두 같은 버전을 받아야 한다.
   멀티에서 칼을 갈면 튕긴다는 보고(09-25)는 로그 요청 뒤 해결 여부 불명.
4. Clean HotBar: 모드 업데이트 뒤 서버에 못 들어감(10-07, 작성자 "서버를 다시 켜 버전을 맞춰라"). 우리는 매번 호스트가 새로 열어 대체로 해당 없음.
5. Swap It: 양손 무기를 든 가드 상태에서 바꾸면 등 무기가 풀림(10-08, 답 없음). 컨트롤러는 안 됨(작성자).
6. CH Status HUD: "42.21 에서 잘 된다"(10-15), "이제 안 된다"(10-12, 답 없음). 니코틴 금단 스트레스·Sickness 표시는 10-16 업데이트 설명에 고쳤다고 적혀 있다.
- 출처: 각 모드의 `https://steamcommunity.com/sharedfiles/filedetails/comments/<번호>`, Clean HotBar 버그 스레드
  https://steamcommunity.com/workshop/filedetails/discussion/3461263912/588433820963856761/

### 시작 전 시험 (v3 추가, 앞 절의 1~4번 다음)

5. **Clean HotBar**: 핫바에 날 무기·총을 걸고 내구도 막대·탄약 표시가 나오는지. 가방에서 같은 무기 여러 개를 핫바 칸으로 끌어 놓아 바닥에 떨어지지 않는지.
6. **Swap It + Clean HotBar**: 등에 무기를 걸고 다른 무기를 든 채 핫바 숫자키 → 두 무기가 맞바꿔지는지. 빈 칸 숫자키 → 든 무기가 걸리는지.
7. **CH Status HUD**: `;` 로 패널이 뜨는지, 채팅 중 `;` 를 쳐도 패널이 안 바뀌는지. **Moodle Quarters**: 배고픔 아이콘에 단계 칸이 보이는지.
8. **Neat Crafting**: 제작 창(B)과 작업대 창이 열리는지, 레시피 검색이 되는지.
9. **Combat Text**: 참가자 화면에서도 좀비를 때리면 체력바가 줄어드는지. 안 줄면 빼도 된다.
10. **Rain Cleans Blood**: 비 오는 날 피 묻은 옷을 입고 있다가 모습이 깨끗해지는지, 그 뒤 옷을 벗고 다시 입을 수 있는지.
11. **MGRS**: 지도(M) → 옵션에서 셀 격자(CellGrid)를 켜면 마우스 칸의 좌표가 뜨는지, 미니맵에 마우스를 올리면 내 좌표가 뜨는지.

## 다시 점검하는 법

`.claude/skills/zomboid-mod-check/` 스킬이 이 문서의 방법(받기, 정적 분석, 함수 비교, 한국어, 격리 로딩 테스트, 커뮤니티 조사)을
스크립트로 묶어 둔 것이다. 새 모드를 넣거나 게임 빌드가 오르면 그 스킬로 다시 돌린다.
