# Zomboid-multi

Project Zomboid Build 42 멀티 서버 안내 사이트와 호스트용 설치 스크립트.

    https://firstquator.github.io/Zomboid-multi/

서버는 친구 PC 에서 게임 메뉴의 **서버 만들기**(Host)로 열고, 참가자는 호스트의
**Steam 초대**로 들어온다. 포트포워딩, 별도 서버 프로그램, 비밀번호가 필요 없다.
이 방식을 고른 근거는 `docs/research/hosting.md` 에 있다.

## 구성

    data/mods.json            모드팩의 단일 정본. 사이트와 설치 스크립트가 모두 여기서 만든다
    docs/research/            모드 선정(mods.md)과 호스팅 방식(hosting.md) 조사 기록
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

- `zomboid-multi.ini` : `WorkshopItems`, `Mods`, `PVP=false`, `Public=false`, `PauseEmpty=true`
- `zomboid-multi_SandboxVars.lua` : 미니맵 켜기
- `zomboid-multi_spawnregions.lua`, `_spawnpoints.lua` : 42.21 기본 11개 도시

이미 있는 파일은 `*.<시각>.bak` 으로 백업한 뒤 우리 값만 바꾼다. 호스트가 게임 안에서
바꾼 다른 설정은 남는다. 게임이 켜져 있으면 아무것도 쓰지 않고 멈춘다.

본문은 ASCII 로만 만든다. Windows PowerShell 5.1 의 `irm` 이 한글을 깨뜨릴 수 있어서,
화면 문구는 Base64 로 넣고 실행할 때 푼다. 테스트가 이를 검사한다.

## 모드 바꾸기

1. `data/mods.json` 을 고친다. 의존 모드는 별도 항목으로 넣고 `dependsOn` 에 적는다
2. `npm run mods:verify` 로 창작마당 실물과 대조한다(B42 태그, Required items, Mod ID)
3. `modpack.changes` 맨 앞에 변경 내용을 적는다
4. `main` 에 푸시하면 사이트와 설치 스크립트가 함께 갱신된다

호스트는 게임을 끈 상태에서 설치 명령을 다시 실행하면 된다.

## 개발

    npm --prefix web install
    npm run dev          # http://127.0.0.1:4321/Zomboid-multi/
    npm test             # 설치 스크립트, 설정 줄, mods.json 검증
    npm run build

`web/astro.config.mjs` 가 빌드 전에 `mods.json` 을 검사한다(필수 필드, Mod ID 형식,
의존 모드 누락, 로드 순서). 실패하면 빌드가 멈춘다.

`main` 에 `web/`, `data/`, `scripts/` 변경이 푸시되면 `.github/workflows/pages.yml` 이
테스트, 빌드, GitHub Pages 배포를 한다. 저장소 설정의 Pages 소스는 GitHub Actions 여야 한다.
