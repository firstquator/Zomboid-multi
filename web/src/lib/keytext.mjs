// 문장 속 키 이름을 키캡(<kbd>)으로 바꾼다. 입력은 일반 문자열이고 출력은 HTML 이다.
// 예: "B 로 제작창을 연다" → "<kbd>B</kbd> 로 제작창을 연다", "Shift+W" → "<kbd>Shift</kbd>+<kbd>W</kbd>"
// B42, D6, 10L, TV 처럼 글자가 숫자·글자와 붙어 있으면 키로 보지 않는다.

const NAMED = "Space|Shift|Ctrl|Alt|Esc|Tab|Enter|End|Win|F1[0-2]|F[1-9]";

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

export function keyify(text) {
  let s = esc(text);
  // 조합 키: Shift+W, Ctrl+A, Shift+클릭
  s = s.replace(new RegExp(`(^|[^\\w>/])(${NAMED})\\+(${NAMED}|[A-Z0-9](?![A-Za-z0-9])|좌클릭|우클릭|클릭)`, "g"), (m, p, a, b) =>
    `${p}<kbd>${a}</kbd>+${/[가-힣]/.test(b) ? b : `<kbd>${b}</kbd>`}`,
  );
  // 이름 있는 키. 이미 키캡 안에 있는 것(앞이 >)은 건너뛴다.
  s = s.replace(new RegExp(`(^|[^\\w>/])(${NAMED})(?![\\w<])`, "g"), (m, p, k) => `${p}<kbd>${k}</kbd>`);
  // 글자 하나짜리 키: 앞이 줄 시작·공백·괄호·가운뎃점이고, 뒤가 공백·한글 조사·문장부호일 때만
  s = s.replace(/(^|[\s(·])([A-Z])(?=$|[\s)·,.→~]|[가-힣])/g, (m, p, k) => `${p}<kbd>${k}</kbd>`);
  // 역슬래시 키(한/영 전환 모드)
  s = s.replace(/(^|\s)\\(?=$|\s|[가-힣])/g, "$1<kbd>\\</kbd>");
  return s;
}
