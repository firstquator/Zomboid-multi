# report.md 읽는 법

`mod_analyze.py` 는 정규식으로 찾는다. 아래 기준으로 실제 문제인지 가른다. 예시는 2026-10-18 점검(42.21.0, 14개)에서 나온 것이다.

## 파일 덮어쓰기

- 같은 상대 경로는 나중에 로드된 모드 파일이 쓰이고 앞 모드 파일은 무시된다.
- `media/lua/shared/translate/**` 와 `media/sandbox-options.txt` 는 모드마다 따로 읽으므로 경로가 같아도 무해하다
  (스크립트가 harmless 로 빼 둔다). 게임 로그의 `mod "X" overrides media/lua/shared/translate/...` 줄도 같은 이유로 무시한다.
- 그 밖의 경로(`.lua`, `media/scripts/*.txt`, `media/fonts/**`, 텍스처)가 겹치면 두 파일을 비교한다.
  - 예: `media/fonts/KO/fonts.txt` 를 WorldMap Name Symbols 와 Hx_KR_Vanilla 가 둘 다 넣는다. Hx 판이 상위집합이라 무해.
- 바닐라 `.lua` 를 같은 경로로 통째로 바꾸는 모드는 현재 빌드에서 그 파일이 바뀌었는지 반드시 비교한다(가장 위험한 방식).

## 같은 바닐라 함수를 여러 모드가 고침

- 둘 다 wrap(원래 함수를 잡아 두고 부름)이면 함께 동작한다.
  - 예: `ISInventoryPage:onBackpackRightMouseDown` ← Smarter Storage, Proximity Inventory 둘 다 wrap.
- 나중 쪽이 replace 면 앞 모드의 기능이 사라진다. 앞 쪽이 replace 면 뒤 wrap 이 그 교체본을 감싸므로 대개 괜찮다.
  - 예: `MainScreen:onEnterFromGame` ← Alert System(replace, 내용이 42.21 원본과 같음), errorMagnifier(wrap). 무해.
- wrap/replace 판정은 "같은 파일에 `= A.b` 로 원래 함수를 잡아 두는 줄이 있는가"로 한다. 다른 이름으로 잡거나 테이블에
  모아 두면 replace 로 잘못 나올 수 있다. 코드를 열어 원래 함수를 부르는지 본다.

## 통째로 교체(replace)

- `fn_diff.py` 로 현재 바닐라와 비교한다. SKILL.md 3단계 기준.
  - 예: Common Sense `ISCampingMenu.onAddAllFuel` → 공용 리스트를 지역 변수로 바꾼 버그 수정뿐. 무해.
  - 예: Hx_KR_Vanilla `ISBaseIcon:doContextMenu` → 한국어 어순만 다르고, 옛 "버리기" 코드는 `if self.onClickDiscard then`
    안이라 42.21 에서 실행되지 않음. 무해.
  - 예: Stack All `ISConsolidateDrainable.nextItem/runAgain/perform` → 42.21 과 함수 구성이 같고, 고치려는 바닐라 문제가
    42.21 에도 그대로 있음. 바닐라 "합치기"도 이 코드를 탄다는 점은 기록한다.
- 디버그·관리자 도구 함수(BrushTool, `createDebugContextMenu`)는 일반 플레이와 무관하다.

## 한 모드 안에서 같은 전역을 여러 파일이 정의

- 하위 폴더에 옛 파일이 남은 경우가 많다(게임은 `media/lua/<side>/` 아래 모든 `.lua` 를 경로 알파벳순으로 실행한다).
  - 예: Stack All 의 `client/New folder/` 에 옛 파일 4개. 최종 클래스는 알파벳순 마지막 파일 것이고, 우클릭 항목은
    먼저 등록된 옛 핸들러가 넣는다(나머지는 같은 이름이면 건너뜀).
- 확인할 것: 이벤트 핸들러가 여러 번 등록돼 메뉴가 중복되는지, 옛 파일의 위험한 패치(예: 행동 시간 0)가 실제로 켜지는지,
  패치 중복 방지 표시(`_xxxPatched`)가 있는지.

## 감싸려는 함수가 없음 / 없는 이벤트 / instanceof 클래스 없음

- 셋 다 현재 빌드에서 이름이 사라진 경우다. 조건문 안이 아니면 로드 때 또는 그 기능을 쓸 때 오류가 난다. 높은 위험.
- `SandboxVars.*` 처럼 실행 중에 채워지는 테이블은 스크립트가 뺀다.

## require 대상 파일 없음

- 다른 모드 지원용인 경우가 대부분이다. `getActivatedMods():contains("...")` 나 `if TetrisEvents then` 같은 조건 안이면 무해.
  - 예: Better Sorting 의 GameNight·New Music 지원, Has Been Read 의 Inventory Tetris 지원.

## 메서드 호출

