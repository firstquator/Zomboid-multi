# Zomboid-multi

Project Zomboid Build 42 멀티 서버 안내 사이트와 호스트용 설치 스크립트.

    https://firstquator.github.io/Zomboid-multi/

서버는 친구 PC 에서 게임 메뉴의 **서버 만들기**(Host)로 열고, 참가자는 호스트의
**Steam 초대**로 들어온다. 포트포워딩, 별도 서버 프로그램, 비밀번호가 필요 없다.
이 방식을 고른 근거는 `docs/research/hosting.md` 에 있다.

## 구성

    data/mods.json            모드팩의 단일 정본. 사이트와 설치 스크립트가 모두 여기서 만든다
    docs/research/            모드 선정(mods.md), 모드 호환성(compat.md), 호스팅 방식(hosting.md) 조사 기록
    scripts/verify-workshop.mjs  창작마당 실물과 mods.json 대조
    web/                      Astro 정적 사이트
      src/pages/              index, host(호스트 가이드), join(참가자 가이드), mods, help
      src/pages/install.ps1.ts   호스트가 실행하는 설치 스크립트를 빌드 때 만든다
      src/lib/installer.mjs   설치 스크립트 생성기
      src/lib/server-config.mjs  WorkshopItems= / Mods= 줄 생성
      src/data/guides.mjs     두 가이드의 단계 제목
      src/data/shots.json     가이드에 넣는 실제 화면 사진 목록(없으면 단순화한 그림을 쓴다)

## 설치 스크립트

호스트는 PowerShell 에 아래 한 줄을 붙여 넣는다.

    irm https://firstquator.github.io/Zomboid-multi/install.ps1 | iex

`%USERPROFILE%\Zomboid\Server` 에 `zomboid-multi` 설정 파일 4개를 다룬다.

- `zomboid-multi.ini` : `WorkshopItems`, `Mods`, `PVP=false`, `Public=false`, `PauseEmpty=true`,
  `MapRemotePlayerVisibility=4`(지도에 플레이어 위치 모두 표시)
- `zomboid-multi_SandboxVars.lua` : 미니맵 켜기, `MinutesPerPage=0.1`(기술 서적 거의 바로 읽기)
- `zomboid-multi_spawnregions.lua`, `_spawnpoints.lua` : 42.21 기본 11개 도시

서버 옵션과 샌드박스 값은 `data/mods.json` 의 `vanilla` 에 적는다. 화면 이름과 위치(`where`),
기본값(`default`)도 같이 적어 두면 사이트의 모드 목록과 호스트 가이드에 그대로 나온다.

이미 있는 파일은 `*.<시각>.bak` 으로 백업한 뒤 우리 값만 바꾼다. 호스트가 게임 안에서
바꾼 다른 설정은 남는다. 게임이 켜져 있으면 아무것도 쓰지 않고 멈춘다.

본문은 ASCII 로만 만든다. Windows PowerShell 5.1 의 `irm` 이 한글을 깨뜨릴 수 있어서,
화면 문구는 Base64 로 넣고 실행할 때 푼다. 테스트가 이를 검사한다.

## 모드 바꾸기

1. `data/mods.json` 을 고친다. 의존 모드는 별도 항목으로 넣고 `dependsOn` 에 적는다.
   두 모드가 서로를 필수로 지정하면 양쪽 모두 적는다(검사기가 순서 검사에서 뺀다)
2. `npm run mods:verify` 로 창작마당 실물과 대조한다(B42 태그, Required items, Mod ID)
3. `modpack.changes` 맨 앞에 변경 내용을 적는다
4. `main` 에 푸시하면 사이트와 설치 스크립트가 함께 갱신된다

호스트는 게임을 끈 상태에서 설치 명령을 다시 실행하면 된다.

## 캐릭터 만들기 페이지

`/character/` 는 직업·특성 설명, 역할별 추천 조합, 포인트 계산기를 담는다. 직업·특성의
포인트, 기술 보너스, 함께 못 고르는 특성, 한국어 이름, 아이콘은 게임 파일에서 뽑는다.

    python scripts/extract-character.py "C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid"

`web/src/data/character.json` 과 `web/public/icons/` (무손실 webp)를 다시 만든다. 게임이
업데이트되면 다시 돌리고, 추천 조합(`web/src/data/builds.mjs`)이 여전히 포인트에 맞는지
`npm test` 로 확인한다. 멀티에서 잠 설정이 꺼져 있으면 수면 특성 3개는 고를 수 없다
(게임 `CharacterCreationProfession.lua` 의 `isTraitEnabled`).

커뮤니티 추천(`communityBuilds`)은 공략 사이트·위키·블로그·유튜브에서 실제로 추천한 조합이고,
출처 링크를 함께 둔다. 원래 조합에 수면 특성이 있으면 우리 서버용으로 바꾸고 원래 조합과 바꾼
이유를 `original`, `changed` 에 남긴다. 찾은 과정은 `docs/research/builds-*.md` 에 있다.
특성 칩(`TraitChip`)에 마우스를 올리면 `TraitTip` 이 게임 설명과 우리 평가를 띄운다.

## 개발

    npm --prefix web install
    npm run dev          # http://127.0.0.1:4321/Zomboid-multi/
    npm test             # 설치 스크립트, 설정 줄, mods.json 검증
    npm run build

`web/astro.config.mjs` 가 빌드 전에 `mods.json` 을 검사한다(필수 필드, Mod ID 형식,
의존 모드 누락, 로드 순서). 실패하면 빌드가 멈춘다.

`main` 에 `web/`, `data/`, `scripts/` 변경이 푸시되면 `.github/workflows/pages.yml` 이
테스트, 빌드, GitHub Pages 배포를 한다. 저장소 설정의 Pages 소스는 GitHub Actions 여야 한다.
