# 모드팩 조사 기록 (v1, 2026-10-18 확인)

`data/mods.json` 을 만들 때 확인한 근거와 뺀 후보를 정리한다.

## 기준과 확인 방법

- 게임 빌드: **42.21.0 (public stable)**. 2026-09-23 unstable, 2026-09-28 stable 로 나왔다. 2026-10-18 기준으로 42.21.x 핫픽스 공지는 없다.
  - Steam 공지 "Build 42.21 Stable Released"(2026-09-28): https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1844751498231307
  - PZwiki Version history(42.21.0 = 2026-09-28 stable): https://pzwiki.net/wiki/Version_history
- 모드마다 아래를 확인했다.
  - Steam Web API `GetPublishedFileDetails`: 제목, 썸네일, 마지막 업데이트(UTC), 태그, 설명의 `Mod ID:` 줄. 빌드 스크립트가 모든 Mod ID 가 설명에 그대로 있는지 검사한다.
  - 워크숍 페이지 HTML: Required items 영역, 최근 댓글 20~25개(42.20/42.21 멀티 문제 보고).
  - 변경 기록, GitHub 저장소(있는 경우).
- 바닐라 미니맵: 샌드박스 `Map.AllowMiniMap` (기본 false). PZwiki Server settings(42.20.0 기준) 의 SandboxVars 예시로 확인: https://pzwiki.net/wiki/Server_settings

## 최종 목록 (11개, 로드 순서대로)

| # | 모드 | Workshop ID | Mod ID | 마지막 업데이트 | 한국어 | 근거 |
|---|---|---|---|---|---|---|
| 1 | Better Sorting | 2313387159 | BetterSortCC | 2026-09-12 | 모드에 포함(기계번역) | https://steamcommunity.com/sharedfiles/filedetails/?id=2313387159 , https://github.com/ChthonicKnight/BetterSorting (42/media/lua/shared/Translate/KO/IG_UI.json) |
| 2 | Smarter Storage | 3290232938 | SmarterStorage | 2026-09-03 | 모드에 포함(설명 기준) | https://steamcommunity.com/sharedfiles/filedetails/?id=3290232938 |
| 3 | Proximity Inventory B42.20+ | 2847184718 | ProximityInventory | 2026-08-30 | Hx 팩 | https://steamcommunity.com/sharedfiles/filedetails/?id=2847184718 , https://github.com/mxswat/pz-ProximityInventory (KO 폴더 없음) |
| 4 | Stack ALL Fix/revamp (42.19+) | 3723627943 | stack_all_42Roy | 2026-05-15 | 확인 못 함 | https://steamcommunity.com/sharedfiles/filedetails/?id=3723627943 |
| 5 | Common Sense [B42.20+] | 3750253491 | VB_CommonSense | 2026-10-12 | 모드에 포함(v3.6.0) | https://steamcommunity.com/sharedfiles/filedetails/?id=3750253491 , https://steamcommunity.com/sharedfiles/filedetails/changelog/3750253491 |
| 6 | Has Been Read | 2544353492 | P4HasBeenRead | 2026-10-10 | 모드에 포함(Hx 시트 기준) | https://steamcommunity.com/sharedfiles/filedetails/?id=2544353492 |
| 7 | Mini Health Panel | 2866258937 | MiniHealthPanel | 2026-10-04 | Hx 팩 | https://steamcommunity.com/sharedfiles/filedetails/?id=2866258937 |
| 8 | [B42/41] WorldMap Name Symbols | 3342110208 | WorldMapNameSymbols | 2026-09-22 | 한국어 전용 | https://steamcommunity.com/sharedfiles/filedetails/?id=3342110208 |
| 9 | [B42]개선된 한글타이핑 | 3780552862 | Improved-KorChat | 2026-08-28 | 한국어 전용 | https://steamcommunity.com/sharedfiles/filedetails/?id=3780552862 |
| 10 | Hx's 좀보이드 통합 번역 | 3040632900 | Hx_KR_Vanilla, Hx_KR_Mod | 2026-10-09 | 번역 팩 | https://steamcommunity.com/sharedfiles/filedetails/?id=3040632900 , 번역 목록 시트: https://docs.google.com/spreadsheets/d/1mvICZ2zet0rIlq-07fFTJWmXbkvNSl0WoWujl3-ULkA |
| 11 | Named skill VHS tapes | 2732294885 | NamedSkillVHSTapes | 2026-09-05 | 공식 번역 사용 | https://steamcommunity.com/sharedfiles/filedetails/?id=2732294885 |

