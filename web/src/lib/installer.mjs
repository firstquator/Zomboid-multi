// 호스트용 설치 스크립트(install.ps1)를 mods.json 에서 만든다.
//
// 친구는 PowerShell 에 `irm <주소> | iex` 한 줄을 붙여 넣는다. 이때 Windows
// PowerShell 5.1 의 irm 은 GitHub Pages 가 주는 .ps1 을 UTF-8 로 읽어 준다는
// 보장이 없어서, 한글이 섞이면 깨진 글자가 그대로 실행된다. 그래서 스크립트
// 본문은 ASCII 로만 쓰고, 화면에 띄울 한글 문구는 UTF-8 바이트를 Base64 로
// 넣었다가 실행할 때 푼다. 테스트가 ASCII 여부를 검사한다.
//
// 쓰는 파일은 %USERPROFILE%\Zomboid\Server 아래 네 개다(docs/research/hosting.md 10절).
// - <이름>.ini            : 있으면 우리 키만 바꾸고, 없으면 새로 만든다
// - <이름>_SandboxVars.lua : 있으면 우리 값만 바꾸고, 없으면 새로 만든다
// - <이름>_spawnregions.lua, _spawnpoints.lua : 없을 때만 만든다
// 이미 있는 파일을 통째로 덮지 않는 이유는, 호스트가 게임 안 "서버 설정" 에서
// 바꾼 값(좀비 수 등)이 모드팩을 갱신할 때마다 기본값으로 돌아가면 안 되기 때문이다.
// 게임 서버는 시작할 때 빠진 키를 기본값으로 채워 파일을 다시 쓴다.

import { iniOverrides, ordered } from "./server-config.mjs";

/** 화면에 나가는 문구. 첫 화면의 터미널 연출도 같은 문구를 쓴다. */
export const MESSAGES = {
  title: "[좀보이드 멀티] 서버 설정 설치",
  ok: "완료",
  gameRunning: "Project Zomboid가 실행 중입니다. 게임을 완전히 끈 뒤 다시 실행하세요.",
  checkFolder: "설정 폴더 확인",
  backup: "기존 설정 백업",
  mods: (n) => `서버 설정에 모드 ${n}개 등록`,
  sandbox: "샌드박스 설정 (미니맵, 독서 시간)",
  spawn: "스폰 지역 11곳 등록",
  preselect: "서버 만들기 화면 기본 선택 지정",
  done: "설치 완료",
  next: (name) => `게임 실행 → 서버 만들기 → 서버 이름 ${name} → 시작`,
  fail: "설치 중 오류가 발생했습니다. 이 창을 캡처해 공유하세요.",
};

// 42.21 의 서버 만들기가 직접 만드는 스폰 지역 목록(11개 도시) 그대로다.
// 파일이 없을 때 서버가 쓰는 내장 대체본은 4개 도시뿐이라 우리가 넣는다.
const SPAWN_TOWNS = [
  "Brandenburg, KY",
  "Echo Creek, KY",
  "Ekron, KY",
  "Fallas Lake, KY",
  "Irvington, KY",
  "March Ridge, KY",
  "Muldraugh, KY",
  "Riverside, KY",
  "Rosewood, KY",
  "Valley Station, KY",
  "West Point, KY",
];

export const SPAWN_REGIONS_LUA = [
  "function SpawnRegions()",
  "\treturn {",
  ...SPAWN_TOWNS.map((t) => `\t\t{ name = "${t}", file = "media/maps/${t}/spawnpoints.lua" },`),
  "\t}",
  "end",
  "",
].join("\n");

export const SPAWN_POINTS_LUA = [
  "function SpawnPoints()",
  "\treturn {",
  "\t\tunemployed = {",
  "\t\t\t{ worldX = 40, worldY = 22, posX = 67, posY = 201 }",
  "\t\t}",
  "\t}",
  "end",
  "",
].join("\n");

const LUA_KEY = /^[A-Za-z_][A-Za-z0-9_]*$/;
const LUA_VALUE = /^(true|false|-?\d+(\.\d+)?)$/;

/**
 * 샌드박스 값 목록으로 SandboxVars.lua 를 만든다.
 * 이 파일에 문법 오류가 있으면 서버가 시작하자마자 꺼지므로, 키와 값은
 * 정해진 모양만 받고 나머지는 빌드를 멈춘다.
 * @param {{ key: string, value: string }[]} values key 는 "MinutesPerPage" 처럼 맨 위 값이거나
 *   "Map.AllowMiniMap" 처럼 묶음 안의 값
 */
