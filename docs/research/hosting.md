# Project Zomboid B42 멀티 호스팅 조사

> 조사일 2026-10-18 · 대상 버전 **42.21.0 (stable)** · 용도: 웹사이트의 "슬라이드형 단계별 호스팅 가이드"와 "한 번에 설치" 기능의 근거 자료

## 근거 표기

| 표기 | 뜻 |
|---|---|
| `[공식-Sn]` | projectzomboid.com 블로그, The Indie Stone 포럼 패치노트 |
| `[위키-Wn]` | pzwiki.net (The Indie Stone 공식 위키, 자원봉사자가 관리) |
| `[코드]` | 실측 PC 에 설치된 42.21.0 (rev `4a0e9546ec`, Steam 기본 브랜치) 게임 파일을 직접 읽은 결과. Lua 는 원문, Java 는 `projectzomboid.jar` 바이트코드를 디스어셈블해서 확인했다. 파일/클래스 위치는 부록 D. |
| `[로그]` | 같은 PC 에서 2026-10-18 에 "서버 만들기"(Host)로 서버를 한 번 띄운 기록(`%USERPROFILE%\Zomboid\coop-console.txt`)과, 그때 게임이 자동으로 만든 백업 zip 안의 설정 파일 |
| `[커뮤니티-Cn]` | Steam 토론 |
| `[가이드-Gn]` | 호스팅 업체/팬 사이트 가이드 (2026-07 이후 것 위주) |
| `[외부-Vn/Mn]` | Valve, Microsoft 공식 문서 |

출처 URL 은 맨 아래 "출처" 절에 모았다. 확인하지 못한 것은 **미확인**으로 적었다.

---

## 결론 요약

### 1) 권장 호스팅 방식: 메인 메뉴의 "서버 만들기"(영문 Host)

- B42.21 에서 동작한다. 42.21 패치노트에 Host 관련 수정이 여러 개 있고 `[공식-S6]`, 실측 PC 에서 42.21.0 으로 Host 서버가 떠서 호스트가 접속까지 했다 `[로그]`.
- 친구는 **Steam 초대**로 들어온다. 이 경로는 IP 가 아니라 서버의 Steam ID 로 Steam P2P 연결을 한다 `[코드]`. Steam P2P 는 NAT 통과를 시도하고 안 되면 Steam 릴레이 서버로 우회한다 `[외부-V2]`. 그래서 B42 에서 포트포워딩 없이 Host 로 친구와 했다는 보고가 있다 `[커뮤니티-C1]`.
- 별도 프로그램, 배치 파일 수정, 콘솔 조작이 필요 없다. 설정 파일은 전용 서버와 같은 `%USERPROFILE%\Zomboid\Server\` 를 쓴다 `[코드]` `[위키-W2]`.
- 단점: 호스트가 게임을 나가면 서버가 꺼진다 (`Host user disconnected, stopping the server`) `[로그]`. 호스트 PC 에서 게임 프로세스와 서버 프로세스(별도 Java) 두 개가 돌아서 메모리를 더 쓴다 `[코드]`.
- 비개발자 친구 + 호스트도 함께 플레이 → **Host 권장**. 전용 서버(Steam 도구)는 24시간 서버가 필요할 때만.

### 2) "한 번에 설치" 흐름: 가능하다고 판단

**호스트**
1. PowerShell 한 줄(`irm <url> | iex`)이 `%USERPROFILE%\Zomboid\Server\` 에 4개 파일을 쓴다: `zomboid-multi.ini`, `zomboid-multi_SandboxVars.lua`, `zomboid-multi_spawnregions.lua`, `zomboid-multi_spawnpoints.lua`.
2. 게임 실행 → 메인 메뉴 **서버 만들기** → "서버 이름 :" 목록에서 `zomboid-multi` 선택 → "서버 메모리 설정 :" → **시작**.
3. 게임에 들어가면 ESC → **친구 초대** → 친구마다 **초대**.

- Host 화면의 "서버 이름" 목록은 열릴 때마다 `Zomboid\Server\` 폴더의 `*.ini` 를 읽어서 만든다. `.ini` 파일 하나만 있어도 목록에 뜬다 `[코드]`.
- ini 를 처음부터 우리가 만들어도 된다. 서버는 시작할 때 ini 를 읽어 **아는 키만** 반영하고, 곧바로 모든 키를 기본값과 합쳐 **파일을 다시 쓴다** `[코드]`. 빠진 키는 기본값으로 채워지고, 모르는 키는 버려진다. SandboxVars 도 같다: 빠진 항목은 기본값으로 두고, 시작할 때 전체를 다시 쓴다 `[코드]`.

**참가자**
- Steam 컬렉션을 구독할 필요가 없다. 접속하면 "서버에 적용된 창작마당 아이템" 화면이 뜨고, **설치**를 누르면 게임이 그 아이템들을 Steam 에서 자동으로 구독하고 받는다 `[코드]` `[위키-W2]` `[가이드-G3]`.
- `steam://` 링크는 보조 수단이다. Host 서버는 호스트가 초대(허용)한 Steam 계정만 받아 주기 때문에 링크만으로는 못 들어온다 `[코드]`. 참가자 쪽 "원클릭"은 Steam 초대 수락이 가장 확실하다.

### 3) 위험 요소

1. **초대 안 하면 못 들어온다.** Host 서버는 호스트 본인과 초대 목록에 있는 Steam ID 만 연결을 받는다 `[코드]`. 초대 목록은 서버 프로세스 메모리에 있어서 서버를 다시 켜면 비어 있고, 호스트가 "친구 초대" 창을 열 때 저장된 목록(`invited.ini`)을 다시 보낸다 `[코드]`. → 가이드에 "매번 ESC → 친구 초대" 단계를 넣는다.
2. **참가자는 메인 메뉴에서 초대를 받아야 한다.** 플레이 중이면 "게임 플레이 중에는 초대를 받을 수 없습니다.", 메인 메뉴가 아닌 화면이면 "초대를 받기 전 메인 메뉴로 돌아가세요." `[코드]`.
3. **버전이 같아야 한다.** 모두 42.21 (Steam 기본 브랜치). `legacy41`, `42.19`, `unstable` 베타를 고른 사람이 있으면 안 맞는다 `[공식-S3]`. 접속 시 "클라이언트 버전(%1)와 서버(%2)버전이 일치하지 않습니다." `[코드]`.
4. **모드 버전 불일치**: "창작마당 아이템의 버전이 서버와 다릅니다." → 호스트는 서버를 다시 켜고, 참가자는 Steam 을 재시작한다 (게임 안내 문구 그대로) `[코드]`.
5. **SandboxVars.lua 문법 오류 = 서버 즉시 종료.** 파일이 있는데 읽기에 실패하면 서버가 `System.exit` 한다 `[코드]`. 설치 스크립트가 쓰는 Lua 는 미리 검증해야 한다.
6. **인코딩**: Windows PowerShell 5.1 의 `-Encoding UTF8` 은 BOM 을 붙인다 `[외부-M2]`. 게임의 ini 파서는 줄 앞뒤 공백만 지우고 BOM 은 지우지 않는다 `[코드]`. 첫 줄이 키라면 그 키가 무시된다. → **BOM 없는 UTF-8 + 첫 줄은 `#` 주석**.
7. **게임이 켜져 있을 때 파일을 쓰면 덮어써질 수 있다.** 서버는 시작할 때 파일을 다시 쓰고 `[코드]`, Host 의 "서버 설정" 화면에서 저장해도 다시 쓴다. → 스크립트는 게임을 끈 상태에서 실행.
8. **`irm | iex` 신뢰 문제.** 실행 정책은 붙여넣은 명령을 막지 않는다 `[외부-M1]`. 친구에게 "모르는 스크립트를 실행하라"는 형태라 스크립트 원문 공개와 수동 설치 대안이 필요하다. 백신/SmartScreen 반응은 **미확인**.
9. **메모리**: Host 서버는 고른 메모리를 시작할 때 통째로 잡는다(`-Xms` = `-Xmx`) `[코드]`. 게임 자체도 기본 3GB 를 쓴다 `[코드]` `[위키-W4]`.
10. **모드 호환성**: B41 전용 모드는 받아지기는 하지만 B42 에서 로드되지 않거나 접속 문제를 만든다 `[가이드-G1]`. (모드 선정은 `docs/research/mods.md` 담당)

---

## 1. 현재 stable 빌드 (2026-10 기준)

