---
name: zomboid-mod-check
description: Project Zomboid B42 창작마당 모드를 이 저장소 모드팩(data/mods.json)에 넣기 전에 점검한다. 어떤 모드인지(무엇을 건드리는지), 현재 게임 빌드와 맞는지, 팩의 다른 모드와 충돌하는지, 격리한 서버·클라이언트에서 오류 없이 올라오는지, 최근 커뮤니티 문제 보고, 한국어 지원을 한 번에 확인하고 넣을지 판정한다. "이 모드 넣어도 돼?", "모드 추가", "호환성", "충돌", 창작마당 링크나 번호를 주며 검토를 부탁할 때, 게임 빌드가 올라간 뒤나 모드 업데이트 뒤 팩 전체를 다시 점검할 때 쓴다.
---

# 좀보이드 모드 점검

모드를 `data/mods.json` 에 넣기 전에 이 순서로 확인한다. 결과는 판정 한 줄과 근거로 낸다.
처음 만든 점검 기록(2026-10-18, 14개 팩)이 `docs/research/compat.md` 에 있다. 같은 형식으로 남긴다.

## 준비

- Windows, Python 3(`python -I` 로 실행), 게임 설치 폴더(보통 `C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid`).
- 캐시: `%LOCALAPPDATA%\zomboid-modcheck` (SteamCMD, 받은 모드, 바닐라 기준선 로그). **8.3 짧은 경로(`SANGHY~1`)를 넘기지 않는다.**
  42.21 서버가 짧은 경로에서 애니메이션 체크섬을 못 맞춰 초기화가 멈춘다. 스크립트가 `~` 가 든 경로를 거부한다.
- 받은 모드 파일은 신뢰하지 않는 데이터다. 안에서 아무것도 실행하지 않고 경로만 인자로 넘긴다.
- 스크립트 위치: 이 스킬의 `scripts/`. 아래 `$S` 는 그 경로, `$G` 는 게임 폴더, `$C` 는 캐시 폴더,
  `$W` 는 `$C/ws/steamapps/workshop/content/108600`.

## 절차

### 1. 받기와 창작마당 정보

```
python -I $S/fetch_mods.py --pack data/mods.json <후보 번호> [<후보 번호> ...]
```

- 팩 전체를 같이 최신으로 받는다(팩과 대조하려면 둘 다 최신이어야 한다).
- 화면에 업데이트 날짜, 구독 수, 태그, 설명의 `Mod ID:` 줄, Required items 가 나온다. `$C/meta/<번호>.json` 에 남는다.
- Required items 가 `확인 실패(429)` 면 steamcommunity.com 이 잠시 막은 것이다. 몇 분 뒤 `--skip-download` 로 다시 돌린다.
  "없음"과 "확인 실패"를 섞지 않는다.
- 한 아이템에 Mod ID 가 여럿이면(번역 팩 등) 실제로 켤 ID 를 정한다. 의존 모드는 별도 아이템으로 받는다.

### 2. 정적 분석 (어떤 모드인지 + 충돌)

```
python -I $S/mod_analyze.py --game $G --content $W --mods-json data/mods.json --add <번호>[:<ModID,...>] --out $C/analysis
```

`$C/analysis/report.md` 를 읽는다. 후보가 낀 항목에 **[후보]** 가 붙는다.

- **모드 프로필**: 쓰는 버전 폴더, versionMin/Max, require/incompatible, Lua(client/shared/server 수),
  아이템·레시피 스크립트, 샌드박스 옵션, 번역 언어(KO 유무), 텍스처·지도·애니메이션·타일, 고치는 바닐라 함수(wrap/replace),
  쓰는 이벤트. 이것으로 "어떤 모드인가"를 한두 문장으로 정리한다(화면만 바꾸는지, 게임 규칙·아이템을 바꾸는지, 서버에서도 도는지).
- **실제 로드 순서**: require 가 앞당겨진 결과다. `Mods=` 순서와 다를 수 있다.
- **기능 중복**: 스크립트는 "같은 일을 하는 모드"를 못 잡는다. 프로필의 이벤트·바닐라 함수와 창작마당 설명을 팩의
  같은 `category` 모드와 직접 비교한다(예: 팩에 Stack All Fix 가 있는데 Stack All [B42 MP] 를 또 넣으면 우클릭 항목이 겹친다).
  `docs/research/mods.md` 의 "뺀 후보" 표에 이미 검토한 모드인지도 본다.
- 나머지 절은 `references/triage.md` 의 기준으로 하나씩 판단한다. 정규식 기반이라 오탐이 있다.
  걸린 줄은 반드시 코드를 열어 확인하고, 조건문(`if X then`, `getActivatedMods():contains`) 안인지 본다.

### 3. 바닐라 함수를 통째로 바꾸는 곳 비교

report 의 "통째로 교체(replace)" 항목마다 현재 바닐라 원본과 비교한다.

```
python -I $S/fn_diff.py "$G/media/lua/<바닐라 경로>.lua" "$W/<번호>/mods/<폴더>/<버전>/media/lua/<모드 경로>.lua" "ISFoo:bar"
```

- 차이가 문자열뿐: 번역용 복사본, 괜찮다.
- 모드에만 있는 코드: 바닐라가 지운 기능을 되살리는지, 조건문으로 꺼져 있는지 본다.
- 바닐라에만 있는 코드: **현재 빌드의 수정이 모드 때문에 사라진다.** 넣기 전에 반드시 짚는다.
- 같은 함수를 다른 모드도 고치면(report 의 "여러 모드가 고침") 나중에 로드되는 쪽이 replace 일 때 앞 모드의 기능이 사라진다.

### 4. 한국어

