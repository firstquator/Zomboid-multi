// 창작마당 실물과 data/mods.json 을 대조한다.
//
//   node scripts/verify-workshop.mjs
//
// 모드는 며칠 단위로 바뀐다. 제작자가 새 의존 모드를 추가하거나 B42 태그를
// 떼거나 아이템을 내리면, mods.json 은 그대로인데 서버는 시작하지 못한다.
// 이 스크립트가 그 어긋남을 잡는다. 오류가 있으면 종료 코드 1 로 끝난다.
//
// 확인하는 것
// 1. 아이템이 아직 공개 상태인지
// 2. "Build 42" 태그가 붙어 있는지
// 3. 워크숍 페이지의 Required items 가 전부 mods.json 에 들어 있는지
// 4. 설명문의 Mod ID 줄에 우리가 쓴 Mod ID 가 있는지 (경고만)

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const DETAILS_API = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/";
const PAGE = (id) => `https://steamcommunity.com/sharedfiles/filedetails/?id=${id}`;

/** 워크숍 페이지 HTML 에서 Required items 의 아이템 번호와 이름을 뽑는다. */
export function parseRequiredItems(html) {
  const out = [];
  const re = /filedetails\/\?id=(\d+)"[^>]*>\s*<div class="requiredItem">\s*([^<]*?)\s*<\/div>/g;
  for (const m of html.matchAll(re)) out.push({ id: m[1], name: m[2] });
  return out;
}

/** 설명문에서 "Mod ID: xxx" 줄을 모두 뽑는다. BBCode 태그 앞에서 끊는다. */
export function parseModIds(description) {
  const out = [];
  for (const m of String(description ?? "").matchAll(/Mod\s*ID\s*:\s*([^\r\n\[<]+)/gi)) {
    const id = m[1].trim();
    if (id) out.push(id);
  }
  return out;
}

async function fetchDetails(ids) {
  const body = new URLSearchParams({ itemcount: String(ids.length) });
  ids.forEach((id, i) => body.set(`publishedfileids[${i}]`, id));
  const res = await fetch(DETAILS_API, { method: "POST", body });
  if (!res.ok) throw new Error(`Steam API 응답 ${res.status}`);
  const json = await res.json();
  return new Map(json.response.publishedfiledetails.map((d) => [d.publishedfileid, d]));
}

async function main() {
  const path = fileURLToPath(new URL("../data/mods.json", import.meta.url));
  const data = JSON.parse(await readFile(path, "utf8"));
  const mods = data.mods;
  const inPack = new Set(mods.map((m) => m.workshopId));
  const details = await fetchDetails(mods.map((m) => m.workshopId));

  const errors = [];
  const warnings = [];

  for (const m of mods) {
    const d = details.get(m.workshopId);
    const at = `${m.name} (${m.workshopId})`;
    if (!d || d.result !== 1) {
      errors.push(`${at}: 창작마당에서 찾을 수 없습니다. 내려갔거나 비공개로 바뀌었을 수 있습니다`);
      continue;
    }
    const tags = (d.tags ?? []).map((t) => t.tag);
    if (!tags.includes("Build 42")) errors.push(`${at}: "Build 42" 태그가 없습니다 (태그: ${tags.join(", ") || "없음"})`);

    const updated = new Date(d.time_updated * 1000).toISOString().slice(0, 10);
    if (m.b42?.lastUpdated && updated > m.b42.lastUpdated) {
      warnings.push(`${at}: ${m.b42.lastUpdated} 이후 업데이트됨 (${updated}). 변경 내용을 확인하세요`);
    }

    const ids = parseModIds(d.file_description);
    for (const id of m.modIds) {
      if (ids.length && !ids.includes(id)) warnings.push(`${at}: 설명문의 Mod ID(${ids.join(", ")})에 ${id} 가 없습니다`);
    }

    const html = await (await fetch(PAGE(m.workshopId))).text();
    for (const req of parseRequiredItems(html)) {
      if (!inPack.has(req.id)) errors.push(`${at}: 필요한 모드 ${req.name} (${req.id}) 가 mods.json 에 없습니다`);
      else if (!m.dependsOn.includes(req.id)) warnings.push(`${at}: ${req.name} (${req.id}) 를 dependsOn 에 적어 두세요`);
    }
  }

  for (const w of warnings) console.log(`경고  ${w}`);
  for (const e of errors) console.log(`오류  ${e}`);
  console.log(`\n모드 ${mods.length}개 확인 · 오류 ${errors.length} · 경고 ${warnings.length}`);
  if (errors.length) process.exitCode = 1;
}

// 테스트에서 parse 함수만 가져다 쓸 때는 네트워크를 타지 않는다.
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch((e) => {
    console.error(e);
    process.exitCode = 1;
  });
}