- **42.21** 이 2026-09-28 에 Stable 로 나왔다. "We released 42.21 into our Unstable beta last Wednesday … the 'Go' button is being pressed… today." `[공식-S1]`
- 공식 사이트 상단 표시: `Stable Build: 42.21 | Unstable Build: 42.21` `[공식-S5]`
- pzwiki: "The current stable version is 42.21.0" `[위키-W2]`
- 실측 PC: `%USERPROFILE%\Zomboid\version.txt` = `42.21.0 4a0e9546ec`, Steam 앱 매니페스트에 베타 키 없음(= 기본 브랜치) `[로그]`
- 지나온 길: 42.20 이 2026-07-29 Stable (멀티 포함) `[공식-S3]` → 42.20.4 보안 핫픽스(`loadstring`/`loadstream` 비활성) → 42.21 Unstable 2026-09-23 `[공식-S2]` → 42.21 Stable 2026-09-28 `[공식-S1]`. 그 뒤 핫픽스 공지는 2026-10-18 현재 없다 `[공식-S5]`.
- B41 을 계속하려면 Steam 베타 `legacy41`, 42.19 세이브를 계속하려면 베타 `42.19` `[공식-S3]` `[공식-S4]`.
- 42.21 에 들어간 멀티 관련 수정 중 이 문서와 관계있는 것 `[공식-S6]`:
  - "Added a notification for players who try to connect to an MP server with different game version"
  - "Fixed missing ShowCoords setting in Host"
  - "Fixed an issue where clicking Start more than once while creating or launching a hosted world would result in multiple instances of the server console opening"
  - "Fixed being unable to launch closed hosted server by ensuring that the default role for host connection is set to admin"
  - "Fixed not being able to connect to a dedicated/host server if the server option UsernameDisguises is enabled"
  - "Fixed an issue which would block clients from loading into server"

## 2. 호스팅 방식 비교

| | (a) 메인 메뉴 "서버 만들기"(Host) | (b) Steam 도구 "Project Zomboid Dedicated Server" |
|---|---|---|
| B42 동작 | 된다. 42.21 패치노트에 Host 수정 `[공식-S6]`, 42.21.0 실측 `[로그]` | 된다. 앱 ID 380870, 기본 브랜치가 B42 `[위키-W2]` `[가이드-G4]` |
| 설치 | 게임만 있으면 됨 | Steam 라이브러리 → 도구에서 따로 설치. "Do not launch the server via Steam" — Steam 의 플레이 버튼이 아니라 `StartServer64.bat` 로 실행해야 함 `[위키-W2]` |
| 시작 | 메뉴 클릭 | 배치 파일 실행, 첫 실행 때 콘솔에서 관리자 비밀번호 입력 `[위키-W2]` |
| 메모리 설정 | Host 화면 드롭다운 (0.75~16GB) `[코드]` | `StartServer64.bat` 의 `-Xms`/`-Xmx` 를 직접 고쳐야 함 `[위키-W2]` |
| 친구 접속 | Steam 초대 (Steam P2P, 포트포워딩 불필요 보고) `[코드]` `[외부-V2]` `[커뮤니티-C1]` | IP 직접 입력. 인터넷 친구는 UDP 16261/16262 포트포워딩 필요 `[위키-W2]` `[위키-W4]` |
| 호스트도 플레이 | 자연스럽게 됨 (서버가 뜨면 호스트 게임이 자동으로 첫 접속, `isCoopHost=true`) `[로그]`. 관리자 권한이 필요하면 채팅에 `/grantadmin "이름"` `[위키-W4]` | 같은 PC 에서 게임을 따로 켜고 자기 서버에 IP 로 접속 (공인 IP 또는 로컬 IP) `[위키-W2]` |
| 서버 수명 | 호스트가 나가면 꺼짐 `[로그]` | 호스트가 게임을 꺼도 계속 돎 |
| 비밀번호 | `Password=` 무시됨 ("Ignored when hosting a server via the Host button") `[위키-W3]`, 42.21 생성 ini 주석도 같음 `[로그]` | `Password=` 적용 |
| 한글 닉네임 | Steam 닉네임으로 로그인하고, Host+Steam 경로는 `AllowNonAsciiUsername` 검사를 거치지 않음 `[코드]` | 기본값 `AllowNonAsciiUsername=false` 라서 한글 사용자명은 `NonAsciiCharacters` 로 거부됨 `[코드]` |
| 알려진 문제 | "initializing" / "Downloaded x of y" 에서 멈춤 → 재시작 반복 `[위키-W4]` | Steam 도구판이 "Getting server info" 에서 멈추거나 모드를 못 받음 → SteamCMD 로 설치하라고 안내 `[위키-W4]` |

**결론: 비개발자 친구에게는 (a) Host 를 권한다.** (b) 는 포트포워딩, 배치 파일 편집, 콘솔 조작, 같은 PC 에 게임과 서버를 따로 띄우는 과정이 모두 필요하다.

참고 (B41/B42 차이): B41 Host 에 포트포워딩이 필요했는지는 사용자마다 경험이 갈린다. 같은 스레드에서 "B41 때는 포트포워딩해야 했다(맵 청크가 안 불러와짐)"는 사람과 "B40~B42 내내 포트 안 열고 Host 했다"는 사람이 맞선다. B42 에서는 질문자가 `db` 폴더를 지운 뒤 포트포워딩 없이 됐다고 적었다 `[커뮤니티-C1]`.

## 3. 설정 파일

### 위치
- `%USERPROFILE%\Zomboid\Server\` `[위키-W3]` `[위키-W2]`. 코드상으로는 `<캐시 폴더>\Server` 이고, 캐시 폴더 기본값이 `%USERPROFILE%\Zomboid` 다 `[코드]`. 게임 실행 옵션 `-cachedir=` 을 쓰면 위치가 바뀐다 `[위키-W4]`.
- Host 화면의 "서버 설정"을 누르면 나오는 관리 화면에 이 경로가 "설정 저장 경로: %1" 로 표시된다 `[코드]`.

### 파일 이름 규칙 (서버 이름이 `zomboid-multi` 일 때)

| 파일 | 내용 | 없으면 |
|---|---|---|
| `zomboid-multi.ini` | 서버 옵션(PVP, 포트, 모드 목록 등) | 서버가 기본값으로 만든다 `[코드]` |
| `zomboid-multi_SandboxVars.lua` | 게임 규칙(좀비, 전리품, 미니맵 등) | 서버가 기본값으로 만든다 (`writing ...\servertest_SandboxVars.lua`) `[로그]` `[코드]` |
| `zomboid-multi_spawnregions.lua` | 스폰 지역 목록 | 서버가 만든다. 단 서버 내장 템플릿은 4개 도시(Muldraugh, West Point, Rosewood, Riverside)뿐 `[코드]` |
| `zomboid-multi_spawnpoints.lua` | 직업별 스폰 좌표 | 서버가 만든다 `[코드]` |

- 접미사 목록은 게임 코드에 `_SandboxVars.lua`, `_spawnpoints.lua`, `_spawnregions.lua`, (옛) `_zombies.ini` 로 들어 있다 `[코드]`.
- 세계 저장은 `Zomboid\Saves\Multiplayer\zomboid-multi\` `[위키-W2]`, 호스트 쪽 캐시는 `...\zomboid-multi_player\` `[코드]` `[로그]`. 서버 계정 DB 는 `Zomboid\db\zomboid-multi.db` (실측 PC 에 `db\servertest.db` 존재) `[로그]`.

### Host 메뉴가 이 폴더를 읽는가 → 예
- Host 화면이 열릴 때마다 `readAllSettings()` 로 폴더를 다시 읽어 "서버 이름 :" 목록을 채운다 `[코드]`.
- 목록에 넣는 조건: 폴더가 아닌 파일, 이름이 `.ini` 로 끝나고 `_zombies.ini` 로 끝나지 않음, `.ini` 를 뺀 이름에 `/ \ : ; " .` 가 없고 `_zombies` 를 포함하지 않음 `[코드]`. → `zomboid-multi` 는 통과. **백업 파일 이름이 `.ini` 로 끝나면 목록에 같이 뜬다** (예: `zomboid-multi.ini.bak` 은 안 뜸, `zomboid-multi-old.ini` 는 뜸).
- 고른 이름의 파일이 하나라도 있으면 "새 설정"이 아니므로 시작할 때 기본값으로 덮지 않고 기존 파일을 쓴다. 파일이 하나도 없는 이름일 때만 기본값을 새로 만든다 `[코드]`.
- 42.21 의 "새 설정 만들기"는 기본값만 쓴다. 메인 메뉴에서 켜 둔 모드를 서버 설정에 자동으로 넣는 코드가 꺼져 있다 (`if true then return end`) `[코드]`.

### 파일만 미리 넣어 두면 Host 화면에서 바로 고를 수 있는가 → 예
- `.ini` 만 있어도 목록에 뜬다 `[코드]`. 나머지 3개는 없으면 서버가 만들지만, 미니맵을 켜려면 SandboxVars 를, 11개 도시 스폰 목록을 쓰려면 spawnregions 를 우리가 써야 한다 (부록 B).
- 실측 PC 의 Host 화면 기억 값은 `Zomboid\Lua\host.ini` 에 `servername=`, `username=`, `memory=` 세 줄로 저장된다 `[코드]` `[로그]`. 이 파일의 `servername=zomboid-multi` 로 드롭다운 기본 선택을 바꿀 수 있다 (선택 사항).

## 4. B42 모드 줄 형식

