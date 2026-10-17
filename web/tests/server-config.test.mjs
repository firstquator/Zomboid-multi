import { describe, it, expect } from "vitest";
import { workshopItems, modIds, manualLines, iniOverrides } from "../src/lib/server-config.mjs";
import { fixtureMods } from "./fixtures.mjs";

describe("server-config", () => {
  it("WorkshopItems 는 loadOrder 순으로 잇는다 (원본 배열 순서와 무관)", () => {
    expect(workshopItems(fixtureMods)).toBe("2000000001;2000000002;2000000003");
  });

  it("Mods 는 게임이 쓰는 형식대로 접두 없이 잇고, ID 가 여럿이면 전부 넣는다", () => {
    expect(modIds(fixtureMods)).toBe("CoreLib;UsesLib;TwoA;TwoB");
  });

  it("수동 설정용 두 줄은 키=값 형식이다", () => {
    const [ws, m] = manualLines(fixtureMods);
    expect(ws).toBe("WorkshopItems=2000000001;2000000002;2000000003");
    expect(m).toBe("Mods=CoreLib;UsesLib;TwoA;TwoB");
  });

  it("공개 목록에 올리지 않고 PvP 를 끈다", () => {
    const o = iniOverrides(fixtureMods);
    expect(o.Public).toBe("false");
    expect(o.PVP).toBe("false");
  });

  it("값 안에 = 가 없다 (게임 ini 파서는 = 로 잘라서 값이 잘린다)", () => {
    for (const v of Object.values(iniOverrides(fixtureMods))) expect(v.includes("=")).toBe(false);
  });
});
