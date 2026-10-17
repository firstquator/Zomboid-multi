// 테스트용 작은 모드팩. 실제 mods.json 과 모양만 같다.
const mod = (o) => ({
  name: "Mod",
  nameKo: "모드",
  category: "ui",
  summary: "s",
  why: "w",
  korean: { status: "native", note: "" },
  b42: { supported: true, lastUpdated: "2026-09-01", tags: ["Build 42"], note: "" },
  dependsOn: [],
  thumbnail: "",
  sandbox: [],
  url: `https://steamcommunity.com/sharedfiles/filedetails/?id=${o.workshopId}`,
  ...o,
});

export const fixtureMods = [
  mod({ workshopId: "2000000002", modIds: ["UsesLib"], name: "Uses Lib", dependsOn: ["2000000001"], loadOrder: 2 }),
  mod({ workshopId: "2000000001", modIds: ["CoreLib"], name: "Core Lib", category: "lib", loadOrder: 1 }),
  mod({ workshopId: "2000000003", modIds: ["TwoA", "TwoB"], name: "Two Ids", category: "korean", loadOrder: 3 }),
];

export const fixtureData = () => ({
  schemaVersion: 1,
  game: { build: "42.21.0", branch: "public", checkedAt: "2026-10-18" },
  modpack: { version: "v1", changes: [{ date: "2026-10-18", summary: "첫 모드팩", mustUpdate: true }] },
  categories: [
    { id: "lib", label: "필수 라이브러리" },
    { id: "ui", label: "화면" },
    { id: "korean", label: "한국어" },
  ],
  mods: structuredClone(fixtureMods),
  vanilla: [],
});