### 확인된 사실
- `WorkshopItems=` : Steam 창작마당 숫자 ID, `;` 로 구분. 게임이 만든 ini 의 주석 원문: `WorkshopItems=514427485;513111049` `[로그]` `[위키-W3]`. 서버는 `;` 로 나눈 뒤 공백을 지우고, 올바른 Steam ID 형식(숫자)인 것만 받는다 `[코드]`.
- `Mods=` : 모드 ID(창작마당 제목도, 폴더 이름도 아님). 각 모드의 `mod.info` 안 `id=` 값 `[가이드-G1]` `[코드]`. `;` 로 구분, 적은 순서가 로드 순서이며 의존 모드를 앞에 둔다 `[가이드-G1]`. 창작마당 아이템 하나에 모드가 여러 개 들어 있으면 `Mods=` 에 여러 개, `WorkshopItems=` 에는 한 개 `[가이드-G1]`.
- **`\` 접두**: 42.21 서버는 `Mods=` 값에서 **`\` 를 전부 지운 다음** `;` 로 나누어 읽는다 (`GameServer.main`: `mods.replace("\\", "").split(";")`) `[코드]`. 그래서 42.21 에서는 아래 두 줄이 같은 결과다.
  ```ini
  Mods=\ModA;\ModB
  Mods=ModA;ModB
  ```
- 42.21 의 Host "서버 설정" 화면이 모드를 추가할 때 쓰는 값은 `\` 없는 ID 다 (`modInfo:getId()` = `mod.info` 의 `id=` 값 그대로) `[코드]`. 반대로 `\ModA` 처럼 적어 두면 그 화면의 모드 목록에서 이름 대신 "알 수 없는 모드"로 보인다 (표시만 그렇고 서버 로드는 됨) `[코드]`.
- 게임은 `mod.info` 의 `require=`, `incompatible=` 줄과 `mods\default.txt` 의 `mod = ...` 줄에서도 `\` 를 지우고 읽는다 `[코드]`. B42 에서 모드 참조에 `\` 를 붙이는 형식이 쓰였다는 뜻이다.

### 커뮤니티 자료 (서로 엇갈림, 원문 그대로)
- 42.13 (2025-12) 전용 서버: "The format of the Mods configuration in the .ini file should be: `Mods=\Mod1Id;\Mod2d;\...`" `[커뮤니티-C3]`
- low.ms (2026-08-03, 42.20 시기): `WorkshopItems=2544353492;3674013419` / `Mods=\P4HasBeenRead;\JeevesClaims`, "A Build 41 Mods= line has no backslashes at all … Hand one across to a Build 42 server and it loads nothing, silently." `[가이드-G1]`
- Pine Hosting (2026-08-13): `Mods=ExampleMod;AnotherMod;ThirdMod`, "Current Build 42 versions no longer require the leading backslash that was used during some earlier Build 42 multiplayer versions." `[가이드-G2]`
- 42.20 에서 `\` 없는 줄이 정말 실패했는지는 **미확인**. 42.21 은 코드상 둘 다 된다.

### 권장
- 42.21 기준으로는 둘 다 된다. 이전 B42 버전과도 맞추려면 **`\` 접두**(`Mods=\ModA;\ModB`)를 권한다. 대가는 Host "서버 설정 → 모드" 화면에서 "알 수 없는 모드"로 보이는 것뿐이다. 게임 UI 와 똑같이 보이게 하고 싶으면 접두 없이 쓴다. 어느 쪽이든 42.21 서버 로드 결과는 같다.
- B41 형식은 `\` 없음 `[가이드-G1]`.

### `Map=` 줄
- 기본값 `Map=Muldraugh, KY` `[로그]` `[위키-W3]`. 키를 빼면 서버가 이 기본값으로 채운다 `[코드]`. **맵 모드가 없으면 건드릴 필요 없다.**
- 맵 모드가 있으면 그 맵 폴더 이름을 앞에, `Muldraugh, KY` 를 **맨 뒤**에 둔다. 위키 원문 예: `Map=vehicle_interior;Basements;Ashenwood;alshardware;AZSpawn;Muldraugh, KY` `[위키-W4]`

## 5. 모드 받기

### 호스트(Host 서버)
- Host 서버는 시작할 때 `WorkshopItems=` 목록을 보고 **스스로** 받는다. 시작 화면에 "창착마당 아이템 받는 중"(게임 번역 원문 그대로), "다운로드 중 %1 / %2" 가 표시된다 `[코드]`. 오래된 아이템이면 지우고 다시 받는 경로("재설치 중 %1 / %2")도 있다 `[코드]`.
- Host 서버가 받은 모드는 게임 설치 폴더 안 `steamapps\workshop\content\108600\` 에 따로 쌓이는 것으로 보인다 (실측 PC 의 `...\ProjectZomboid\steamapps\workshop\content\108600\` 에 아이템 폴더들이 있음) `[로그]`. B41 시절에도 Host 용 사본이 게임 폴더에 따로 있어서 버전 불일치 때 양쪽을 지웠다는 증언이 있다 `[커뮤니티-C4]`. 이 폴더가 정확히 언제 쓰이는지는 **부분 확인**.
- 호스트가 미리 구독해야 하는가: 코드상 필요 없다. 서버가 직접 받고, 호스트 본인의 게임도 접속할 때 참가자와 같은 자동 구독 과정을 거친다 `[코드]`. 단, Host 의 "서버 설정" 화면에서 모드를 **고르려면** 설치된 모드만 목록에 보이므로 먼저 구독해야 한다 `[위키-W4]` ("Try enabling the mods in the 'Mods' panel on the main menu first"). 파일로 미리 써 넣는 흐름이면 이 화면을 쓸 일이 없다.

### 참가자
- 구독 필요 없다. 접속 과정에서 서버의 창작마당 목록을 받아 "서버에 적용된 창작마당 아이템" 화면에 항목별 상태(미구독 / 설치 완료 / 업데이트 필요 / 다운로드 중)를 보여 주고, **설치**를 누르면 구독 안 된 아이템은 `SubscribeItem`, 오래된 아이템은 `DownloadItem` 을 호출한다 `[코드]`.
- 위키: "Added Steam Workshop-subscribed mods to the server will be downloaded automatically on connecting client machines" `[위키-W2]`. 가이드: "You will be prompted to accept the server's Workshop mod list on first join if it uses mods — accept to auto-subscribe." `[가이드-G3]`
- 부작용: 실제 Steam 구독이 추가된다. 나중에 정리하려면 직접 구독을 해지해야 한다 `[코드]` (SubscribeItem 호출).
- 서버 `Mods=` 에 있는데 창작마당 아이템이 아닌(로컬) 모드는 참가자에게 받아지지 않고 `"%1" 모드가 설치되지 않았습니다.` 로 막힌다 `[코드]`.

### 버전 불일치 오류
- 게임 문구 원문 `[코드]`:
  - EN `Workshop item version is different than the server's` / KO `창작마당 아이템의 버전이 서버와 다릅니다.`
  - 상세 EN `Possibly the server's version is outdated, requiring the server to be restarted.<br>If your version is outdated, try restarting Steam to get the latest version.`
  - 상세 KO `서버의 버전이 오래되었을 가능성이 있습니다, 서버를 재기동할 필요가 있습니다.<br>만약 당신의 버전이 오래된 경우는 스팀을 재시작해 최신 버전을 받아 보세요.`
- 원인: 참가자 PC 에 설치된 아이템 시각이 서버가 알려 준 갱신 시각과 다르면 이 오류가 난다 `[코드]`. 모드 제작자가 업데이트하면 Steam 은 참가자 쪽부터 받고, 서버는 다시 켤 때까지 옛 버전을 쓰는 경우가 많다 `[가이드-G5]`.
- 해결 순서 (순한 것부터):
  1. 호스트가 게임을 완전히 나갔다가 Host 로 다시 시작 (서버가 새 버전을 받음) `[코드 문구]` `[가이드-G5]`
  2. 참가자는 Steam 을 완전히 종료 후 재실행, Steam 다운로드가 끝난 뒤 접속 `[코드 문구]` `[가이드-G5]`
  3. 그래도 안 되면 해당 모드 구독 해지 → 재구독 `[가이드-G5]`
  4. 최후: 창작마당 폴더와 `appworkshop_108600.acf` 삭제 (B41 시절 커뮤니티 방법, 파괴적) `[커뮤니티-C4]`

## 6. 네트워크

### 포트 (B42.21)
- 서버 로그 원문 `[로그]`:
  ```
  Server is listening on port 16261 (for Steam connection) and port 16262 (for UDPRakNet connection)
  Clients should use 16261 port for connections
  ```
- ini 기본값 `DefaultPort=16261`, `UDPPort=16262` `[로그]` `[위키-W3]`. 위키의 전용 서버 포트포워딩 목록도 `16261 UDP`, `16262 UDP - Direct Connection Port` `[위키-W2]`. `RCONPort=27015` 는 기본값만 있다 `[로그]`.
- 일부 오래된 가이드에 나오는 다른 포트들은 42.21 로그에 나오지 않는다 `[로그]`.

### UPnP
- 기본 `UPnP=true`. 서버가 시작할 때 라우터에 자동 포트 개방을 시도한다 `[위키-W3]`. 실측 로그 `[로그]`:
  ```
  Router detection/configuration starting.
  If the server hangs here, set UPnP=false.
  No UPnP-enabled Internet gateway found, you must configure port forwarding on your gateway manually in order to make your server accessible from the Internet.
  ```
  UPnP 가 실패해도 서버는 계속 뜬다 `[로그]`.

