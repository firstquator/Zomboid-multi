import { describe, it, expect } from "vitest";
import { readFileSync, existsSync, readdirSync } from "node:fs";

// scripts/extract-items.py 가 게임 파일에서 뽑은 아이템 도감 데이터를 점검한다.
const read = (path) => JSON.parse(readFileSync(new URL(path, import.meta.url), "utf8"));
const index = read("../public/data/items-index.json");
const detail = read("../public/data/items-detail.json");
const items = Object.values(detail.items);
const item = (id) => detail.items[id];
const recipe = (id) => detail.recipes[id];
const publicFile = (rel) => new URL(`../public/${rel}`, import.meta.url);
const hangul = /[가-힣]/;

// 제작법 재료 한 칸에 들어갈 수 있는 도감 아이템 (직접 적힌 것 + 태그로 받는 것)
const slotItems = (slot) => {
  const ids = new Set((slot.items ?? []).filter((id) => detail.items[id]));
  for (const tag of slot.tags ?? []) for (const id of detail.tagItems[tag] ?? []) ids.add(id);
  return ids;
};

describe("아이템 목록", () => {
  it("검색용 목록과 상세 데이터가 같은 아이템을 담는다", () => {
    const a = index.items.map((x) => x.id).sort();
    const b = Object.keys(detail.items).sort();
    expect(a).toEqual(b);
    expect(a.length).toBeGreaterThan(4000);
  });

  it("id 가 겹치지 않고 Base.이름 형식이다", () => {
    const ids = index.items.map((x) => x.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ids.filter((id) => !/^Base\.[A-Za-z0-9_]+$/.test(id))).toEqual([]);
  });

  it("모든 아이템에 이름과 영문 이름이 있고, 거의 모두 한국어 이름이다", () => {
    expect(items.filter((x) => !x.name?.trim() || !x.nameEn?.trim()).map((x) => x.id)).toEqual([]);
    const notKorean = items.filter((x) => !hangul.test(x.name));
    expect(notKorean.length).toBeLessThanOrEqual(5);
  });

  it("분류는 원래 키와 한국어 이름을 함께 갖고, 검색용 분류 표와 맞는다", () => {
    for (const x of items) {
      expect(x.category.key, x.id).toBeTruthy();
      expect(index.categories[x.category.key], x.id).toBe(x.category.name);
    }
  });

  it("무게는 0 이상의 숫자이고, 요약이 비어 있지 않다", () => {
    expect(items.filter((x) => typeof x.weight !== "number" || x.weight < 0).map((x) => x.id)).toEqual([]);
    expect(index.items.filter((x) => !x.summary?.trim()).map((x) => x.id)).toEqual([]);
  });

  it("빼기로 한 아이템(가구 타일, 숨김, 상처·좀비 피해 표시, 디버그·테스트용)이 없다", () => {
    const bad = items.filter(
      (x) =>
        /^Base\.(Mov_|ZedDmg_|Wound_|MakeUp_)/.test(x.id) ||
        /debug|^Base\.Test/i.test(x.id) ||
        ["Furniture", "Hidden", "ZedDmg", "Wound"].includes(x.category.key) ||
        x.type === "animal",
    );
    expect(bad.map((x) => x.id)).toEqual([]);
  });

  it("들고 다니며 쓰는 Moveable(생가죽·텐트·침낭)은 남아 있다", () => {
    for (const id of ["Base.CowHide", "Base.TentGreen", "Base.SleepingBag_Green"]) expect(item(id), id).toBeTruthy();
  });
});

describe("아이콘", () => {
  it("아이콘 경로가 가리키는 파일이 실제로 있다", () => {
    const icons = new Set(items.map((x) => x.icon).filter(Boolean));
    const missing = [...icons].filter((rel) => !existsSync(publicFile(rel)));
    expect(missing).toEqual([]);
  });

  it("아이콘이 없는 아이템은 손꼽을 만큼만 있다", () => {
    expect(items.filter((x) => !x.icon).length).toBeLessThanOrEqual(10);
  });

  it("같은 그림을 쓰는 아이템은 파일 하나를 함께 쓰고, 쓰지 않는 파일은 남기지 않는다", () => {
    const used = new Set(items.map((x) => x.icon).filter(Boolean).map((rel) => rel.split("/").pop()));
    const files = readdirSync(publicFile("icons/item")).filter((f) => f.endsWith(".webp"));
    expect(used.size).toBeLessThan(items.length);
    expect(files.sort()).toEqual([...used].sort());
  });

  it("아이콘 파일 이름은 대소문자만 다른 것이 없다 (GitHub Pages 는 대소문자를 가린다)", () => {
    const files = readdirSync(publicFile("icons/item"));
    expect(new Set(files.map((f) => f.toLowerCase())).size).toBe(files.length);
  });
});

