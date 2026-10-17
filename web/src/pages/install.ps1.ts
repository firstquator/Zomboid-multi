// /install.ps1 : 호스트 친구가 `irm ... | iex` 로 받아 실행하는 설치 스크립트.
// 빌드할 때 mods.json 에서 만들어 정적 파일로 내보낸다.
import type { APIRoute } from "astro";
import { buildInstaller } from "../lib/installer.mjs";
import { mods, site, vanilla, SERVER_NAME, SITE_URL, REPO_URL } from "../lib/site.mjs";

export const GET: APIRoute = () => {
  const sandbox = vanilla.filter((v: any) => v.sandboxKey).map((v: any) => ({ key: v.sandboxKey, value: v.value }));
  const body = buildInstaller({
    mods,
    serverName: SERVER_NAME,
    siteUrl: SITE_URL,
    repoUrl: REPO_URL,
    modpackVersion: site.modpackVersion,
    sandbox,
  });
  return new Response(body, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
};