### 포트포워딩 없이 Steam 초대로 되는가 → 된다 (근거 3가지)
1. 초대받은 참가자는 IP 가 아니라 **서버 Steam ID** 로 접속한다. 초대 연결 문자열에 IP 대신 Steam ID 가 들어간다는 주석이 코드에 있다: "When the coop host sends an invite, the +connect string contains the server's Steam ID instead of an IP address." `[코드]`
2. 네트워크 모듈(`ZNetJNI64.dll`)이 Steam P2P 세션 콜백(`P2PSessionRequest_t`, `P2PSessionConnectFail_t`)과 `SteamNetworking006` 을 쓴다 `[코드]`. Steamworks 문서: P2P 패킷 전송은 "automatically establishes NAT-traversing or Steam relay server connections", 릴레이는 "allowed by default" `[외부-V2]`.
3. 사용자 보고: B42 Host 를 포트포워딩 없이 했다 `[커뮤니티-C1]`. B41 에서도 "host, allow specific Steam friends and invite them. No need for dedicated servers or port-forwarding." `[커뮤니티-C2]`. 위키도 "Port 16262 closed" 경고는 "For small co-op servers, this warning can often be ignored if players are still able to connect" 라고 쓴다 `[위키-W4]`.

### Host 서버의 출입 통제 (중요)
- Host 모드에서 Steam 연결 요청이 오면 "호스트 본인이거나 초대 목록에 있으면" 받고 아니면 거절한다 `[코드]`.
- 호스트가 ESC → **친구 초대** 창에서 **초대**를 누르면 그 친구가 초대 목록에 추가되고 Steam 초대가 날아간다 `[코드]`. 같은 창의 친구별 **거절/수락** 버튼은 초대 메시지 없이 목록에만 넣고 빼는 스위치다 `[코드]`.
- "친구 초대" 메뉴는 Host 서버를 띄운 사람과 Host 서버에 들어온 사람에게 보인다 `[코드]`. 하지만 서버 허용 목록에 추가하는 동작은 **호스트 PC 에서만** 일어난다(Host 서버 프로세스가 돌고 있을 때만 `invite-add` 전송) `[코드]`. 참가자가 다른 친구를 초대하면 Steam 초대는 가지만, 호스트가 허용하지 않은 그 친구는 접속이 거부된다고 본다 (코드 근거 추론).

### Windows 방화벽
- Host 서버는 게임 폴더의 `jre64\bin\java.exe` 로 따로 실행된다 `[코드]`. 이 파일의 설명은 `Zulu Platform x64 Architecture` (Azul Zulu 25) 다 `[로그]`.
- 실측 PC 에는 이 이름의 인바운드 허용 규칙 4개(개인/공용 × TCP/UDP)와 `Project Zomboid` 규칙 2개가 있었다 `[로그]`. 개인/공용 × TCP/UDP 4개 묶음은 Windows 방화벽 팝업에서 허용을 눌렀을 때 생기는 모양이다. 그래서 처음 서버를 열 때 이 이름으로 팝업이 뜰 가능성이 높다. **팝업 화면 자체는 이번에 재현하지 않았다 (부분 확인)**.
- 위키: "Windows users may also need to open the necessary ports on their firewall." `[위키-W4]`
- 가이드 문구: 팝업이 뜨면 **액세스 허용**.

### 친구가 들어오는 방법
| 방법 | 동작 | 조건 |
|---|---|---|
| Steam 초대 (권장) | 호스트: ESC → 친구 초대 → 친구 선택 → 초대. 참가자: Steam 알림에서 수락 | 참가자가 메인 메뉴에 있어야 함, 포트포워딩 불필요 `[코드]` `[위키-W4]` |
| Steam 친구 목록 "게임 참가" | 게임에 들어간 사람은 Steam 리치 프레즌스에 `+connect <주소>` 를 등록한다. 친구가 이걸 누르면 접속 시도 `[코드]` | 호스트가 그 친구를 미리 수락/초대해 둬야 함 `[코드]` |
| IP 직접 입력 | 여러 명이서 하기 → 즐겨찾기에 공인 IP와 포트 16261 추가 `[위키-W2]`. Host 서버면 게임이 서버 정보를 조회해서 Steam ID 연결로 바꾼다 `[코드]` | 호스트 라우터에 UDP 16261/16262 포트포워딩 `[위키-W4]` + 초대 목록 등록 `[코드]` |

## 7. 샌드박스

### 미니맵 키 (B42.21 확인)
- 정확한 키: **`SandboxVars.Map.AllowMiniMap`**, 기본 `false` `[로그]` `[위키-W3]`. 42.21 이 만든 파일 원문 `[로그]`:
  ```lua
      Map = {
          -- 미니 맵을 사용할 수 있습니다.
          AllowMiniMap = false,
          -- 세계 맵을 사용할 수 있습니다.
          AllowWorldMap = true,
          -- 게임 시작 시 세계 맵 전체가 공개됩니다.
          MapAllKnown = false,
          -- 광원 없이는 지도를 읽을 수 없습니다.
          MapNeedsLight = true,
      },
  ```
- 미니맵은 `AllowWorldMap` 이 켜져 있고 `AllowMiniMap == true` 일 때만 허용된다 `[코드]`. 게임 안에서는 화면 왼쪽 아이콘 줄의 지도 아이콘을 누르면 나오는 선택 창에서 세계 지도/미니맵을 고른다 `[코드]`. 단축키는 **미확인**.

### 호스트가 알아야 할 기본값 (42.21 생성 파일 기준) `[로그]`
- ini: `PVP=true` (단 `SafetySystem=true` 라서 각자 PvP 를 켠 사람끼리만 공격 가능 `[위키-W3]`), `PauseEmpty=true` (아무도 없으면 시간 정지), `MaxPlayers=32` (1~254), `Public=false`, `Open=true`, `SaveWorldEveryMinutes=0` (클라이언트가 떠날 때만 저장), `BackupsOnStart=true`, `BackupsCount=5`, `AllowNonAsciiUsername=false` (Host+Steam 경로엔 적용 안 됨 `[코드]`).
- SandboxVars: `VERSION = 6`, `Zombies = 4` (보통), `ZombieRespawn = 4` (없음), `DayLength = 4` (1시간 30분), `StartMonth = 7`, `StartDay = 9`, `StartTime = 2` (오전 9시), `WaterShut = 2` / `ElecShut = 2` (단수·단전 0~30일 / 14~30일), `Map.AllowMiniMap = false`.
- 친구끼리 협동이면 `PVP=false` 를 고려할 만하다 (판단, 사실 아님).

## 8. 언어

- 설정 위치: 메인 메뉴 **설정** → **사용자 인터페이스 (UI)** 탭 → **언어 선택** `[코드]`. 바꾸면 게임이 Lua 를 다시 불러 바로 적용한다(재시작 불필요) `[코드]`.
- 처음 실행 때는 Windows 언어를 따른다. 게임은 `options.ini` 에 언어가 없으면 Java `user.language`(Windows 로캘)로 고르고, 그것도 없으면 영어를 쓴다 `[코드]`. 한국어 Windows 면 처음부터 한국어로 뜬다 (추론, 코드 근거).
- Steam 상점 지원 언어에 Korean 포함 `[외부-V3]`. 게임에 한국어 전용 글꼴(`media\fonts\KO`, `Config_Korean.bmfc`)과 번역(`media\lua\shared\Translate\KO\*.json`)이 들어 있다 `[코드]`.
- **B42 한국어 글꼴 깨짐**: 공식 출시 공지의 글꼴 문제 목록에는 "Chinese (Simplified), Chinese (Traditional), and Catalan" 만 있고 한국어는 없다 `[공식-S3]` `[공식-S4]`. 실측 PC 는 `options.ini` 가 `language=KO` 이고, 게임이 만든 서버 ini 주석이 한국어로 정상 출력됐다 `[로그]`. 한국어 웹 검색에서는 B42 한국어 깨짐 보고를 찾지 못했다. → **알려진 이슈 없음 (단, 화면 렌더링은 눈으로 확인하지 않음)**. 모드 안 문구가 영어로 나오는 것은 별개 문제다.
- 한국어 메뉴 이름 (42.21 KO 번역 원문) `[코드]`:

| 영문 | 한국어 |
|---|---|
| Multiplayer (Join) | 여러 명이서 하기 |
| Host | 서버 만들기 |
| Host 화면 제목 | 서버 열기 |
| Server name / Edit settings / Server memory | 서버 이름 : / 서버 설정 / 서버 메모리 설정 : |
| Start / Abort | 시작 / 중단 |
| Invite Friends (ESC 메뉴) | 친구 초대 |
| Invite / Allow / Deny | 초대 / 수락 / 거절 |
| Server Workshop Items 화면 | 서버에 적용된 창작마당 아이템 / 설치 / 끊기 |
| Use Steam Relay (IP 접속 창) | 스팀 릴레이 사용 |
| Options / User Interface / Language | 설정 / 사용자 인터페이스 (UI) / 언어 선택 |

## 9. 흔한 실패와 해결