- 11개 모두 워크숍 태그에 "Build 42" 가 있다.
- 의존성: 11개 모두 워크숍 Required items 영역이 비어 있다(같은 방법으로 '92 AM General M998 페이지에서 that DAMN Library 가 잡히는 것을 보고 검사 방법이 맞는지 확인했다). 설명에 나오는 Mod Options 는 B41 용(2169435993)이고 B42 는 내장 Mod Options 를 쓰므로 넣지 않았다. 그래서 의존 트리는 전부 독립이다.
- 로드 순서: Hx 통합 번역은 번역 대상 모드들 뒤(10번). Named skill VHS tapes 는 작성자가 "번역을 바꾸는 모드보다 뒤에 로드"하라고 해서 맨 끝(11번).

## "스택" 해석 근거

- 사용자가 "스택"이라고만 했으므로 두 가지 해석을 비교했다.
  1. 같은 종류 아이템 한 번에 옮기기(테라리아식 Quick Stack): **42.12 부터 바닐라 루팅 창에 "Transfer Same Type / Loot Same Type" 버튼**이 생겼다. Smart Stack 작성자(https://steamcommunity.com/sharedfiles/filedetails/?id=966221273)와 Easy Drop'n'Loot 작성자(https://steamcommunity.com/sharedfiles/filedetails/?id=2871469707)가 각자 설명에 적었다. 42.20 에서는 "스택 아이템 옮기기 재작업(큰 묶음 옮기는 시간 단축)"도 들어갔다(PZwiki Build 42.20.0).
  2. 반쯤 쓴 소모품 합치기(Stack All): 워크숍에서 "stack" 으로 검색하면 가장 구독이 많은 모드가 Stack All(약 29만)이고, Hx 시트도 "소모성 아이템 합치기"로 분류한다.
- 1번은 바닐라로 해결되므로 2번을 모드 자리로 골랐다. 원본 Stack All(2629074154)은 42.14 부터 42.20 까지 "작동 안 함" 댓글이 이어져서, 42.20.2·42.20.3 멀티 정상 보고가 있는 수정판 3723627943 을 넣었다.

## 뺀 후보와 이유

| 모드 | Workshop ID | 뺀 이유 |
|---|---|---|
| Common Sense (원본) | 2875848298 | 마지막 업데이트 2025-03-07. 42.20 정식 대응 업데이트 없음 |
| Common Sense B42.20 - Community Compatibility Fix | 3717968421 | 쓸 만하지만 구독 7.8만으로 이어받기판(35만)보다 적고, 마지막 업데이트 2026-09-19 |
| Common Sense Reup [42.21.+] | 3792900796 | 구독 7천, 설명이 짧아 변경 내용 확인 불가 |
| Stack All (원본) | 2629074154 | 2024-12 이후 업데이트 없음, 42.14 부터 작동 안 함 댓글 다수 |
| Stack All [B42 MP] | 3816647906 | 2026-10-09 공개, 구독 43, 사용 보고 없음. 수정판(3723627943)이 깨지면 대안 |
| Smart Stack | 966221273 | 작성자가 42.12 바닐라 버튼으로 필요 없어졌다고 명시 |
| Easy Drop'n'Loot | 2871469707 | 작성자가 42.12 에 바닐라가 같은 기능을 넣었다고 명시 |
| Manage Containers | 2650547917 | 멀티에서 지정 카테고리가 다른 플레이어에게 동기화 안 됨(2026-09-13 댓글), Better Sorting 분류 변경 때마다 카테고리 불일치(BetterSorting GitHub #106), Smarter Storage 와 메뉴 충돌 보고 |
| Tidy Up Meister | 2769706949 | 42.21 에서 여러 행동이 깨진다는 보고 뒤 2026-10-10 v2.0 으로 전면 재작성, 이후에도 문제 보고가 있음. 바닐라 42.8 부터 자동 되돌려놓기 기능이 있음 |
| Skill Recovery Journal | 2503622437 | 죽어도 스킬을 되찾게 해 난이도를 크게 낮춤 |
| Proximity Inventory 포크들 | 3669550831, 3740165370, 3498294068, 3624308198 | 원작자 원본(2847184718)이 B42.20+ 로 갱신됨. 3669550831 은 스스로 원본으로 가라고 안내 |
| 지도 한글화 (B42) / Addon | 3407686437 / 3532909971 | 스폰 선택 화면 지도만 한글화(게임 안 지도·미니맵 아님). 본체는 2025-01 이후 업데이트 없음 |
| NB 지도 한글 라벨 | 3782062909 | 월드맵 라벨 한글화지만 구독 493, Hx_KR_Vanilla 의 한국어 거리 이름과 겹침 |
| [B42] Korean Region Names Only | 3816978070 | 모드 맵(Grapeseed 등) 전용, 구독 16 |
| WorldMap Name Symbols - Preservation Fix | 3811074719 | 구독 51, 작성자가 실제 게임·전용 서버 검증은 안 했다고 명시 |
| Street Names on Minimap | 3784739919 | 영어 거리 이름 표시, 구독 235 |
| 미니맵 교체 모드(TwisTonFire minimap, MiniMap by Minidoracat, Project Viewpoint Minimap) | 3572564421, 3763913359, 3810179295 | 바닐라 미니맵으로 충분, UI 충돌 위험만 늘어남 |
| 다른 한국어 번역 팩 | 3812394747, 3782584849, 3735405869, 3652024434, 3392975164, 3386745988 | 구독이 적거나 오래됐고 Hx 팩과 겹침 |
| 프로젝트 좀보이드 갤러리 모드 번역 [PZGKO] | 2900444089 | Hx 설명에 "함께 쓰면 좋은 모드"로 나오지만 필수는 아니고, 마지막 업데이트가 2025-09-01 |
| 42.15 이후 모드 한국어 번역_a43 | 3690094119 | Common Sense 번역용으로 검토했으나 Common Sense 3.6.0 에 KO 가 들어가 불필요 |
| [B42] 한글 채팅 자동 입력 | 3818346758 | 2026-10-17 공개 베타, 구독 20 |
| errorMagnifier | 2896041179 | 오류 찾기 도구라 편의 모드가 아님. 문제가 생겼을 때만 잠깐 넣어 쓰면 된다 |
| Mod Update and Alert System | 3077900375 | 이 팩 안에 이걸 의존으로 요구하는 모드가 없음 |
| Map Legend UI / Read While Walking | 2710167561 / 2845952197 | 마지막 업데이트가 42.20 정식 이전(2026-03 / 2025-08) |
| Equipment UI, Reorder The Hotbar, Reorder Containers | 2950902979, 2903771337, 2901962885 | 제목에 [DISCONTINUED] |
| [B41&B42] Show Wall Health | 3002666175 | (v3 점검) 우클릭할 때마다 클라이언트가 자기 쪽 벽 체력을 보내고, 서버는 그 값이 더 낮으면 실제 체력을 그 값으로 낮춘다(`WallHealthServer.lua`). 오브젝트를 순번(`getObjectIndex`)으로 찾아서, 클라이언트 값이 오래됐거나 순번이 어긋나면 수리한 벽이 도로 깎이거나 다른 벽·문 체력이 바뀔 수 있다. 같은 줄의 서버 오류 보고, 42.21 에서 창이 안 뜬다는 10-13 보고가 해결되지 않음 |
| [41][42] Show Weapon Stats MP | 2762715872 | (v3 점검) 기본 설정에서 무기 툴팁을 영어 문구로 통째로 다시 그려 바닐라 한국어 툴팁이 사라진다(호환 모드는 각자 모드 옵션에서 켜야 함). 멀티에서 탄약 수가 안 보이는 버그를 작성자가 인정했지만 08-16 뒤 업데이트 없음. 내구도는 Clean HotBar 가 보여 준다 |
| Item Condition Overlay (BUILD 42 STABLE) | 3641048285 | 인벤토리에도 내구도 막대를 그리지만 42.20.4 뒤 "대부분 안 나온다"는 보고 여럿(전용 서버 포함), 마지막 업데이트 08-09, 한국어 없음. Clean HotBar 와 같이 쓰면 둘 다 핫바를 그린다 |
| [B41/B42] Item Condition, Condition On Dash, Weapon Condition Indicator, Equipment Condition (42.13-16) | 2852309899, 3306168142, 3412262177, 3646678287 | 2024-12~2026-03 이후 업데이트 없음(42.20 정식 이전) |
| [B41\|B42] Simple Status | 2867431511 | 상태 막대 패널로 가장 유명하고 KO 내장이지만, 켜고 끄는 기본 키가 `\` 라 한글 채팅의 한/영 키와 겹친다. 42.21·호스트 멀티에서 "안 된다"는 댓글과 "된다"는 댓글이 섞여 있고, 마지막 업데이트가 42.21 정식 이전(09-13) |
| Modern Status [B42] | 3451167732 | 원형 게이지 등 꾸밀 수 있는 범위가 가장 넓지만 CH Status HUD 와 같은 일을 한다. 둘 중 하나만 넣는다 |
| Minimal Display Bars 계열 | 3388844542, 3775659041 | 같은 종류의 상태 막대. 원작(2004998206)과 겹치는 이어받기판이 여럿이다 |
| [B42] Moodle Descriptions Expanded | 3389003300 | 무들 설명 문구를 바꾸는 모드라 한국어 게임에서는 번역이 있어야 의미가 있다. 다른 모드와 함께 쓰면 적용 안 된다는 9월 보고 |
| Dynamic Moodles, Neon moodle levels | 3674800555, 3392116408 | 무들 아이콘 교체. Moodles in lua 프레임워크가 따로 필요하다. Moodle Quarters 로 단계 구분은 충분 |
| KillCount | 2553809727 | "42.21 에서 안 된다" 댓글(10-15) |
| DayZ Health HUD | 3818297469 | 2026-10-18 공개, 사용 보고 거의 없음 |

## 확인 못 한 점

- 워크숍 파일을 직접 내려받아 열어 보지 않았다(SteamCMD 를 쓰지 않음). 한국어 포함 여부는 설명·변경 기록·GitHub·Hx 시트로만 판단했다.
- Stack ALL Fix/revamp: KO 포함 여부와 42.21 작동 여부. 마지막 업데이트가 42.20 정식 이전이다.
- Has Been Read 의 KO: Hx 시트(2025-10 자료)의 "Mod" 표시만 근거다.
- Mini Health Panel: 모드 자체 번역은 영어·프랑스어뿐이다(2026-10-04 변경 기록: https://steamcommunity.com/sharedfiles/filedetails/changelog/2866258937 ). Hx 팩이 새 문구까지 번역하는지는 확인 못 했다.
- Hx 통합 번역: 42.20.2 전용 서버에서 Hx_KR_Vanilla 가 map_symbols.bin 을 키운다는 보고(2026-08-21)와 전단지 흰 화면 보고(2026-08-26) 뒤에 변경 기록에 "42.20.4 전단지·신문 이미지 수정"(08-27), "addKoreanStreetData 수정"(09-03), "멀티 심볼 코드 수정"(09-07)이 올라왔다( https://steamcommunity.com/sharedfiles/filedetails/changelog/3040632900 ). 실제로 해결됐는지는 직접 확인 못 했다. Hx 시트의 번역 대상 목록도 2025-10 자료라 최신이 아닐 수 있다.
- Smarter Storage 의 이름표가 멀티에서 모두에게 같이 보이는지.
- Better Sorting 은 워크숍 댓글이 꺼져 있어 GitHub 이슈로 대신 확인했다.

## 호스트 메모

- 샌드박스 설정 → Meta → In-game Map → "Allow Mini-Map"(`Map.AllowMiniMap`) 을 켠다.
- 모두 게임 언어를 한국어로 둔다.
- WorldMap Name Symbols: 옵션 → 모드 → WorldMap Name Symbols 에서 "미니맵에 심볼 텍스트를 보이게 합니다"를 체크한다. 멀티에서 지명이 안 보이면 펜을 우클릭해 "모드 심볼 일괄 추가"를 누른다.
- 한글 채팅: 윈도우 입력기는 영문으로 두고, 채팅창에서 `\` 키로 한/영을 바꾼다.
- Better Sorting: 샌드박스의 카테고리별 전리품 희귀도는 기본값으로 두는 편이 안전하다(GitHub #105).
- Common Sense 는 업데이트가 잦다. 서버를 다시 켜기 전에 워크숍 업데이트를 받는다.
- 문제가 생기면 먼저 4번(Stack ALL Fix)을 빼 본다. 지도 쪽이 이상하면 Hx_KR_Vanilla 만 빼고 Hx_KR_Mod 는 남긴다.

## 2026-10-18 추가: Skill Recovery Journal (모드팩 v2)

처음에는 "난이도를 크게 낮추는 모드 제외" 기준으로 뺐으나, 사용자 요청으로 넣었다.

- Skill Recovery Journal (2503622437, Mod ID `SkillRecoveryJournal`): Build 42 태그, 2026-09-04 갱신, 구독 약 281만.
  변경 기록에 'B42.20.3 hotfix2'(2026-08-18)와 비ASCII 파일명 저장 수정(2026-09-03, 한글 Steam 이름 관련).
  GitHub `Contents/mods/Skill Recovery Journal/common/media/lua/shared/Translate/KO` 에 KO 번역 5개 파일.
- 필수 모드(워크숍 Required items): errorMagnifier (2896041179, `errorMagnifier`),
  Mod Update and Alert System (3077900375, `ChuckleberryFinnAlertSystem`). 두 라이브러리는 서로를 필수로 지정한다.
- `npm run mods:verify` 결과 14개 모두 오류·경고 없음.

## 2026-10-18 추가: 화면·편의 모드 13개 (모드팩 v3)

사용자 요청: "무기 내구도 보이기, 갈증·배고픔·피로·무서움 같은 상태를 쉽게 보는 UI, 그 외 있으면 좋을 모드".

- 후보 찾기: 창작마당 검색(B42 태그, `durability`·`condition`·`moodle`·`status`·`bars` 등)과 B42 태그 전체·QOL 태그의
  구독 순 상위 목록에서, 42.20 정식(2026-07-29) 이후 갱신된 것만 골랐다. 설명문과 페이지의 최근 댓글(모드마다 6~10개)을 읽었다.
- 점검: `zomboid-mod-check` 스킬. 결과는 `compat.md` 의 "v3 추가 점검" 절.
- 넣은 13개(Workshop ID / Mod ID):

| 모드 | Workshop ID | Mod ID | 마지막 업데이트 | 한국어 | 고른 이유 |
|---|---|---|---|---|---|
| NeatUI Framework [B42] | 3508537032 | NeatUI_Framework | 2026-09-21 | 글자 없음 | Neat Crafting 의 필수 라이브러리 |
| Clean HotBar [B42] | 3461263912 | CleanHotBar | 2026-10-12 | 모드 KO | 무기 내구도. 핫바·손에 든 칸에 내구도·날카로움·탄약. 설명에 42.21.0 까지 명시 |
| CH Status HUD | 3776182375 | CHStatusHUD | 2026-10-15 | 모드 KO | 배고픔·갈증·피로·공포 등 32가지 수치 패널(`;` 키). 42.21 작동 댓글 여럿 |
| Moodle Quarters [B42] | 2854030563 | moodle_quarters | 2026-08-11 | 글자 없음 | 상태 아이콘 단계를 1/4 칸으로 보여 줌 |
| Neat Crafting [B42] | 3502080466 | Neat_Crafting | 2026-10-15 | 모드 KO | 제작 창 교체(검색·제작 사슬). 42.21.x 명시 |
| Better Generator Info | 3576056135 | BetterGeneratorInfo | 2026-09-16 | 모드 KO | 발전기 연료 남은 시간·전력 범위 |
| Combat Text (B40+B41+B42) | 2286124931 | CombatText | 2026-08-25 | Hx | 좀비 체력바·피해 숫자. 조건부(렉·멀티 미확인) |
| Swap It | 2366717227 | SwapIt | 2026-08-19 | Hx | 핫바 숫자키로 무기 맞바꿔 들기. 필요 라이브러리가 이미 팩에 있음 |
| Picking Meister | 3422220305 | P4PickingMeister | 2026-09-04 | Hx | 가방 속 물건 바로 꺼내기, 총 탄 한 번에 빼기 |
| [B42] Drag Bodies Faster | 3393821407 | DBFaster50 | 2026-08-02 | 글자 없음 | 시체 끌기 50% 빠르게(5가지 중 50% 판만) |
| Rain Cleans Blood [B42.20 + MP] | 2956146279 | RainCleansBlood | 2026-09-25 | Hx | 비·눈에 피·재가 씻김. 조건부(툴팁 수치 안 바뀜) |
| Map Symbol Size Slider | 2734705913 | MapSymbolSizeSlider | 2026-08-01 | 모드 KO | 지도 기호 크기 조절 |
| Military Grid Reference System … | 2928660831 | MGRS (FMCCYAYFGLE) | 2026-08-07 | Hx | 지도·미니맵 격자 좌표로 위치 부르기. 필요 라이브러리가 이미 팩에 있음 |

- 같은 일을 하는 모드 중 고른 기준과 뺀 후보는 위 "뺀 후보" 표에 더했다(Show Wall Health, Show Weapon Stats 는 점검 뒤 뺐다).
- `korean.status` 에 `no-text`(글자 없음)를 새로 만들었다. 아이콘·애니메이션·라이브러리처럼 번역할 글자가 없는 모드를 "영어만"으로 보이지 않게 하려고.
- 사이트: 분류 "환경"(Rain Cleans Blood)을 더했고, 참가자 가이드 마지막 장에 상태 수치(`;`)·무기 바꿔 들기·지도 좌표 팁을, 단축키 목록에 `;` 를 넣었다.
- `npm run mods:verify` 결과 27개 모두 오류·경고 없음.