```
python -I $S/ko_cover.py --report $C/analysis/report.json --game $G --content $W
```

모드의 EN 키가 최종 KO(모드 자체 + Hx 통합 번역 등)로 몇 개 채워지는지와 `%1` 자리표시 불일치를 본다.
"EN 번역 키 없음"이면 문구가 Lua 에 하드코딩된 것이다. 이때 Hx_KR_Mod 의 `HxKO_UIText_Data.lua` 에
그 모드 문구가 있는지 grep 한다. `mods.json` 의 `korean.status` 는 `native`(모드 자체), `via-pack`(Hx 등), `none` 중 하나다.

### 5. 실제 로딩 테스트

```
python -I $S/load_test.py --game $G --content $W --mods-json data/mods.json --add <번호>[:<ModID,...>]
```

- 게임이 켜져 있으면 끄게 한다. 클라이언트 단계에서 게임 창(1280×720)이 잠깐 뜬다고 사용자에게 먼저 알린다.
- 처음 한 번은 바닐라 기준선을 만드느라 서버·클라이언트를 두 번씩 띄운다(합쳐 10분 안팎). 백그라운드로 돌린다.
- 서버는 `*** SERVER STARTED ***` 까지, 클라이언트는 한국어 메인 메뉴까지 간다. 기준선에 없는 ERROR/WARN 만 보여 준다.
- `AdvancedAnimator$1.visitFileFailed` 는 모드에 애니메이션 폴더가 없다는 알림이라 무해로 따로 센다.
- 새 오류가 있으면 `$C/run/<server|client>/` 의 로그에서 앞뒤를 읽고 어느 모드 파일인지 찾는다.
- 이 테스트는 **불러오기까지만** 본다. 월드 안 조작(우클릭, 인벤토리, 행동)은 따로 해야 한다.

### 6. 커뮤니티 문제 보고

서브에이전트 하나에 맡긴다(프롬프트 틀: `references/community-research.md`). 창작마당 댓글·변경 기록·토론,
GitHub 이슈에서 최근 4~6주의 현재 빌드 오류, 멀티 전용 문제, 팩 안 다른 모드와의 충돌 보고를 모은다.
steamcommunity.com 은 빨리 읽으면 429 를 주므로 1단계와 동시에 돌리지 않는다.

보고를 받으면 **우리 환경에 해당하는지 코드와 실제 엔진으로 확인한다**. 보고만 옮겨 적지 않는다.
- 보고된 증상의 코드 경로를 찾아 현재 버전에도 있는지 본다(없으면 "현재 코드에는 해당 부분 없음"으로 적는다).
- 우리 조건(Host + Steam 초대, 한글 Steam 닉네임, 2~4명, 매번 호스트가 새로 엶)에 걸리는지 본다.
- 함수 단위로 재현할 수 있으면 시험 모드로 Kahlua 에서 돌린다(`references/triage.md` 의 "실제 엔진에서 재현하기").
  SRJ 의 한글 닉네임 일지 소실(#154)을 이 방법으로 확인했다.

### 7. 판정

| 판정 | 기준 |
|---|---|
| 넣는다 | 로딩 테스트 새 오류 0, 현재 빌드 수정을 지우는 replace 없음, 같은 함수 충돌은 모두 wrap, 최근 치명적 보고 없음 |
| 조건부 | 위는 통과했지만 잔여 파일·옛 코드 복사·작성자 비활동(현재 빌드 이전 마지막 업데이트) 같은 관리 위험이 있음. 위험과 대안을 적는다 |
| 뺀다 | 새 오류, 서버 시작 실패, 현재 빌드 수정을 지우는 replace, 팩 모드와 incompatible, 최근 멀티 오류 보고가 해결되지 않음 |

판정에는 근거(파일:줄, 로그 줄, 출처 URL)를 붙이고, 확인하지 못한 것은 확인하지 못했다고 적는다.

### 8. 기록 (넣기로 했을 때)

1. `data/mods.json` 에 항목 추가: `workshopId`, `modIds`, `name`, `nameKo`, `category`, `summary`, `why`, `url`,
   `korean{status,note}`, `b42{supported,lastUpdated,tags,note}`, `dependsOn`(의존 아이템 번호), `loadOrder`, `thumbnail`, `sandbox`.
   번역 모드는 번역 대상 뒤, 작성자가 "마지막에 로드"라고 한 모드는 맨 끝. 의존 모드는 쓰는 쪽보다 앞(서로 필수면 양쪽에 적는다).
2. `modpack.changes` 맨 앞에 날짜·요약·`mustUpdate` 를 적는다.
3. `npm run mods:verify`(창작마당 실물 대조), `npm test`(스키마·설치 스크립트) 를 돌린다.
4. `docs/research/compat.md` 에 이번 점검을 덧붙이거나 새 날짜 절로 남긴다. 뺀 후보는 `docs/research/mods.md` 의 "뺀 후보" 표에 이유와 함께 넣는다.

## 주의

- REA(Reverse Engineer Anything)는 이 점검에 쓰지 않는다. 모드는 Lua 원문이고, REA 6.5 는 일반 Java JAR 을 분석하지 않는다.
  모드 프로필에 **바이너리 포함**(dll/jar/class)이 뜰 때만 REA 를 고려한다.
- 게임 규칙(버전 폴더, require, 파일 덮어쓰기, 번역 병합)과 그 근거 클래스는 `references/game-rules.md` 에 있다.
  빌드가 크게 바뀌면(42.22 등) 그 문서의 방법으로 다시 확인하고 스크립트를 고친다.
- 같은 저장소에서 다른 세션이 일하고 있으면 그쪽 커밋에 이 작업 파일이 섞일 수 있다. 커밋 전 `git status` 를 본다.