### 접속이 안 됨
1. 호스트가 친구 초대 창에서 초대/수락을 안 했다 → ESC → 친구 초대 → 초대 `[코드]`
2. 참가자가 게임 플레이 중이거나 메인 메뉴가 아닌 화면에 있다 → 메인 메뉴로 나와서 다시 초대 받기 `[코드]`
3. 게임 버전이 다르다 → Steam 속성의 베타를 "없음"(기본)으로 `[공식-S3]` `[코드]`
4. 모드 버전 불일치 → 5절 순서대로
5. IP 로 접속하는 경우: 공인 IP 를 줬는지, 라우터에서 UDP 16261/16262 를 열었는지 확인 `[위키-W4]`. 같은 집 네트워크에서 전용 서버에 접속이 안 되면 Windows 네트워크 프로필을 "개인"으로 `[위키-W4]`
6. "Loading the world" 에서 멈춤: 위키에 2026-08-03 기준 신규 버그로 올라와 있다. 우회법은 "호스트를 한 번 해 보고 끊은 뒤 친구 서버 접속", 또는 `%UserProfile%\Zomboid\Saves\Multiplayer` 에서 그 서버 폴더 삭제 + 관리자에게 Users 목록에서 자기를 지워 달라고 하기 `[위키-W4]`. 42.21 에 "Fixed an issue which would block clients from loading into server" 가 있다 `[공식-S6]`. 이것으로 완전히 해결됐는지는 **미확인**.

### 모드 다운로드가 멈춤
- Host 서버가 "initializing" 이나 "Downloaded x of y" 에서 멈춤 → `Zomboid\coop-console.txt` 끝에 0/0 bytes 인 모드가 있는지 확인. 중단(**중단** 버튼) 후 다시 시작하고, 다른 모드에서 또 멈추면 반복 `[위키-W4]`
- 전용 서버가 "Getting server info" 에서 멈추거나 모드를 못 받음 → Steam 도구판 문제, SteamCMD 로 설치 `[위키-W4]`

### 서버가 시작 직후 꺼짐
- SandboxVars.lua 문법 오류 → 서버가 즉시 종료 `[코드]`. 우리 스크립트가 쓴 파일이면 지우거나 다시 쓰기
- B42 초기 사례: Host 가 5초쯤 initializing 하다 terminated → `%UserProfile%\Zomboid\db` 폴더를 지우니 해결 `[커뮤니티-C1]`. `db` 에는 서버 계정 DB(`<서버이름>.db`)가 있으므로 지우기 전에 백업 `[로그]`
- 로그에 `Cannot invoke "zombie.characters.Role.hasCapability..."` 가 보이면 `UsernameDisguises`/`HideDisguisedUserName` 끄기 `[위키-W4]` (42.21 에서 관련 접속 문제 수정 `[공식-S6]`)
- 서버 메모리를 PC 여유보다 크게 잡았을 때 시작 실패: Host 서버는 시작할 때 메모리를 통째로 잡으므로(`-Xms`=`-Xmx`) `[코드]` 실패할 수 있다고 본다. 실제 증상은 **미확인**
- 로그 위치: Host 서버 `Zomboid\coop-console.txt`, 게임 `Zomboid\console.txt`, 전용 서버 `server-console.txt`, 지원 요청용 `Zomboid\logs.zip` `[위키-W4]`

### 세이브 위치와 백업
- 세계: `%USERPROFILE%\Zomboid\Saves\Multiplayer\<서버이름>\` (+ `<서버이름>_player\`) `[코드]` `[위키-W2]`
- 설정: `%USERPROFILE%\Zomboid\Server\<서버이름>*` `[위키-W3]`, 계정 DB: `%USERPROFILE%\Zomboid\db\<서버이름>.db` `[로그]`
- 자동 백업: `BackupsOnStart=true` → 서버를 켤 때마다 `Zomboid\backups\startup\backup_N.zip` (최대 `BackupsCount=5`개). 버전이 바뀌면 `backups\version\` `[로그]`. 백업 zip 에는 `options.ini`, `Lua`, `mods`, `db`, `Server` 폴더와 `Saves\Multiplayer\<서버이름>` 이 들어간다 `[코드]`
- 수동 백업: 게임을 끈 상태에서 `%USERPROFILE%\Zomboid` 폴더를 통째로 압축 `[위키-W4]`

### 호스트 RAM
- Host 화면의 "서버 메모리 설정 :" 드롭다운: 0.75GB ~ 16GB, 0.25GB 단위, 저장값이 없으면 4GB `[코드]`
- 권장: "Allocate at least 3 GB of RAM for the server itself to run, then add approximately 500 MB of memory for each additional player" — 예: 4명 → 3 + 4×0.5 = 5GB, 모드가 많으면 더 `[위키-W4]` (같은 공식이 Steam 토론에도 있음 `[커뮤니티-C1]`)
- 게임 자체(클라이언트)는 기본 3GB(`ProjectZomboid64.json` 의 `-Xmx3072m`) `[코드]` `[위키-W4]`. 게임 메모리는 이 파일의 `-Xmx` 를 고쳐 늘린다 `[위키-W4]`
- Steam 최소 사양: RAM 8GB (게임만 기준) `[외부-V3]`
- → 호스트 PC 에는 게임 3GB + 서버 5~6GB + Windows 몫이 동시에 필요하다. 친구 4명 + 모드면 **RAM 16GB 이상** 권장 (위 수치로 계산한 판단).

## 10. "한 번에 설치" 가능성

### 호스트용: `irm <url> | iex` 로 설정 파일 써 넣기 → 가능

**ini 를 처음부터 만들어도 되는가 → 된다 (코드 확인)**
- `ServerOptions.init()`: `<캐시>\Server\<서버이름>.ini` 가 있으면 `loadServerTextFile` → 성공하면 바로 `saveServerTextFile`, 없으면 `saveServerTextFile` 로 기본값 생성 `[코드]`.
- `loadServerTextFile`: 파일의 각 `이름=값` 중 **게임이 아는 이름만** 값을 반영한다. 모르는 이름은 무시 `[코드]`.
- `saveServerTextFile`: 게임이 아는 **모든** 옵션을 현재 값(파일 값 또는 기본값)으로 다시 쓴다 `[코드]`. → 빠진 키는 기본값으로 채워진다. 우리가 단 주석은 없어지고 게임 주석으로 바뀐다.
- `ResetID`, `ServerPlayerID` 는 없으면 새로 생긴다 (42.21 생성 파일에서 기본값이 무작위였음) `[로그]`.
- SandboxVars 도 같다: 서버가 `loadServerLuaFile` 로 읽고 곧바로 `saveServerLuaFile` 로 다시 쓴다 `[코드]`. 각 옵션은 표에 그 키가 있을 때만 값을 바꾸고, 하위 표(`Map = {…}`)가 없으면 그냥 기본값으로 둔다 `[코드]`. `VERSION` 값에 따라 옛 형식을 바꾸는 단계가 있으므로 `VERSION = 6` 을 넣는다 `[코드]`.

**파일 형식 규칙 (ini 파서 `ConfigFile.read`)** `[코드]`
- 줄 단위. 앞뒤 공백을 지운 뒤 빈 줄과 `#` 로 시작하는 줄은 건너뛴다.
- `=` 가 없는 줄은 오류로 기록하고 건너뛴다.
- `split("=")` 으로 나눈다 → **값 안에 `=` 를 넣으면 잘린다**. 키와 `=` 사이에 공백도 넣지 않는다 (`PVP = false` 는 키 이름이 `PVP ` 가 되어 무시됨).
- BOM 은 지우지 않는다 → BOM 없는 UTF-8. 안전하게 첫 줄은 `#` 주석으로.
- 실측 생성 파일은 UTF-8 (BOM 없음), CRLF 줄바꿈이었다 `[로그]`.

**스크립트가 지켜야 할 것 (위 사실에서 나온 설계 판단)**
1. 게임(`ProjectZomboid64`)이 꺼져 있는지 확인. 켜져 있으면 중단하고 안내.
2. `$env:USERPROFILE\Zomboid\Server` 가 없으면 만든다 (게임도 Host 화면을 열 때 없으면 만든다 `[코드]`).
3. 같은 이름 파일이 있으면 `.ini` 로 끝나지 않는 이름으로 백업 (예: `zomboid-multi.ini.20261018-1530.bak`). `.ini` 로 끝나면 Host 목록에 뜬다 `[코드]`.
4. 4개 파일을 모두 쓴다. 특히 spawnregions 는 42.21 Host 가 만드는 11개 도시판(부록 B)을 쓴다. 서버 내장 대체 템플릿은 4개 도시뿐이다 `[코드]`.
5. BOM 없는 UTF-8 (`New-Object System.Text.UTF8Encoding($false)` + `[IO.File]::WriteAllText`). PowerShell 5.1 의 `Set-Content -Encoding UTF8` / `Out-File -Encoding UTF8` 는 BOM 을 붙인다 `[외부-M2]`.
6. Lua 문법이 깨지면 서버가 즉시 종료되므로 고정 템플릿만 쓴다 `[코드]`.
7. (선택) `Zomboid\Lua\host.ini` 의 `servername=` 을 `zomboid-multi` 로 바꿔 Host 화면 기본 선택 지정. 이 파일 형식은 `servername=…`, `username=…`, `memory=…`(MB) 세 줄, CRLF `[코드]`. `memory` 는 768~16384 사이 256 단위여야 드롭다운과 맞는다 `[코드]`.
8. 스크립트 본문은 ASCII 로 쓰거나, 서버가 `Content-Type: …; charset=utf-8` 을 주게 한다. Windows PowerShell 5.1 의 `irm` 이 charset 없는 응답의 한글을 어떻게 읽는지는 **미확인**.
9. 원문 보기 링크와 수동 대안(zip 받아서 폴더에 복사)을 같이 준다. 실행 정책은 이 형태를 막지 않는다 `[외부-M1]`.

