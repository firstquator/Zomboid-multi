import { describe, it, expect } from "vitest";
import { existsSync } from "node:fs";
import { keybinds, keyGroups, essentials, inventoryMoves, keyboardRows } from "../src/data/keys.mjs";
import { startSteps, radial, fuelWays, powerCut, mechParts, toolNames, mechBooks, driveNotes, dashboardSpots } from "../src/data/vehicles.mjs";
import { controlTips, tipTopics } from "../src/data/tips.mjs";

const guide = (p) => new URL(`../public/guide/${p}.webp`, import.meta.url);
const missing = (paths) => paths.filter((p) => !existsSync(guide(p)));

describe("단축키", () => {
  it("모든 키가 정해진 갈래에 속하고 이름이 있다", () => {
    const groups = new Set(keyGroups.map((g) => g.id));
    expect(keybinds.filter((b) => !groups.has(b.group) || !b.name || !b.keys.length)).toEqual([]);
  });

  it("먼저 외울 키와 조작 팁의 키는 단축키 목록에 있는 키다", () => {
    const known = new Set(keybinds.flatMap((b) => b.keys));
    const used = [...essentials, ...controlTips].flatMap((e) => e.keys);
    expect(used.filter((k) => !known.has(k))).toEqual([]);
  });

  it("키보드 그림에 없는 키는 마우스·모드 키뿐이다", () => {
    const board = new Set(keyboardRows.flat().map((c) => c.k).filter(Boolean));
    const off = new Set(keybinds.flatMap((b) => b.keys).filter((k) => !board.has(k)));
    expect([...off].sort()).toEqual(["LMB", "RMB", "Wheel"].sort());
  });

  it("소지품 창 동작에 설명이 있다", () => {
    expect(inventoryMoves.every((m) => m.title && m.text && m.keys.length)).toBe(true);
  });
});

describe("차량", () => {
  it("쓰는 그림이 모두 있다", () => {
    const paths = [
      ...startSteps.map((s) => s.icon),
      ...radial.inside.map((r) => r.icon),
      ...radial.outside.map((r) => r.icon),
      ...fuelWays.flatMap((f) => f.icons),
      ...powerCut.icons,
      ...mechBooks.map((b) => b.icon),
      ...driveNotes.map((d) => d.icon),
      "vehicle/cardashboard",
      "vehicle/carradialmenu",
      "mech/4door_base",
    ];
    expect(missing(paths)).toEqual([]);
  });

  it("정비 부품의 마스크와 도구 그림이 있고 도구 이름이 있다", () => {
    expect(missing(mechParts.flatMap((p) => p.masks.map((m) => `mech/4door_${m}`)))).toEqual([]);
    expect(missing(mechParts.flatMap((p) => p.tools.map((t) => `item/${t}`)))).toEqual([]);
    expect(mechParts.flatMap((p) => p.tools).filter((t) => !toolNames[t])).toEqual([]);
  });

  it("계기판 표시 위치가 그림 안에 있다", () => {
    expect(dashboardSpots.every((s) => s.x > 0 && s.x < 100 && s.y > 0 && s.y < 100)).toBe(true);
  });
});

describe("생활 꿀팁", () => {
  it("주제마다 그림과 팁이 있고 팁 그림이 모두 있다", () => {
    expect(missing(tipTopics.map((t) => `spiffo/${t.spiffo}`))).toEqual([]);
    expect(tipTopics.every((t) => t.tips.length >= 4 && t.tips.every((x) => x.title && x.text))).toBe(true);
    expect(missing(tipTopics.flatMap((t) => t.tips.flatMap((x) => x.icons ?? [])))).toEqual([]);
  });
});
