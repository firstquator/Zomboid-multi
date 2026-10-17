import { describe, it, expect } from "vitest";
import { parseRequiredItems, parseModIds } from "../../scripts/verify-workshop.mjs";

describe("verify-workshop 파서", () => {
  it("워크숍 페이지의 Required items 를 뽑는다", () => {
    const html = `
      <div class="requiredItemsContainer" id="RequiredItems">
        <a href="https://steamcommunity.com/workshop/filedetails/?id=2392709985" target="_blank">
          <div class="requiredItem">
            Tsar's Common Library
          </div>
        </a>
        <a href="https://steamcommunity.com/workshop/filedetails/?id=111" target="_blank"><div class="requiredItem">Other</div></a>
      </div>`;
    expect(parseRequiredItems(html)).toEqual([
      { id: "2392709985", name: "Tsar's Common Library" },
      { id: "111", name: "Other" },
    ]);
  });

  it("설명문의 Mod ID 줄을 모두 뽑고 BBCode 앞에서 끊는다", () => {
    const d = "Workshop ID: 123\r\nMod ID: ModA\r\nMod ID: ModA_B42[/b]\nmod id:ModC";
    expect(parseModIds(d)).toEqual(["ModA", "ModA_B42", "ModC"]);
  });
});