- "jar 에도 Lua 에도 없음"만 본다. 조건(`if self.isPageLeft then`)이 있으면 무해. 없으면 그 줄이 실행될 때 오류.
- "jar 에는 있음"은 노출 클래스 목록 밖이라 확인만 못 한 것이다(지도 API `getSymbolsAPIv2` 등). 보통 무해.

## UTF-8 바이트를 가정한 문자열 코드 (한국어 그룹에 중요)

- Kahlua 문자열은 Java 문자열이다. `'한'` 은 `#s == 1`, `s:byte(1) == 0xD55C` 로 들어온다. 모드가 `s:byte` 로 UTF-8 바이트를
  풀거나 `string.char(0xE0+...)` 로 바이트를 다시 붙이면 한글이 다른 문자열로 바뀐다.
- 이 문자열이 저장 키나 비교에 쓰이면 데이터가 사라진다. 우리 호스트 방식은 Steam 닉네임(한글 가능)이 접속 이름이므로
  `getUsername()` 이 그런 코드로 들어가는지 따라가 본다.
  - 예: Skill Recovery Journal 의 장부 JSON 코덱. 장부 ID 에 접속 이름이 들어가서, 한글 닉네임이면 호스트가 다시 켠 뒤
    일지 기록을 못 찾는다(42.21 격리 서버에서 재현, 이슈 #154).
- 의심되면 아래 "실제 엔진에서 재현하기"로 확인한다.

## 실제 엔진에서 재현하기

커뮤니티 보고나 코드 의심을 Kahlua 에서 직접 확인하는 방법. 시험 모드를 만들어 `load_test.py --mode server` 로 돌리고
`<캐시>\run\server\server-console.txt` 에서 출력 줄을 grep 한다.

```
<임시>\content\9999999998\mods\XxxTest\42\mod.info        name=Xxx Test / id=XxxTest / require=\<대상 Mod ID>
<임시>\content\9999999998\mods\XxxTest\42\media\lua\shared\zz_XxxTest.lua   대상 모듈을 require 해서 함수를 부르고 print("[XXXTEST] ...")
<임시>\content\ 에 대상 모드와 그 require 모드 폴더(창작마당 번호 폴더째)를 복사
<임시>\empty-mods.json                                       {"mods": []}

python -I load_test.py --game $G --content <임시>\content --mods-json <임시>\empty-mods.json --add 9999999998 --mode server
```

- 처음 실행이면 서버 기준선부터 만든다(몇 분). `shared` 파일은 서버에서도 실행되므로 서버만 띄워도 된다.
- SRJ 코덱 시험 결과 예: `name=PlayerOne roundtrip=true`, `name=한글닉네임 roundtrip=false usernameSame=false`.
- 콘솔 로그에서 한글은 깨져 보이지만 판정 값(true/false, 길이)은 그대로 읽을 수 있다.

## 스크립트·샌드박스

- 아이템·레시피 정의가 다른 모드나 바닐라와 같은 `모듈.이름` 이면 나중 정의가 이긴다. 의도된 덮어쓰기인지 설명을 본다.
- 샌드박스 옵션 이름이 겹치면 한쪽 설정이 다른 쪽에 먹는다. 실제 문제다.

## 번역

- JSON 오류: 끝 쉼표만 있는 경우는 게임이 정식판에서 비엄격 모드로 읽어 받아 준다(`withStrictMode(Core.IS_DEV)`).
  그 밖의 문법 오류는 `Translator` 가 `RuntimeException("JSON Error in ...")` 을 던져 번역 로드가 깨질 수 있다. 실제 문제.
- KO 키를 나중 모드가 덮는 것은 정상(키 단위로 나중 값이 이김). 다만 Hx_KR_Mod 같은 통합 번역은 모드 업데이트보다
  늦을 수 있다. 작성자가 "번역 모드보다 뒤에 로드"라고 한 모드(Named skill VHS tapes)는 맨 뒤에 둔다.

## 로딩 테스트

- 기준선(바닐라)에 없는 ERROR/WARN 이 0 이면 불러오기 단계는 통과다.
- 서버만 오류: shared/server Lua, 아이템 스크립트, 샌드박스 옵션, 번역 JSON 쪽을 본다.
- 클라이언트만 오류: client Lua 를 본다.
- Lua 오류 줄에는 `Lua((MOD:<mod.info 의 name>)).<파일>.lua> Exception thrown` 처럼 모드 이름과 파일이 찍히고,
  그 아래 `attempted index: X of non-table: null` 같은 원인이 나온다(일부러 고장 낸 시험 모드로 확인함).
  `KahluaThread.flushErrorMessage` 줄들은 같은 오류의 스택 덤프라 따로 세지 않는다.
- 서버가 `couldn't find "...xml"` 로 멈추면 먼저 경로에 `~` 가 없는지 본다(테스트 환경 문제였던 적이 있다).