export function sandboxLua(values) {
  const top = [];
  const groups = new Map();
  for (const { key, value } of values) {
    const parts = key.split(".");
    if (parts.length > 2 || !parts.every((p) => LUA_KEY.test(p))) {
      throw new Error(`샌드박스 키 형식이 아닙니다: ${key} (예: MinutesPerPage, Map.AllowMiniMap)`);
    }
    if (!LUA_VALUE.test(String(value))) {
      throw new Error(`샌드박스 값은 true, false, 숫자만 씁니다: ${key} = ${value}`);
    }
    if (parts.length === 1) {
      top.push([parts[0], value]);
      continue;
    }
    if (!groups.has(parts[0])) groups.set(parts[0], []);
    groups.get(parts[0]).push([parts[1], value]);
  }
  const lines = ["SandboxVars = {", "    VERSION = 6,"];
  for (const [k, v] of top) lines.push(`    ${k} = ${v},`);
  for (const [group, entries] of groups) {
    lines.push(`    ${group} = {`);
    for (const [k, v] of entries) lines.push(`        ${k} = ${v},`);
    lines.push("    },");
  }
  lines.push("}", "");
  return lines.join("\n");
}

const b64 = (s) => Buffer.from(s, "utf8").toString("base64");
const psq = (s) => `'${String(s).replace(/'/g, "''")}'`;

/** 첫 화면 터미널에 보여 줄 줄들. 실제 스크립트 출력과 같은 문구를 쓴다. */
export function demoLines({ modCount, serverName }) {
  return [
    { text: MESSAGES.title, tone: "warn" },
    { text: `  ${MESSAGES.checkFolder}`, status: MESSAGES.ok, tone: "ok" },
    { text: `  ${MESSAGES.mods(modCount)}`, status: MESSAGES.ok, tone: "ok" },
    { text: `  ${MESSAGES.sandbox}`, status: MESSAGES.ok, tone: "ok" },
    { text: `  ${MESSAGES.spawn}`, status: MESSAGES.ok, tone: "ok" },
    { text: MESSAGES.done, tone: "accent" },
    { text: MESSAGES.next(serverName), tone: "plain" },
  ];
}

/**
 * @param {object} o
 * @param {any[]} o.mods mods.json 의 mods
 * @param {string} o.serverName 설정 이름. 파일 이름과 서버 만들기 화면의 "서버 이름" 이 된다
 * @param {string} o.siteUrl 사이트 주소. 스크립트 머리말에 남긴다
 * @param {string} o.repoUrl 저장소 주소
 * @param {string} o.modpackVersion 모드팩 버전
 * @param {{ key: string, value: string }[]} [o.sandbox] 샌드박스 값. key 는 "MinutesPerPage", "Map.AllowMiniMap" 형식
 * @param {{ key: string, value: string }[]} [o.ini] 서버 설정(ini)에 더 넣을 값(지도 표시 등)
 */