**게임이 이미 만든 기본 ini 에 몇 줄만 바꾸는 방식과 비교**: 결과는 같다 (어느 쪽이든 서버가 시작할 때 전체를 다시 쓴다) `[코드]`. 처음부터 쓰는 쪽이 친구가 게임을 한 번도 안 켰어도 되므로 더 단순하다. 단, 이미 진행 중인 세계(`Saves\Multiplayer\zomboid-multi` 가 있음)에서 SandboxVars 를 바꾸면 어디까지 반영되는지는 **미확인** (시작 날짜처럼 세계를 만들 때만 쓰는 값은 안 바뀔 것으로 보임).

### 참가자용: 컬렉션 없이 "접속만 하면 자동 설치" → 된다
- 근거는 5절. 참가자는 Steam 초대 수락 → "설치" 클릭만 하면 된다 `[코드]` `[위키-W2]` `[가이드-G3]`.

### `steam://` 링크로 할 수 있는 것
| 링크 | Valve 문서상 동작 `[외부-V1]` | 좀보이드 적용 |
|---|---|---|
| `steam://url/CommunityFilePage/<id>` | "Opens a Workshop/Greenlight submission." (Steam 클라이언트에서 창작마당 페이지 열기) | 모드 미리보기/수동 구독용으로 쓸 수 있다. 자동 설치에는 필요 없음 |
| `steam://connect/<IP>[:<port>][/<password>]` | "Connects the user to the server specified by the IP." (DNS 이름 안 됨) | 좀보이드 서버는 Steam 게임 서버로 등록된다 `[코드]`. 실제로 이 링크가 게임을 켜고 접속하는지는 **미확인** |
| `steam://run/108600//+connect <ip>:<port>/` | "Runs an application … args are passed to the application as launch parameters." | 게임은 실행 인자 `+connect`, `+password` 를 읽어 메인 메뉴에서 접속 창을 자동으로 띄운다 `[코드]`. 하지만 IP 접속이라 포트포워딩이 필요하고, Host 서버면 초대 목록 등록도 필요하다 `[코드]`. 공백을 `%20` 으로 써야 하는지 등 실동작은 **미확인** |

→ 포트포워딩 없는 Host 구성에서 참가자를 넣는 확실한 방법은 **Steam 초대**뿐이다. 웹사이트는 링크 대신 "게임 켜고 메인 메뉴에서 기다리기 → 초대 수락 → 설치" 를 안내하는 것이 맞다.

---

## 웹사이트 가이드 단계 초안

### 호스트 (9단계)
1. Steam 에서 Project Zomboid 를 최신으로 업데이트한다. 라이브러리 → 우클릭 → 속성 → 게임 버전 및 베타에서 베타를 고르지 않은 상태(기본)인지 확인 `[공식-S3]`.
2. (처음이면) 게임을 한 번 켜서 약관에 동의하고, 설정 → 사용자 인터페이스 (UI) → 언어 선택 → 한국어. 확인 후 게임 종료 `[코드]`.
3. 사이트의 PowerShell 한 줄을 붙여 넣어 실행 → `zomboid-multi` 설정 파일 4개 생성.
4. 게임 실행 → 메인 메뉴 **서버 만들기** `[코드]`.
5. **서버 이름 :** 에서 `zomboid-multi` 선택 `[코드]`.
6. **서버 메모리 설정 :** 4명이면 5GB, 모드가 많으면 6~8GB (PC RAM 16GB 이상 권장) `[위키-W4]`.
7. **시작** → 창작마당 아이템 다운로드가 끝날 때까지 대기. Windows 방화벽 창이 뜨면 **액세스 허용** `[로그]` `[위키-W4]`.
8. 캐릭터를 만들어 들어간 뒤 ESC → **친구 초대** → 친구 선택 → **초대** (친구마다, 매 세션) `[코드]`.
9. 끝낼 때는 호스트가 마지막에 나간다. 호스트가 나가면 서버가 저장하고 꺼진다 `[로그]`. 세이브는 `Zomboid\backups\startup` 에 자동 백업된다 `[로그]` `[코드]`.

### 참가자 (4단계)
1. Steam 에서 호스트와 친구인지, 게임이 최신(베타 아님)인지 확인 `[공식-S3]`.
2. 게임을 켜고 **메인 메뉴에서 기다린다** (게임 중이면 초대를 못 받음) `[코드]`.
3. Steam 초대 알림을 수락한다 (또는 Steam 친구 목록에서 호스트 → 게임 참가. 호스트가 먼저 초대/수락해 둬야 함) `[코드]`.
4. "서버에 적용된 창작마당 아이템" 화면에서 **설치** → 다운로드가 끝나면 캐릭터를 만들고 스폰 `[코드]`.

---

## B41 / B42 차이 정리

