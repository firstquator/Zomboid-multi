import { defineConfig } from "astro/config";
import { validateMods } from "./src/lib/mods-schema.mjs";
import mods from "../data/mods.json" with { type: "json" };

// 빌드 시작 전에 검증한다. 잘못된 모드 정보가 배포되면 호스트 친구의
// 서버가 모드를 못 찾거나, 의존 모드가 빠져 접속이 막힌다.
const result = validateMods(mods);
if (!result.ok) {
  console.error("data/mods.json 검증 실패:");
  for (const e of result.errors) console.error("  - " + e);
  process.exit(1);
}

export default defineConfig({
  site: "https://firstquator.github.io",
  base: "/Zomboid-multi",
  trailingSlash: "ignore",
});
