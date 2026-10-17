# 게임 규칙과 근거 (42.21.0 `projectzomboid.jar` 디컴파일, 2026-10-18)

스크립트는 아래 규칙을 그대로 따라 한다. 빌드가 바뀌면 같은 방법으로 다시 확인한다.

## 다시 확인하는 법

```
# CFR 0.152: https://github.com/leibnitz27/cfr/releases/download/0.152/cfr-0.152.jar  (게임 jre64 의 java 로 돌린다)
"$G/jre64/bin/java.exe" -jar cfr.jar "$G/projectzomboid.jar" \
  --jarfilter '^zombie\.(ZomboidFileSystem|gameStates\.ChooseGameInfo|Lua\.LuaManager|core\.Translator|sandbox\.CustomSandboxOptions)$' \
  --outputdir <임시 폴더> --silent true
```

어떤 클래스가 특정 문자열을 쓰는지 모르면 jar 안 `.class` 바이트에서 그 문자열을 찾는다(`sandbox-options` → `CustomSandboxOptions`).

## 버전 폴더 (`ZomboidFileSystem.getModVersionDirName`, `getGameVersionIntFromName`)

- 폴더 이름을 `주 * 1000 + min(부, 999)` 로 읽는다. 세 번째 자리(42.20.**1**)는 무시한다. 숫자가 아니면 0.
- 게임 버전 이하 중 가장 큰 폴더를 쓴다. 없으면 `42.0`(없는 폴더)로 두고 `common` 만 읽는다.
- `common/mod.info` 나 버전 폴더의 `mod.info` 중 하나만 있으면 모드로 인정한다.
- 파일은 `common` 다음 버전 폴더를 읽고, 같은 경로면 버전 폴더가 이긴다(`loadMod`).

## 로드 순서 (`ZomboidFileSystem.loadModAndRequired`)

- `Mods=`(또는 `mods/default.txt`) 순서대로 가되, 각 모드의 `require` 를 그 모드 앞에 먼저 넣는다. 이미 들어간 모드는 건너뛴다.
- `require` 값 앞의 `\` 는 무시된다. `examplemod` 는 거부된다.
- 서버 접속 클라이언트는 서버 모드 목록 앞에 자기 쪽 "번역 전용 모드"(media 아래가 `lua/shared/Translate/*.txt|json` 뿐인 모드)를 더 불러온다(`loadTranslationMods`).

## 파일 덮어쓰기와 Lua 실행 순서 (`ZomboidFileSystem.loadMod`, `LuaManager.LoadDirBase`)

- 모드 순서대로 상대 경로(소문자)를 `activeFileMap` 에 넣고 나중 모드가 덮는다. 바닐라 같은 경로도 모드 파일이 쓰인다.
- Lua 는 `shared` → `client`(서버는 `server`) 순으로, 각 단계에서 바닐라 파일 전부(경로 알파벳순, 대소문자 무시) 다음에
  모드별 파일(모드 순서, 모드 안에서는 경로 알파벳순)을 실행한다. 같은 경로는 처음 나온 자리에서 한 번만, 최종 파일로 실행된다.
- 하위 폴더까지 모든 `.lua` 를 실행한다(이름이 `New folder` 여도).

## 번역 (`Translator.loadFiles`, `tryFillMapFromMods`)

- 바닐라 → 모드 순서대로 각 모드의 `common` 과 버전 폴더에서 `media/lua/shared/Translate/<언어>/<이름>.json` 을 직접 읽는다.
  경로가 같아도 파일끼리 지우지 않고, 키 단위로 빈 값이 아니면 나중 값이 이긴다.
- JSON 은 `org.json` 으로 읽고 `withStrictMode(Core.IS_DEV)` 다. 정식판은 비엄격(끝 쉼표 허용). 파싱 실패는 `RuntimeException("JSON Error in ...")`.
- 42.21 은 `.json` 만 읽는다. 모드에 같이 있는 B41 식 `*_KO.txt` 는 쓰이지 않는다.

## 샌드박스 옵션 (`CustomSandboxOptions`)

- 모드마다 버전 폴더의 `media/sandbox-options.txt`, 없으면 `common` 의 것을 따로 읽는다. 옵션 이름이 겹치면 문제다.

## Lua 노출 (`LuaManager$Exposer.exposeAll`, `LuaManager$GlobalObject`, `LuaEventManager`)

- `setExposed(X.class)` 로 노출한 클래스와 그 상위 클래스의 public 메서드를 Lua 에서 `obj:method()` 로 부를 수 있다.
  스크립트는 `LuaManager$Exposer` 상수 풀의 클래스 참조를 노출 목록으로 본다(상위집합).
- 전역 함수는 `GlobalObject` 의 `@LuaMethod(name=..., global=true)`. 스크립트는 그 클래스의 식별자 문자열을 상위집합으로 쓴다.
- 이벤트는 `LuaEventManager.AddEvent("...")` 로 등록한 262개(42.21)와 Lua 의 `LuaEventManager.AddEvent`.
  없는 이벤트 이름의 `Events.X` 는 `nil` 이라 `.Add` 에서 오류가 난다.

## 테스트 실행 인자

- 서버: `zombie.network.GameServer -nosteam -cachedir=<폴더> -servername <이름> -adminpassword <비번>` (비번이 없으면 콘솔에서 묻고 멈춘다).
- 클라이언트: `ProjectZomboid64.exe -nosteam -cachedir=<폴더>`. 활성 모드는 `<폴더>/mods/default.txt`, 초기화 방지용
  `reset-mods-42_00.txt` 가 있어야 한다. 창 모드는 `options.ini` 의 `fullScreen=false`, `width`, `height`.
- 서버가 만든 `mods/loaded.txt` 를 클라이언트 폴더로 옮기지 않는다(시작 때 default.txt 에 합쳐지고 지워진다).