| 항목 | B41 | B42 (42.21) | 근거 |
|---|---|---|---|
| `Mods=` 형식 | `\` 없음 | 커뮤니티 표준은 `\ModID`. 42.21 서버는 `\` 를 지우고 읽으므로 둘 다 동작. 42.21 UI 는 `\` 없이 씀 | `[가이드-G1]` `[가이드-G2]` `[커뮤니티-C3]` `[코드]` |
| spawnpoints 형식 | (B41 형식은 직접 확인 안 함. 위키 예시는 절대 좌표 `posX = 12067, posY = 6801, posZ = 0` 로 옛 형식으로 보임) | 42.21 생성 파일은 셀+셀 안 좌표 `worldX = 40, worldY = 22, posX = 67, posY = 201` | `[위키-W3]` `[로그]` |
| spawnregions 기본 | (확인 안 함) | Host 생성 파일 11개 도시 (위키 42.20 판도 11개). 서버 내장 대체 템플릿은 4개 도시 | `[위키-W3]` `[로그]` `[코드]` |
| `MaxPlayers` 최대 | (확인 안 함. 위키 문구 "Max: 100" 은 옛 문구로 보임) | 42.21 생성 파일 "최대: 254" | `[위키-W3]` `[로그]` |
| 새 Host 설정에 활성 모드 자동 포함 | (예전 동작으로 보이는 코드가 남아 있음, 확인 안 함) | 비활성 (`if true then return end`) | `[코드]` |
| Host 포트포워딩 | 사용자 경험이 갈림 | 불필요 보고 | `[커뮤니티-C1]` `[커뮤니티-C2]` |
| 번역 파일 | — | `Translate\KO\*.json` | `[코드]` |
| 저장 호환 | B41 세이브는 B42 불가 | 42.19 세이브도 42.20+ 불가 | `[공식-S4]` `[공식-S3]` |

---

## 미확인 목록

1. Windows 방화벽 팝업에 실제로 뜨는 이름 (실측 PC 의 규칙 이름으로 추정: `Zulu Platform x64 Architecture`)
2. `steam://connect`, `steam://run/108600//+connect …` 의 좀보이드 실동작
3. 전용 서버에 "스팀 릴레이 사용"으로 포트포워딩 없이 접속되는지
4. 진행 중인 세계에서 SandboxVars 변경이 어디까지 반영되는지
5. 42.20 에서 `\` 없는 `Mods=` 가 실패했는지 (가이드끼리 상충, 42.21 은 코드상 둘 다 됨)
6. "Loading the world" 버그가 42.21 에서 완전히 해결됐는지
7. 미니맵 단축키 (UI 경로는 코드로 확인)
8. Steam 한국어 클라이언트의 메뉴 표기("게임 버전 및 베타" 등)
9. 서버 메모리를 PC 여유보다 크게 잡았을 때의 실제 증상
10. `irm | iex` 에 대한 Windows Defender / SmartScreen 반응
11. Windows PowerShell 5.1 `irm` 의 charset 없는 응답 디코딩 (스크립트는 ASCII 로 쓰는 것이 안전)
12. Windows 사용자 폴더 이름에 한글이 있을 때 문제가 있는지
13. B42 화면에서 한국어 글꼴이 깨지지 않는지를 눈으로 확인하지는 않음 (설정·로그로만 확인)

---

## 부록 A. 42.21 기본 ini 전체 키와 기본값

출처: 실측 PC 에서 42.21.0 Host 로 처음 시작할 때 게임이 만든 `servertest.ini` (자동 백업 `Zomboid\backups\startup\backup_1.zip` 안) `[로그]`. 주석은 빼고 `키=기본값` 만 원문 순서대로 적었다. 같은 키 이름이 `ServerOptions` 클래스 문자열에도 있다 `[코드]`. 총 144개.

### 요청 키 요약

| 키 | 42.21 기본값 | 비고 |
|---|---|---|
| `PVP` | `true` | `SafetySystem=true` 와 함께면 각자 켠 사람끼리만 PvP |
| `Public` | `false` | 게임 안 서버 목록 노출 |
| `Password` | (빈 값) | Host 버튼 서버에는 무시됨 `[위키-W3]` |
| `MaxPlayers` | `32` | 최소 1, 최대 254, 관리자 제외 |
| `PauseEmpty` | `true` | 접속자가 없으면 시간 정지 |
| `SafetySystem` | `true` | |
| `UPnP` | `true` | |
| `DefaultPort` | `16261` | |
| `UDPPort` | `16262` | |
| `WorkshopItems` | (빈 값) | `;` 구분 숫자 ID |
| `Mods` | (빈 값) | `;` 구분 모드 ID, 4절 참고 |
| `Map` | `Muldraugh, KY` | 맵 모드가 있으면 앞에 추가 |

### 전체 목록

```ini
PVP=true
PVPLogToolChat=true
PVPLogToolFile=true
PauseEmpty=true
GlobalChat=true
ChatStreams=s,r,a,w,y,sh,f,all
Open=true
ServerWelcomeMessage=(긴 기본 환영 문구, 생략)
DisplayUserName=true
ShowFirstAndLastName=false
UsernameDisguises=false
HideDisguisedUserName=false
SwitchZombiesOwnershipEachUpdate=false
SpawnPoint=0,0,0
SafetySystem=true
ShowSafety=true
SafetyToggleTimer=2
SafetyCooldownTimer=3
SafetyDisconnectDelay=60
SpawnItems=
DefaultPort=16261
UDPPort=16262
ResetID=(생성 시 무작위)
Mods=
Map=Muldraugh, KY
DoLuaChecksum=true
DenyLoginOnOverloadedServer=true
Public=false
PublicName=My PZ Server
PublicDescription=
MaxPlayers=32
PingLimit=0
SafehousePreventsLootRespawn=true
DropOffWhiteListAfterDeath=false
NoFire=false
AnnounceDeath=false
AnnounceAnimalDeath=false
SaveWorldEveryMinutes=0
PlayerSafehouse=false
AdminSafehouse=false
SafehouseAllowTrepass=true
SafehouseAllowFire=true
SafehouseAllowLoot=true
SafehouseAllowRespawn=false
SafehouseDaySurvivedToClaim=0
SafeHouseRemovalTime=144
SafehouseAllowNonResidential=false
SafehouseDisableDisguises=true
MaxSafezoneSize=20000
AllowDestructionBySledgehammer=true
SledgehammerOnlyInSafehouse=false
War=false
WarStartDelay=600
WarDuration=3600
WarSafehouseHitPoints=3
ServerPlayerID=(생성 시 무작위)
RCONPort=27015
RCONPassword=
DiscordEnable=false
DiscordToken=
DiscordChatChannel=
DiscordLogChannel=
DiscordCommandChannel=
WebhookAddress=
Password=
MaxAccountsPerUser=0
AllowCoop=true
SleepAllowed=false
SleepNeeded=false
KnockedDownAllowed=false
SneakModeHideFromOtherPlayers=true
UltraSpeedDoesnotAffectToAnimals=false
WorkshopItems=
SteamScoreboard=false
SteamVAC=true
UPnP=true
VoiceEnable=true
VoiceMinDistance=10.0
VoiceMaxDistance=100.0
Voice3D=true
SpeedLimit=70.0
LoginQueueEnabled=false
LoginQueueConnectTimeout=60
server_browser_announced_ip=
PlayerRespawnWithSelf=false
PlayerRespawnWithOther=false
FastForwardMultiplier=40.0
DisableSafehouseWhenOwnerConnected=false
Faction=true
FactionDaySurvivedToCreate=0
FactionPlayersRequiredForTag=1
DisableRadioStaff=false
DisableRadioAdmin=true
DisableRadioGM=true
DisableRadioOverseer=false
DisableRadioModerator=false
DisableRadioInvisible=true
ClientCommandFilter=-vehicle.*;+vehicle.damageWindow;+vehicle.fixPart;+vehicle.installPart;+vehicle.uninstallPart
ClientActionLogs=ISEnterVehicle;ISExitVehicle;ISTakeEngineParts;
PerkLogs=true
ItemNumbersLimitPerContainer=0
BloodSplatLifespanDays=0
AllowNonAsciiUsername=false
BanKickGlobalSound=true
RemovePlayerCorpsesOnCorpseRemoval=false
TrashDeleteAll=false
PVPMeleeWhileHitReaction=false
MouseOverToSeeDisplayName=true
HidePlayersBehindYou=true
PVPMeleeDamageModifier=30.0
PVPFirearmDamageModifier=50.0
CarEngineAttractionModifier=0.5
PlayerBumpPlayer=false
MapRemotePlayerVisibility=1
BackupsCount=5
BackupsOnStart=true
BackupsOnVersionChange=true
BackupsPeriod=0
DisableVehicleTowing=false
DisableTrailerTowing=false
DisableBurntTowing=false
BadWordListFile=
GoodWordListFile=
BadWordPolicy=3
BadWordReplacement=[HIDDEN]
AntiCheatSafety=2
AntiCheatSpeed=2
AntiCheatNoClip=4
AntiCheatHit=2
AntiCheatPacketException=4
AntiCheatPermission=2
AntiCheatXP=2
AntiCheatSafeHouse=2
AntiCheatPlayer=2
AntiCheatChecksum=2
MultiplayerStatisticsPeriod=1
DisableScoreboard=false
HideAdminsInPlayerList=false
MaxPacketsPerSecond=300
ShowCoordinates=false
Seed=
UsePhysicsHitReaction=false
ChatMessageCharacterLimit=200
ChatMessageSlowModeTime=3
```

## 부록 B. 42.21 Host 가 만든 spawnregions / spawnpoints 원문 `[로그]`

`servertest_spawnregions.lua` (탭 들여쓰기, CRLF):

```lua
function SpawnRegions()
	return {
		{ name = "Brandenburg, KY", file = "media/maps/Brandenburg, KY/spawnpoints.lua" },
		{ name = "Echo Creek, KY", file = "media/maps/Echo Creek, KY/spawnpoints.lua" },
		{ name = "Ekron, KY", file = "media/maps/Ekron, KY/spawnpoints.lua" },
		{ name = "Fallas Lake, KY", file = "media/maps/Fallas Lake, KY/spawnpoints.lua" },
		{ name = "Irvington, KY", file = "media/maps/Irvington, KY/spawnpoints.lua" },
		{ name = "March Ridge, KY", file = "media/maps/March Ridge, KY/spawnpoints.lua" },
		{ name = "Muldraugh, KY", file = "media/maps/Muldraugh, KY/spawnpoints.lua" },
		{ name = "Riverside, KY", file = "media/maps/Riverside, KY/spawnpoints.lua" },
		{ name = "Rosewood, KY", file = "media/maps/Rosewood, KY/spawnpoints.lua" },
		{ name = "Valley Station, KY", file = "media/maps/Valley Station, KY/spawnpoints.lua" },
		{ name = "West Point, KY", file = "media/maps/West Point, KY/spawnpoints.lua" },
	}
end
```

`servertest_spawnpoints.lua`:

```lua
function SpawnPoints()
	return {
		unemployed = {
			{ worldX = 40, worldY = 22, posX = 67, posY = 201 }
		}
	}
