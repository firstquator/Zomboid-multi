// 사이트 전체가 함께 쓰는 값. mods.json 에서 한 번만 꺼내 정리한다.
// 화면 곳곳에 같은 숫자(모드 개수, 빌드 번호)가 나오는데, 각자 따로 세면
// 어느 날 서로 다른 값을 보여 주게 된다.
import data from "../../../data/mods.json" with { type: "json" };

export const SITE_ORIGIN = "https://firstquator.github.io";
export const SITE_BASE = "/Zomboid-multi";
export const SITE_URL = `${SITE_ORIGIN}${SITE_BASE}/`;
export const REPO_URL = "https://github.com/firstquator/Zomboid-multi";

// 게임 Host 화면에 이 이름으로 설정이 나타난다. 파일 이름에도 그대로 쓰인다.
export const SERVER_NAME = "zomboid-multi";

export const INSTALL_URL = `${SITE_URL}install.ps1`;
export const INSTALL_COMMAND = `irm ${INSTALL_URL} | iex`;

const mods = [...data.mods].sort((a, b) => a.loadOrder - b.loadOrder);

export const site = {
  build: data.game.build,
  branch: data.game.branch,
  checkedAt: data.game.checkedAt,
  modpackVersion: data.modpack.version,
  changes: data.modpack.changes ?? [],
  modCount: mods.length,
  koreanCount: mods.filter((m) => m.korean?.status !== "none").length,
};

export { mods };
export const categories = data.categories;
export const vanilla = data.vanilla ?? [];

/** 카테고리 id 로 사람이 읽는 이름을 찾는다. 없으면 id 를 그대로 쓴다. */
export const categoryLabel = (id) => categories.find((c) => c.id === id)?.label ?? id;

/** workshopId 로 모드를 찾는다. 의존 관계를 이름으로 보여 줄 때 쓴다. */
export const modById = (workshopId) => mods.find((m) => m.workshopId === workshopId);