describe("대표 아이템", () => {
  const cases = [
    ["Base.Hammer", "망치"],
    ["Base.Bandage", "붕대"],
    ["Base.PetrolCan", "기름통"],
    ["Base.CarKey", "차 열쇠"],
    ["Base.TinnedBeans", "콩 통조림"],
    ["Base.Axe", "소방도끼"],
    ["Base.Saw", "줄톱"],
    ["Base.Nails", "못"],
  ];
  for (const [id, name] of cases) {
    it(`${name}(${id})이 들어 있고 아이콘이 있다`, () => {
      expect(item(id)?.name).toBe(name);
      expect(item(id).icon).toMatch(/^icons\/item\/.+\.webp$/);
    });
  }

  it("망치는 짧은 둔기이고, 망치 태그로 건축과 제작에 도구로 쓰인다", () => {
    const h = item("Base.Hammer");
    expect(h.weapon.skill).toBe("SmallBlunt");
    expect(h.weapon.skillName).toBe("짧은 둔기");
    expect(h.roles.map((r) => r.name)).toContain("망치");
    expect(h.recipes.tool).toContain("WoodenWallLvl1");
    expect(recipe("WoodenWallLvl1").kind).toBe("build");
  });

  it("붕대는 상처를 감는 데 쓰고, 쓰면 더러운 붕대가 된다", () => {
    const b = item("Base.Bandage");
    expect(b.medical.bandage).toBeGreaterThan(0);
    expect(b.becomes.id).toBe("Base.BandageDirty");
  });

  it("콩 통조림은 따서 먹으며, 따는 제작법의 재료다", () => {
    const c = item("Base.TinnedBeans");
    expect(c.food.mustOpen).toBe(true);
    expect(c.recipes.uses).toContain("OpenCannedFood");
    expect(recipe("OpenCannedFood").outputs[0].items).toContain("Base.OpenBeans");
  });

  it("기름통에는 휘발유가 든다", () => {
    expect(item("Base.PetrolCan").fluid.contents.map((f) => f.id)).toContain("Petrol");
  });

  it("목공 1권은 목공 1~2레벨 책이다", () => {
    expect(item("Base.BookCarpentry1").book).toMatchObject({ skill: "Woodwork", skillName: "목공", levels: [1, 2] });
  });

  it("권총은 탄약 종류와 장탄 수를 알려 준다", () => {
    const w = item("Base.Pistol").weapon;
    expect(w.firearm).toBe(true);
    expect(w.ammo.id).toBe("Base.Bullets9mm");
    expect(w.capacity).toBeGreaterThan(0);
  });

  it("가방은 용량과 무게 감소를 알려 준다", () => {
    expect(item("Base.Bag_ALICEpack_Army").bag).toMatchObject({ capacity: 28, weightReduction: 85 });
  });
});

