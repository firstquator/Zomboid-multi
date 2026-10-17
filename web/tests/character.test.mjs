import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { builds, buildGroups, verdicts, communityBuilds, sourceKinds } from "../src/data/builds.mjs";
import { remainingPoints, conflicts, skillTotals, encodeBuild, decodeBuild, SLEEP_TRAITS } from "../src/lib/character.mjs";

const data = JSON.parse(readFileSync(new URL("../src/data/character.json", import.meta.url), "utf8"));
const prof = (id) => data.professions.find((p) => p.id === id);
const trait = (id) => data.traits.find((t) => t.id === id);

describe("추천 조합", () => {
  for (const b of builds) {
    describe(b.title, () => {
      const p = prof(b.profession);
      const ts = [...b.good, ...b.bad].map(trait);

      it("직업과 특성이 모두 게임 데이터에 있다", () => {
        expect(p).toBeTruthy();
        expect(ts.every(Boolean)).toBe(true);
      });

      it("긍정은 비용이 양수, 부정은 음수인 특성만 넣었다", () => {
        expect(b.good.every((id) => trait(id).cost > 0)).toBe(true);
        expect(b.bad.every((id) => trait(id).cost < 0)).toBe(true);
      });

      it("포인트가 모자라지 않는다", () => {
        expect(remainingPoints(p, ts)).toBeGreaterThanOrEqual(0);
      });

      it("함께 못 고르는 특성이 없다 (직업이 주는 특성 포함)", () => {
        expect(conflicts(p, ts)).toEqual([]);
      });

      it("우리 서버에서 고를 수 없는 수면 특성을 넣지 않았다", () => {
        expect(ts.some((t) => SLEEP_TRAITS.includes(t.id))).toBe(false);
      });
    });
  }
});

describe("추천 조합 목록", () => {
  it("id 가 겹치지 않고, 모두 정해진 갈래에 속한다", () => {
    const ids = builds.map((b) => b.id);
    expect(new Set(ids).size).toBe(ids.length);
    const groups = new Set(buildGroups.map((g) => g.id));
    expect(builds.filter((b) => !groups.has(b.group)).map((b) => b.id)).toEqual([]);
  });

  it("같은 조합(직업과 특성이 모두 같은 것)이 두 번 들어가지 않는다", () => {
    const keys = builds.map((b) => [b.profession, ...[...b.good, ...b.bad].sort()].join("."));
    expect(new Set(keys).size).toBe(keys.length);
  });
});

describe("커뮤니티 추천 조합", () => {
  for (const b of communityBuilds) {
    describe(b.title, () => {
      const p = prof(b.profession);
      const ts = [...b.good, ...b.bad].map(trait);

      it("직업과 특성이 모두 게임 데이터에 있고, 긍정·부정이 맞게 나뉘었다", () => {
        expect(p).toBeTruthy();
        expect(ts.every(Boolean)).toBe(true);
        expect(b.good.every((id) => trait(id).cost > 0)).toBe(true);
        expect(b.bad.every((id) => trait(id).cost < 0)).toBe(true);
      });

      it("우리 서버에서 그대로 만들 수 있다 (포인트, 상호 배제, 수면 특성)", () => {
        expect(remainingPoints(p, ts)).toBeGreaterThanOrEqual(0);
        expect(conflicts(p, ts)).toEqual([]);
        expect(ts.some((t) => SLEEP_TRAITS.includes(t.id))).toBe(false);
      });

      it("출처 링크와 종류가 있다", () => {
        expect(b.source.url).toMatch(/^https:\/\//);
        expect(sourceKinds[b.source.kind]).toBeTruthy();
        expect(b.source.name && b.source.title && b.source.version).toBeTruthy();
      });

      if (b.original) {
        it("바꾼 조합은 원래 조합(수면 특성 포함)과 바꾼 이유를 적었다", () => {
          const orig = [...b.original.good, ...b.original.bad];
          expect(orig.every((id) => trait(id))).toBe(true);
          expect(orig.some((id) => SLEEP_TRAITS.includes(id))).toBe(true);
          expect(b.changed).toBeTruthy();
          // 원래 글의 조합도 42.21 수치로 만들 수 있던 조합이다
          expect(remainingPoints(p, orig.map(trait))).toBeGreaterThanOrEqual(0);
        });
      } else {
        it("원래 조합 그대로라면 바꾼 내용이 없다", () => {
          expect(b.changed).toBeUndefined();
        });
      }
    });
  }

  it("id 가 겹치지 않고 우리 추천 조합 id 와도 겹치지 않는다", () => {
    const ids = [...builds, ...communityBuilds].map((b) => b.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("특성 평가", () => {
  it("평가에 적은 id 는 모두 게임 데이터에 있다", () => {
    expect(Object.keys(verdicts).filter((id) => !trait(id))).toEqual([]);
  });

  it("수면 특성은 고를 수 없음(off)으로 표시한다", () => {
    for (const id of SLEEP_TRAITS) expect(verdicts[id]?.tag).toBe("off");
  });
});

describe("계산 규칙", () => {
  it("남은 포인트 = 직업 포인트 − 특성 비용 합", () => {
    expect(remainingPoints({ cost: 8 }, [{ cost: 10 }, { cost: -4 }])).toBe(2);
  });

  it("직업이 주는 특성과 부딪히는 특성을 찾는다", () => {
    const p = { granted: ["cook2"] };
    expect(conflicts(p, [{ id: "cook", exclusive: ["cook2"] }])).toEqual([["cook", "cook2"]]);
  });

  it("같은 기술 보너스는 더한다", () => {
    const t = skillTotals({ xp: [{ skill: "Fitness", name: "체력", level: 1 }] }, [{ xp: [{ skill: "Fitness", name: "체력", level: 2 }] }]);
    expect(t).toEqual([{ skill: "Fitness", name: "체력", level: 3 }]);
  });

  it("조합 링크를 만들고 다시 읽는다", () => {
    const h = encodeBuild("fireofficer", ["thickskinned", "keenhearing"]);
    expect(decodeBuild(`#${h}`)).toEqual({ professionId: "fireofficer", traitIds: ["thickskinned", "keenhearing"] });
    expect(decodeBuild("#step-1")).toBe(null);
  });
});
