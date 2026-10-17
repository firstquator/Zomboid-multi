import { describe, it, expect } from "vitest";
import { keyify } from "../src/lib/keytext.mjs";

describe("문장 속 키를 키캡으로", () => {
  it("글자 하나·이름 있는 키·조합 키를 바꾼다", () => {
    expect(keyify("B 로 제작창을 연다")).toBe("<kbd>B</kbd> 로 제작창을 연다");
    expect(keyify("N 으로 시동")).toBe("<kbd>N</kbd> 으로 시동");
    expect(keyify("Space 로 밀친다")).toBe("<kbd>Space</kbd> 로 밀친다");
    expect(keyify("Shift+W 로 켜고")).toBe("<kbd>Shift</kbd>+<kbd>W</kbd> 로 켜고");
    expect(keyify("버튼을 Shift+클릭하면")).toBe("버튼을 <kbd>Shift</kbd>+클릭하면");
    expect(keyify("W 앞으로, A·D 방향")).toBe("<kbd>W</kbd> 앞으로, <kbd>A</kbd>·<kbd>D</kbd> 방향");
    expect(keyify("전력질주(Alt) 발소리")).toBe("전력질주(<kbd>Alt</kbd>) 발소리");
    expect(keyify("V → 「창문 부수기」")).toBe("<kbd>V</kbd> → 「창문 부수기」");
    expect(keyify("채팅창에서 \\ 로 한/영")).toBe("채팅창에서 <kbd>\\</kbd> 로 한/영");
    expect(keyify("Esc → 친구 초대")).toBe("<kbd>Esc</kbd> → 친구 초대");
  });

  it("숫자·글자가 붙은 낱말은 그대로 둔다", () => {
    for (const s of ["B42는 실내가 어둡다", "D6 (픽업)", "기름통 10L, 제리캔 20L", "TV·비디오", "VHS 테이프", "Endurance", "PZwiki", "/all 은 전체"]) {
      expect(keyify(s)).not.toContain("<kbd>");
    }
  });

  it("HTML 을 이스케이프한다", () => {
    expect(keyify('<b>"E"</b>')).toBe("&lt;b&gt;&quot;<kbd>E</kbd>&quot;&lt;/b&gt;".replace("<kbd>E</kbd>", "E"));
  });
});
