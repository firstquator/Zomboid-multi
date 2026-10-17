import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { validateMods } from "../src/lib/mods-schema.mjs";
import { fixtureData } from "./fixtures.mjs";

describe("validateMods", () => {
  it("올바른 데이터는 통과한다", () => {
    expect(validateMods(fixtureData())).toEqual({ ok: true });
  });

  it("의존 모드가 목록에 없으면 막는다", () => {
    const d = fixtureData();
    d.mods = d.mods.filter((m) => m.workshopId !== "2000000001");
    const r = validateMods(d);
    expect(r.ok).toBe(false);
    expect(r.errors.join("\n")).toContain("2000000001 가 목록에 없습니다");
  });

  it("의존 모드가 쓰는 쪽보다 늦게 불리면 막는다", () => {
    const d = fixtureData();
    d.mods.find((m) => m.workshopId === "2000000001").loadOrder = 9;
    expect(validateMods(d).errors.join("\n")).toContain("loadOrder 가 더 앞서야");
  });

  it("Mod ID 에 세미콜론이나 역슬래시가 있으면 막는다", () => {
    const d = fixtureData();
    d.mods[0].modIds = ["A;B"];
    d.mods[1].modIds = ["\\C"];
    const msg = validateMods(d).errors.join("\n");
    expect(msg).toContain("A;B");
    expect(msg).toContain("\\\\C");
  });

  it("B42 확인이 안 된 모드는 막는다", () => {
    const d = fixtureData();
    d.mods[2].b42.supported = false;
    expect(validateMods(d).ok).toBe(false);
  });

  it("변경 이력은 최신순이어야 한다", () => {
    const d = fixtureData();
    d.modpack.changes = [
      { date: "2026-10-01", summary: "a", mustUpdate: false },
      { date: "2026-10-18", summary: "b", mustUpdate: false },
    ];
    expect(validateMods(d).errors.join("\n")).toContain("최신순");
  });

  it("실제 data/mods.json 도 통과한다", () => {
    const real = JSON.parse(readFileSync(new URL("../../data/mods.json", import.meta.url), "utf8"));
    expect(validateMods(real).errors ?? []).toEqual([]);
  });
});