end
```

## 부록 C. 최소 파일 예시 (제안, 실제 서버로 돌려 보지는 않음)

아래는 3·10절의 코드 확인 결과에 맞춘 **제안**이다. 서버가 빠진 키를 채운다는 것은 코드로 확인했지만, 이 예시 파일 그대로 서버를 띄워 보지는 않았다.

`zomboid-multi.ini` (모드 ID/숫자는 자리표시자):

```ini
# zomboid-multi (written by installer; the game rewrites this file on server start)
PVP=false
PauseEmpty=true
MaxPlayers=8
Public=false
WorkshopItems=1111111111;2222222222
Mods=\ModIdA;\ModIdB
Map=Muldraugh, KY
```

`zomboid-multi_SandboxVars.lua` (빠진 항목은 기본값으로 채워짐):

```lua
SandboxVars = {
    VERSION = 6,
    Map = {
        AllowMiniMap = true,
    },
}
```

BOM 없는 UTF-8 로 쓰는 PowerShell 5.1 호환 예시 (메시지는 인코딩 문제를 피하려고 영어):

```powershell
$dir = Join-Path $env:USERPROFILE 'Zomboid\Server'
if (Get-Process -Name ProjectZomboid64 -ErrorAction SilentlyContinue) { throw 'Close Project Zomboid first.' }
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$enc = New-Object System.Text.UTF8Encoding($false)   # BOM 없음
$ini = "# zomboid-multi`r`nPVP=false`r`nMaxPlayers=8`r`n"
[System.IO.File]::WriteAllText((Join-Path $dir 'zomboid-multi.ini'), $ini, $enc)
```

## 부록 D. 코드 근거 위치 (42.21.0, rev `4a0e9546ec`)

게임 폴더: `C:\Program Files (x86)\Steam\steamapps\common\ProjectZomboid\`

| 확인한 사실 | 위치 |
|---|---|
| Host 화면, 설정 목록, 메모리 드롭다운(512+i×256MB, i=1..62, 기본 4096), 시작 시 새 설정만 기본값 생성, `host.ini` 형식, Steam 모드에서 Steam ID 로 접속 | `media\lua\client\OptionScreens\CoopOptionsScreen.lua` |
| 서버 설정 화면의 모드 목록이 `modInfo:getId()` 를 쓰는 것, 새 설정이 활성 모드를 넣지 않음(`if true then return end`), "설정 저장 경로" | `media\lua\client\OptionScreens\ServerSettingsScreen.lua` |
| 친구 초대/수락/거절, `invited.ini`, `invite-add` | `media\lua\client\OptionScreens\InviteFriends.lua` |
| 초대 수락은 메인 메뉴에서만, `+connect` 처리 | `media\lua\client\OptionScreens\MainScreen.lua` (`MainScreen.onAcceptInvite`, `MainScreenPanelJoinSteam`) |
| 초대 문자열에 Steam ID, IP 접속 시 hosted 서버면 Steam ID 접속으로 전환 | `media\lua\client\OptionScreens\BootstrapConnectPopup.lua` |
| 참가자 창작마당 화면 | `media\lua\client\OptionScreens\ServerWorkshopItemScreen.lua` |
| 미니맵 허용 조건, 지도 아이콘 선택 창 | `media\lua\client\ISUI\Maps\ISMiniMap.lua`, `media\lua\client\ISUI\ISEquippedItem.lua` |
| 언어 선택이 UI 탭에 있고 바로 적용 | `media\lua\client\OptionScreens\MainOptions.lua` |
| 한국어 문구 원문 | `media\lua\shared\Translate\KO\UI.json`, 영문 `...\EN\UI.json` |
| 게임 기본 메모리 `-Xmx3072m` | `ProjectZomboid64.json` |
| ini 읽기 후 즉시 다시 쓰기, 아는 키만 반영 | `projectzomboid.jar` `zombie.network.ServerOptions.init / loadServerTextFile / saveServerTextFile` |
| ini 파서 규칙 (trim, `#`, `split("=")`) | `zombie.config.ConfigFile.read` |
| 설정 목록 필터와 이름 규칙, 설정 폴더 = 캐시\Server | `zombie.network.ServerSettingsManager.readAllSettings / isValidName / isValidNewName / getSettingsFolder`, `ServerSettingsManager$1.accept` |
| `Mods=` 에서 `\` 제거, `WorkshopItems=` 숫자 ID 검사, SandboxVars 읽기 실패 시 `System.exit` | `zombie.network.GameServer.main` |
| SandboxVars 부분 파일 허용 (`fromTable` 이 없는 키는 건너뜀), `VERSION` 업그레이드 | `zombie.SandboxOptions.readLuaFile`, `SandboxOptions$BooleanSandboxOption.fromTable` |
| Host 서버는 호스트/초대된 Steam ID 만 받음 | `zombie.core.znet.SteamUtils.clientInitiateConnectionCallback`, `zombie.network.CoopSlave.isInvited / handleCommand` |
| `inviteFriend` = 초대 목록 추가 + Steam 초대 전송 | `zombie.Lua.LuaManager$GlobalObject.inviteFriend / canInviteFriends` |
| Host 서버 실행 인자 (`jre64\bin\java`, `-Xms`/`-Xmx`, `-coop`, `-servername`) | `zombie.network.CoopMaster` (문자열 상수) |
| 참가자 자동 구독/다운로드, 버전 불일치 판정 | `zombie.gameStates.ConnectToServerState$WorkshopItem.CheckItemState` |
| 호스트 접속명 = Steam 닉네임 | `zombie.network.GameClient.doConnectCoop` (`SteamFriends.GetPersonaName`) |
| Host+Steam 로그인은 `authClient`(비ASCII 검사) 생략, 전용 서버는 검사 | `zombie.network.packets.connection.LoginPacket.processServer`, `zombie.network.ServerWorldDatabase.authClient` |
| 리치 프레즌스 `+connect` 등록 | `zombie.gameStates.IngameState` (`SteamFriends.UpdateRichPresenceConnectionInfo`) |
| 실행 인자 `+connect`, `+password` | `zombie.gameStates.MainScreenState` (문자열 상수) |
| 자동 백업에 들어가는 항목 | `zombie.core.backup.ZipBackup` (문자열 상수) |
| 기본 언어 = options.ini → Windows 로캘 → 영어 | `zombie.core.Translator.getLanguage` |
| `mod.info` 의 `id=`, `require=` 에서 `\` 제거 | `zombie.gameStates.ChooseGameInfo`, `zombie.modding.ActiveModsFile.fromString` |
| Steam P2P 사용 | `ZNetJNI64.dll` 문자열 (`P2PSessionRequest_t`, `P2PSessionConnectFail_t`, `SteamNetworking006`, `Client version=%s has begun P2P connection`) |

로그/생성 파일 (실측 PC, 개인 식별 정보는 이 문서에 옮기지 않음): `%USERPROFILE%\Zomboid\coop-console.txt`, `%USERPROFILE%\Zomboid\version.txt`, `%USERPROFILE%\Zomboid\backups\startup\backup_1.zip`, `%USERPROFILE%\Zomboid\Lua\host.ini`, `%USERPROFILE%\Zomboid\options.ini`.

---

## 출처

### 공식 (The Indie Stone)
- [S1] 42.21 Stable Released (2026-09-28) — https://projectzomboid.com/blog/news/2026/09/42-21-stable-released/
- [S2] Re-population of the Dead: Build 42.21 Unstable released (2026-09-23) — https://projectzomboid.com/blog/news/2026/09/re-population-of-the-dead-build-42-21-unstable-released/
- [S3] PROJECT ZOMBOID BUILD 42.20 RELEASED! (2026-07-29) — https://projectzomboid.com/blog/news/2026/07/project-zomboid-build-42-20-released/
- [S4] B42 CHECKLIST (2026-07-28) — https://projectzomboid.com/blog/news/2026/07/b42-checklist/
- [S5] 공식 뉴스 목록 (상단 "Stable Build: 42.21") — https://projectzomboid.com/blog/news/
- [S6] 42.21 Patch Notes (포럼) — https://theindiestone.com/forums/topic/101693-4221-unstable-released/

### 위키 (pzwiki.net)
- [W1] Build 42 — https://pzwiki.net/wiki/Build_42
- [W2] Dedicated server (2026-10-06 수정) — https://pzwiki.net/wiki/Dedicated_server
- [W3] Server settings (2026-10-06 수정) — https://pzwiki.net/wiki/Server_settings
- [W4] Tech Support (2026-10-06 갱신) — https://pzwiki.net/wiki/Tech_Support
- [W5] Multiplayer — https://pzwiki.net/wiki/Multiplayer
- [W6] Mods — https://pzwiki.net/wiki/Mods

### 외부 공식 문서
- [V1] Valve Developer Community, Steam browser protocol — https://developer.valvesoftware.com/wiki/Steam_browser_protocol (원본이 봇 차단이라 Wayback 사본으로 확인: https://web.archive.org/web/2026id_/https://developer.valvesoftware.com/wiki/Steam_browser_protocol)
- [V2] Steamworks, ISteamNetworking — https://partner.steamgames.com/doc/api/ISteamNetworking
- [V3] Steam 상점 Project Zomboid (지원 언어, 최소 사양) — https://store.steampowered.com/app/108600/ (값은 `https://store.steampowered.com/api/appdetails?appids=108600` 로 확인)
- [M1] Microsoft, about_Execution_Policies (PowerShell 5.1) — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-5.1
- [M2] Microsoft, about_Character_Encoding (PowerShell 5.1, "UTF8 Uses UTF-8 (with BOM)") — https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1

### 커뮤니티 (Steam 토론)
- [C1] B42 multiplayer hosting (2026-02) — https://steamcommunity.com/app/108600/discussions/1/760681630846282883/
- [C2] There's no way to just host a lobby and have friends join is there? (2025-12) — https://steamcommunity.com/app/108600/discussions/1/846243771540651957/
- [C3] B42 deticated server setup with friends step by step (2025-12, 42.13) — https://steamcommunity.com/app/108600/discussions/0/846243771540653994/
- [C4] Workshop item version different than server's. When? (2022, B41) — https://steamcommunity.com/app/108600/discussions/0/3192490350123478202/

### 가이드 (2026-07 이후)
- [G1] low.ms, How to install mods on a Build 42 server (2026-08-03, 08-19 수정) — https://low.ms/knowledgebase/project-zomboid-install-mods-build-42
- [G2] Pine Hosting, Build 42 Server Modding Guide (2026-08-13, 08-19 수정) — https://pinehosting.com/blog/how-to-install-mods-on-a-project-zomboid-build-42-server-self-hosting-server-hosting-guide/
- [G3] build42guide.wiki, Build 42 Multiplayer Guide (2026-09-27 갱신) — https://build42guide.wiki/multiplayer/build-42-multiplayer
- [G4] RespawnHost, Project Zomboid B42 Server — https://respawnhost.com/en/wiki/games/project-zomboid/project-zomboid-b42-server/
- [G5] Supercraft, Workshop item version is different (2026-09-17 수정) — https://supercraft.host/wiki/project-zomboid/workshop-item-version-is-different/
