// 실제 화면 사진 목록(src/data/shots.json)을 읽는다.
//
// 이 파일은 사진을 모으는 대로 채워지므로 아직 없을 수 있다. 정적 import 로
// 읽으면 파일이 없을 때 빌드가 깨지니 glob 으로 있으면 읽고 없으면 빈 목록을 쓴다.
const found = import.meta.glob("../data/shots.json", { eager: true, import: "default" });
const data = Object.values(found)[0] ?? { shots: [] };

export const shots = data.shots ?? [];

/** id 로 사진을 찾는다. 없으면 undefined. */
export const findShot = (id) => shots.find((s) => s.id === id);