describe("제작법 연결", () => {
  const kinds = ["made", "uses", "tool", "teaches", "research"];

  it("아이템이 가리키는 제작법은 모두 있다", () => {
    const missing = [];
    for (const x of items) for (const k of kinds) for (const rid of x.recipes?.[k] ?? []) if (!recipe(rid)) missing.push(`${x.id}:${rid}`);
    expect(missing).toEqual([]);
  });

  it("아이템 → 제작법: 그 제작법의 해당 칸에 실제로 그 아이템이 들어간다", () => {
    const wrong = [];
    for (const x of items) {
      const r = x.recipes ?? {};
      for (const rid of r.made ?? []) if (!recipe(rid).outputs.some((o) => o.items?.includes(x.id))) wrong.push(`made ${x.id} ${rid}`);
      for (const rid of r.uses ?? [])
        if (!recipe(rid).inputs.some((s) => !s.keep && slotItems(s).has(x.id))) wrong.push(`uses ${x.id} ${rid}`);
      for (const rid of r.tool ?? [])
        if (!recipe(rid).inputs.some((s) => s.keep && slotItems(s).has(x.id))) wrong.push(`tool ${x.id} ${rid}`);
      for (const rid of r.teaches ?? []) if (!recipe(rid).taughtBy?.includes(x.id)) wrong.push(`teaches ${x.id} ${rid}`);
      for (const rid of r.research ?? []) if (!recipe(rid).researchFrom?.includes(x.id)) wrong.push(`research ${x.id} ${rid}`);
    }
    expect(wrong).toEqual([]);
  });

  it("제작법 → 아이템: 재료·도구·결과에 든 도감 아이템은 그 제작법을 목록에 갖고 있다", () => {
    const wrong = [];
    for (const [rid, r] of Object.entries(detail.recipes)) {
      for (const s of r.inputs)
        for (const id of slotItems(s)) if (!item(id).recipes?.[s.keep ? "tool" : "uses"]?.includes(rid)) wrong.push(`${rid} ${id}`);
      for (const o of r.outputs)
        for (const id of o.items ?? []) if (item(id) && !item(id).recipes?.made?.includes(rid)) wrong.push(`${rid} → ${id}`);
      for (const id of r.taughtBy ?? []) if (!item(id)?.recipes?.teaches?.includes(rid)) wrong.push(`${rid} taughtBy ${id}`);
      for (const id of r.researchFrom ?? []) if (!item(id)?.recipes?.research?.includes(rid)) wrong.push(`${rid} researchFrom ${id}`);
    }
    expect(wrong).toEqual([]);
  });

  it("태그 재료의 아이템 목록에는 실제로 그 태그를 가진 아이템만 있다", () => {
    const wrong = [];
    for (const [tag, ids] of Object.entries(detail.tagItems)) for (const id of ids) if (!item(id)?.tags.includes(tag)) wrong.push(`${tag} ${id}`);
    expect(wrong).toEqual([]);
    expect(detail.tagItems["base:hammer"]).toContain("Base.Hammer");
  });

  it("제작법마다 한국어 이름과 분류 이름이 있다", () => {
    const recipes = Object.entries(detail.recipes);
    expect(recipes.length).toBeGreaterThan(1000);
    expect(recipes.filter(([, r]) => !hangul.test(r.name)).map(([id]) => id)).toEqual([]);
    expect(recipes.filter(([, r]) => r.category && !r.categoryName).map(([id]) => id)).toEqual([]);
  });

  it("기술 조건에는 기술 이름과 레벨이 있다", () => {
    for (const r of Object.values(detail.recipes))
      for (const s of [...r.skills, ...r.autoLearn]) {
        expect(detail.skills[s.skill], s.skill).toBe(s.name);
        expect(s.level).toBeGreaterThanOrEqual(0);
      }
  });
});

describe("나오는 곳", () => {
  it("나오는 곳마다 표시 이름이 있고, 거의 모두 한국어로 옮겼다", () => {
    const keys = new Set(items.flatMap((x) => (x.loot ?? []).map(([k]) => k)));
    expect([...keys].filter((k) => !detail.places[k])).toEqual([]);
    const korean = [...keys].filter((k) => hangul.test(detail.places[k]));
    expect(korean.length / keys.size).toBeGreaterThan(0.95);
  });

  it("확률은 0 초과 100 이하이고, 6곳까지만 둔다", () => {
    for (const x of items) {
      expect((x.loot ?? []).length).toBeLessThanOrEqual(6);
      for (const [, p] of x.loot ?? []) {
        expect(p).toBeGreaterThan(0);
        expect(p).toBeLessThanOrEqual(100);
      }
      if (x.loot) expect(x.lootCount).toBeGreaterThanOrEqual(x.loot.length);
    }
  });

  it("대표 아이템은 나오는 곳이 있다", () => {
    for (const id of ["Base.Hammer", "Base.Bandage", "Base.TinnedBeans", "Base.PetrolCan", "Base.CarKey", "Base.Axe"])
      expect(item(id).loot?.length, id).toBeGreaterThan(0);
  });

  it("잔가지처럼 채집으로 얻는 것은 채집 구역이 있다", () => {
    const f = item("Base.Twigs").forage;
    expect(f.zones.map((z) => z.zone)).toContain("Forest");
    expect(f.zones.every((z) => z.name)).toBe(true);
  });
});
