import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { buildInstaller, demoLines, sandboxLua, MESSAGES, SPAWN_REGIONS_LUA } from "../src/lib/installer.mjs";
import { fixtureMods } from "./fixtures.mjs";

const make = (over = {}) =>
  buildInstaller({
    mods: fixtureMods,
    serverName: "zomboid-multi",
    siteUrl: "https://example.com/",
    repoUrl: "https://github.com/x/y",
    modpackVersion: "v1",
    sandbox: [
      { key: "Map.AllowMiniMap", value: "true" },
      { key: "MinutesPerPage", value: "0.1" },
    ],
    ini: [{ key: "MapRemotePlayerVisibility", value: "4" }],
    ...over,
  });
const script = make();

// 스크립트 안의 Base64 문자열을 전부 풀어 본다.
const decoded = (s) =>
  [...s.matchAll(/'([A-Za-z0-9+/]{8,}={0,2})'/g)].map((m) => Buffer.from(m[1], "base64").toString("utf8"));
const nonAscii = (s) => [...s].filter((c) => c.charCodeAt(0) > 0x7e);

describe("installer", () => {
  it("스크립트 본문은 ASCII 로만 되어 있다 (irm 이 인코딩을 잘못 읽어도 깨지지 않게)", () => {
    expect(nonAscii(script)).toEqual([]);
  });

  it("실제 data/mods.json 으로 만든 스크립트도 ASCII 로만 되어 있다", () => {
    const real = JSON.parse(readFileSync(new URL("../../data/mods.json", import.meta.url), "utf8"));
    const pick = (f) => real.vanilla.filter((v) => v.file === f).map(({ key, value }) => ({ key, value }));
    expect(nonAscii(make({ mods: real.mods, sandbox: pick("sandbox"), ini: pick("ini") }))).toEqual([]);
  });

  it("줄바꿈은 CRLF 다", () => {
    expect(script.includes("\r\n")).toBe(true);
    expect(/[^\r]\n/.test(script)).toBe(false);
  });

  it("모든 모드의 Workshop ID 와 Mod ID 가 들어간다", () => {
    for (const m of fixtureMods) {
      expect(script).toContain(m.workshopId);
      for (const id of m.modIds) expect(script).toContain(id);
    }
  });

  it("한글 안내문과 모드 원제는 Base64 로 들어 있고 풀면 원래 문구가 나온다", () => {
    const s = make({ mods: [{ ...fixtureMods[1], name: "Hx's 좀보이드 통합 번역" }] });
    const texts = decoded(s);
    expect(texts).toContain(MESSAGES.title);
    expect(texts).toContain(MESSAGES.next("zomboid-multi"));
    expect(texts).toContain("2000000001  Hx's 좀보이드 통합 번역");
  });

  it("지도 플레이어 표시 같은 추가 ini 값도 넣는다", () => {
    expect(script).toContain("'MapRemotePlayerVisibility' = '4'");
  });

  it("맨 위 샌드박스 값(MinutesPerPage)은 기존 파일을 고칠 때도 이름으로 찾는다", () => {
    expect(script).toContain("'MinutesPerPage' = '0.1'");
  });

  it("게임이 켜져 있으면 멈춘다 (서버가 시작할 때 파일을 다시 쓰므로)", () => {
    expect(script).toContain("Get-Process -Name 'ProjectZomboid64'");
  });

  it("비밀번호를 묻지 않는다 (서버 만들기로 연 서버는 Password 를 무시한다)", () => {
    expect(script.includes("Read-Host")).toBe(false);
  });

  it("백업 파일 이름은 .ini 로 끝나지 않는다 (끝나면 서버 이름 목록에 같이 뜬다)", () => {
    expect(script).toContain("($f + '.' + $stamp + '.bak')");
  });

  it("BOM 없는 UTF-8 로 쓴다 (게임 ini 파서는 BOM 을 지우지 않는다)", () => {
    expect(script).toContain("New-Object System.Text.UTF8Encoding($false)");
    expect(script.includes("-Encoding UTF8")).toBe(false);
  });

  it("창을 닫아 버리는 exit 를 쓰지 않는다 (iex 로 돌면 PowerShell 창이 꺼진다)", () => {
    expect(/\bexit\b/i.test(script.replace(/^#.*$/gm, ""))).toBe(false);
  });

  it("기존 샌드박스 값 치환은 정규식 그룹 참조(${1})를 쓴다", () => {
    expect(script).toContain("('${1}' + $SandboxPatch[$k])");
  });

  it("터미널 연출은 실제 스크립트와 같은 문구를 쓴다", () => {
    const lines = demoLines({ modCount: 3, serverName: "zomboid-multi" }).map((l) => l.text.trim());
    expect(lines).toContain(MESSAGES.title);
    expect(lines).toContain(MESSAGES.mods(3));
  });
});

describe("sandboxLua", () => {
  it("VERSION, 맨 위 값, 묶음별 표 순서로 만든다", () => {
    const lua = sandboxLua([
      { key: "MinutesPerPage", value: "0.1" },
      { key: "Map.AllowMiniMap", value: "true" },
      { key: "Map.AllowWorldMap", value: "true" },
      { key: "ZombieLore.Speed", value: "2" },
    ]);
    expect(lua).toBe(
      [
        "SandboxVars = {",
        "    VERSION = 6,",
        "    MinutesPerPage = 0.1,",
        "    Map = {",
        "        AllowMiniMap = true,",
        "        AllowWorldMap = true,",
        "    },",
        "    ZombieLore = {",
        "        Speed = 2,",
        "    },",
        "}",
        "",
      ].join("\n"),
    );
  });

  it("문법이 깨질 수 있는 키와 값은 빌드를 멈춘다 (서버가 즉시 꺼지므로)", () => {
    expect(() => sandboxLua([{ key: "Map.Allow.MiniMap", value: "true" }])).toThrow();
    expect(() => sandboxLua([{ key: "Map.Allow MiniMap", value: "true" }])).toThrow();
    expect(() => sandboxLua([{ key: "Map.AllowMiniMap", value: "yes" }])).toThrow();
    expect(() => sandboxLua([{ key: "Map.AllowMiniMap", value: "true}" }])).toThrow();
  });
});

describe("spawnregions", () => {
  it("42.21 이 만드는 11개 도시를 모두 담는다", () => {
    expect((SPAWN_REGIONS_LUA.match(/name = "/g) ?? []).length).toBe(11);
    expect(SPAWN_REGIONS_LUA).toContain('{ name = "Muldraugh, KY", file = "media/maps/Muldraugh, KY/spawnpoints.lua" },');
  });
});