export function buildInstaller({ mods, serverName, siteUrl, repoUrl, modpackVersion, sandbox = [], ini = [] }) {
  const list = ordered(mods);
  const overrides = iniOverrides(list, ini);
  const M = MESSAGES;
  const crlf = (s) => s.replace(/\r?\n/g, "\r\n");

  const overrideLines = Object.entries(overrides)
    .map(([k, v]) => `    ${psq(k)} = ${psq(v)}`)
    .join("\n");
  // 기존 SandboxVars 를 고칠 때는 마지막 이름(AllowMiniMap)만으로 찾는다.
  const sandboxPatch = sandbox.map((s) => `    ${psq(s.key.split(".").pop())} = ${psq(s.value)}`).join("\n");
  // 모드 원제에도 한글이 섞여 있으므로(예: 한글 입력 모드) 목록도 Base64 로 넣는다.
  const modNames = list.map((m) => `    '${b64(`${m.workshopId}  ${m.name}`)}'`).join(",\n");

  const script = `# Zomboid-multi server preset installer
# Generated from data/mods.json (modpack ${modpackVersion}). Do not edit by hand.
# Site:   ${siteUrl}
# Source: ${repoUrl}
#
# What this script does (only inside %USERPROFILE%\\Zomboid):
#   1. Stops if Project Zomboid is running (the server rewrites these files on start).
#   2. Backs up existing ${serverName} files in Zomboid\\Server as *.<time>.bak.
#   3. ${serverName}.ini: sets WorkshopItems, Mods and a few options. Other keys are kept.
#   4. ${serverName}_SandboxVars.lua: turns on the values below (creates the file if missing).
#   5. ${serverName}_spawnregions.lua / _spawnpoints.lua: created only if missing.
#   6. Zomboid\\Lua\\host.ini: if present, preselects ${serverName} on the Host screen.
# It downloads nothing else and changes nothing outside %USERPROFILE%\\Zomboid.

function Install-ZomboidMulti {
  $ErrorActionPreference = 'Stop'

  function T([string]$b) { [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b)) }
  function Say([string]$b, [string]$color = 'Gray') { Write-Host (T $b) -ForegroundColor $color }
  function Step([string]$b) {
    Write-Host ('  ' + (T $b) + ' ... ') -NoNewline
    Write-Host (T '${b64(M.ok)}') -ForegroundColor Green
  }
  function Set-IniKey($lines, [string]$key, [string]$value) {
    $line = $key + '=' + $value
    for ($i = 0; $i -lt $lines.Count; $i++) {
      if ($lines[$i] -match ('^' + [regex]::Escape($key) + '=')) { $lines[$i] = $line; return }
    }
    $lines.Add($line)
  }

  $Name = ${psq(serverName)}
  $Root = Join-Path $env:USERPROFILE 'Zomboid'
  $Dir = Join-Path $Root 'Server'
  $Ini = Join-Path $Dir ($Name + '.ini')
  $Sandbox = Join-Path $Dir ($Name + '_SandboxVars.lua')
  $Regions = Join-Path $Dir ($Name + '_spawnregions.lua')
  $Points = Join-Path $Dir ($Name + '_spawnpoints.lua')
  $HostIni = Join-Path $Root 'Lua\\host.ini'
  # The game's ini reader does not strip a BOM, so write UTF-8 without one.
  $Utf8 = New-Object System.Text.UTF8Encoding($false)

  $Overrides = [ordered]@{
${overrideLines}
  }
  $SandboxPatch = [ordered]@{
${sandboxPatch}
  }
  $SandboxNew = T '${b64(crlf(sandboxLua(sandbox)))}'
  $RegionsNew = T '${b64(crlf(SPAWN_REGIONS_LUA))}'
  $PointsNew = T '${b64(crlf(SPAWN_POINTS_LUA))}'
  $Mods = @(
${modNames}
  )

  Write-Host ''
  Say '${b64(M.title)}' 'Yellow'

  if (Get-Process -Name 'ProjectZomboid64', 'ProjectZomboid32' -ErrorAction SilentlyContinue) {
    Say '${b64(M.gameRunning)}' 'Red'
    return
  }

  New-Item -ItemType Directory -Force -Path $Dir | Out-Null
  Step '${b64(M.checkFolder)}'

  # Backup names must not end with .ini, or they show up in the Host server list.
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $backedUp = $false
  foreach ($f in @($Ini, $Sandbox, $Regions, $Points)) {
    if (Test-Path $f) { Copy-Item $f ($f + '.' + $stamp + '.bak'); $backedUp = $true }
  }
  if ($backedUp) { Step '${b64(M.backup)}' }

  $lines = New-Object System.Collections.Generic.List[string]
  if (Test-Path $Ini) { $lines.AddRange([string[]][IO.File]::ReadAllLines($Ini)) }
  if ($lines.Count -eq 0 -or -not $lines[0].StartsWith('#')) {
    $lines.Insert(0, '# ' + $Name + ' (written by Zomboid-multi installer; the game rewrites this file on server start)')
  }
  foreach ($k in $Overrides.Keys) { Set-IniKey $lines $k $Overrides[$k] }
  [IO.File]::WriteAllLines($Ini, $lines, $Utf8)
  Step '${b64(M.mods(list.length))}'
  foreach ($m in $Mods) { Write-Host ('      ' + (T $m)) -ForegroundColor DarkGray }

  if (Test-Path $Sandbox) {
    $text = [IO.File]::ReadAllText($Sandbox)
    foreach ($k in $SandboxPatch.Keys) {
      $text = [regex]::Replace($text, '(\\b' + [regex]::Escape($k) + '\\s*=\\s*)[^,\\r\\n]+', ('\${1}' + $SandboxPatch[$k]))
    }
    [IO.File]::WriteAllText($Sandbox, $text, $Utf8)
  } else {
    [IO.File]::WriteAllText($Sandbox, $SandboxNew, $Utf8)
  }
  Step '${b64(M.sandbox)}'

  if (-not (Test-Path $Regions)) { [IO.File]::WriteAllText($Regions, $RegionsNew, $Utf8) }
  if (-not (Test-Path $Points)) { [IO.File]::WriteAllText($Points, $PointsNew, $Utf8) }
  Step '${b64(M.spawn)}'

  if (Test-Path $HostIni) {
    $hl = New-Object System.Collections.Generic.List[string]
    $hl.AddRange([string[]][IO.File]::ReadAllLines($HostIni))
    Set-IniKey $hl 'servername' $Name
    [IO.File]::WriteAllLines($HostIni, $hl, $Utf8)
    Step '${b64(M.preselect)}'
  }

  Write-Host ''
  Say '${b64(M.done)}' 'Green'
  Say '${b64(M.next(serverName))}' 'White'
  Write-Host ('  ' + $Dir) -ForegroundColor DarkGray
  Write-Host ''
}

try {
  Install-ZomboidMulti
} catch {
  Write-Host ''
  Write-Host ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('${b64(M.fail)}'))) -ForegroundColor Red
  Write-Host $_ -ForegroundColor Red
}
`;
  // Windows PowerShell 은 LF 만 있어도 읽지만, 메모장으로 열어 볼 친구를 위해 CRLF 로 낸다.
  return crlf(script);
}
