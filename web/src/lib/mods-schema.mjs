// mods.json 검증. 외부 라이브러리를 쓰지 않는다.
// 필드가 많지 않아서 직접 검사하는 편이 의존성을 줄인다.

const REQUIRED = ["workshopId", "name", "nameKo", "category", "summary", "why", "url"];
const KOREAN = ["native", "via-pack", "none"];
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const WORKSHOP_ID = /^\d{6,12}$/;
// Mod ID 는 ini 의 Mods= 줄에 그대로 들어간다. 세미콜론이나 줄바꿈이
// 섞이면 줄 전체가 깨지고, 역슬래시는 우리가 앞에 붙이므로 들어 있으면 안 된다.
const MOD_ID = /^[^;\\\r\n=]+$/;

/**
 * 모드팩 변경 이력을 검사한다.
 * 맨 앞이 최신이라는 전제로 화면에 보여 주므로 최신순 정렬까지 본다.
 */
function validateChanges(changes) {
  const errors = [];
  if (changes === undefined) return errors;
  if (!Array.isArray(changes)) return ["modpack.changes 는 배열이어야 합니다"];

  changes.forEach((c, i) => {
    const at = `modpack.changes[${i}]`;
    if (!DATE.test(c?.date ?? "")) errors.push(`${at}.date 는 YYYY-MM-DD 형식이어야 합니다 (받은 값: ${c?.date})`);
    if (!c?.summary) errors.push(`${at}.summary 가 없습니다`);
    if (typeof c?.mustUpdate !== "boolean") {
      errors.push(`${at}.mustUpdate 는 true 또는 false 여야 합니다 (받은 값: ${c?.mustUpdate})`);
    }
    // YYYY-MM-DD 는 사전순 비교가 곧 날짜순 비교다.
    if (i > 0 && DATE.test(c?.date ?? "") && DATE.test(changes[i - 1]?.date ?? "") && c.date > changes[i - 1].date) {
      errors.push(`${at}.date 가 앞 항목보다 뒤입니다. 최신순으로 적어야 합니다`);
    }
  });
  return errors;
}

/**
 * 의존 관계를 검사한다.
 *
 * 의존 모드가 목록에 없으면 서버가 시작하지 못하거나 모드가 조용히 꺼진다.
 * 또 의존 모드는 쓰는 쪽보다 먼저 불러와야 하므로 loadOrder 가 앞서야 한다.
 * 단 두 모드가 서로를 필수로 지정한 경우(errorMagnifier 와 Alert System 처럼)는
 * 어느 쪽도 먼저일 수 없으니 순서는 보지 않고 둘 다 있는지만 본다.
 */
function validateDependencies(mods) {
  const errors = [];
  const byId = new Map(mods.map((m) => [m.workshopId, m]));
  mods.forEach((m, i) => {
    const at = `mods[${i}] (${m.name})`;
    if (!Array.isArray(m.dependsOn)) {
      errors.push(`${at}.dependsOn 은 배열이어야 합니다`);
      return;
    }
    for (const dep of m.dependsOn) {
      const d = byId.get(dep);
      if (!d) {
        errors.push(`${at} 가 필요로 하는 모드 ${dep} 가 목록에 없습니다`);
      } else if (dep === m.workshopId) {
        errors.push(`${at} 가 자기 자신을 의존합니다`);
      } else if (!(d.dependsOn ?? []).includes(m.workshopId) && !(d.loadOrder < m.loadOrder)) {
        errors.push(`${at} 의 의존 모드 ${d.name} 는 loadOrder 가 더 앞서야 합니다 (${d.loadOrder} → ${m.loadOrder})`);
      }
    }
  });
  return errors;
}

const VANILLA_FILES = ["ini", "sandbox"];
const INI_KEY = /^[A-Za-z][A-Za-z0-9]*$/;
const SANDBOX_KEY = /^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$/;
const SANDBOX_VALUE = /^(true|false|-?\d+(\.\d+)?)$/;

/**
 * 서버 설정으로 켜는 기본 기능 목록을 검사한다. 설치 스크립트가 이 값을 그대로
 * ini 와 SandboxVars.lua 에 쓰므로, 형식이 틀리면 설정이 무시되거나 서버가 꺼진다.
 */
function validateVanilla(vanilla) {
  const errors = [];
  if (vanilla === undefined) return errors;
  if (!Array.isArray(vanilla)) return ["vanilla 는 배열이어야 합니다"];
  vanilla.forEach((v, i) => {
    const at = `vanilla[${i}]${v?.feature ? ` (${v.feature})` : ""}`;
    for (const f of ["feature", "file", "key", "value", "where", "why"]) {
      if (!v?.[f]) errors.push(`${at}.${f} 가 없습니다`);
    }
    if (!VANILLA_FILES.includes(v?.file)) errors.push(`${at}.file 은 ini 또는 sandbox 여야 합니다 (받은 값: ${v?.file})`);
    if (v?.file === "ini" && (!INI_KEY.test(v.key ?? "") || /[=\r\n]/.test(v.value ?? ""))) {
      errors.push(`${at} 의 ini 키나 값 형식이 틀렸습니다: ${v.key}=${v.value}`);
    }
    if (v?.file === "sandbox" && (!SANDBOX_KEY.test(v.key ?? "") || !SANDBOX_VALUE.test(v.value ?? ""))) {
      errors.push(`${at} 의 샌드박스 키나 값 형식이 틀렸습니다 (값은 true, false, 숫자): ${v.key} = ${v.value}`);
    }
  });
  return errors;
}

export function validateMods(data) {
  const errors = [];

  if (!data || typeof data !== "object") return { ok: false, errors: ["데이터가 객체가 아닙니다"] };
  if (data.schemaVersion !== 1) errors.push(`schemaVersion 은 1 이어야 합니다 (받은 값: ${data.schemaVersion})`);
  if (!data.game?.build) errors.push("game.build 가 없습니다");
  if (!DATE.test(data.game?.checkedAt ?? "")) errors.push("game.checkedAt 은 YYYY-MM-DD 형식이어야 합니다");
  if (!data.modpack?.version) errors.push("modpack.version 이 없습니다");
  if (!Array.isArray(data.categories) || data.categories.length === 0) errors.push("categories 가 비어 있습니다");
  if (!Array.isArray(data.mods)) return { ok: false, errors: [...errors, "mods 는 배열이어야 합니다"] };

  errors.push(...validateChanges(data.modpack?.changes));
  errors.push(...validateVanilla(data.vanilla));

  const cats = new Set((data.categories ?? []).map((c) => c.id));
  const seenWs = new Set();
  const seenModId = new Set();
  const seenOrder = new Set();

  data.mods.forEach((m, i) => {
    const at = `mods[${i}]${m?.name ? ` (${m.name})` : ""}`;
    for (const f of REQUIRED) {
      if (m[f] === undefined || m[f] === null || m[f] === "") errors.push(`${at}.${f} 가 없습니다`);
    }
    if (!WORKSHOP_ID.test(m.workshopId ?? "")) errors.push(`${at}.workshopId 가 숫자 형식이 아닙니다 (받은 값: ${m.workshopId})`);
    if (seenWs.has(m.workshopId)) errors.push(`${at}.workshopId 가 중복입니다: ${m.workshopId}`);
    seenWs.add(m.workshopId);

    if (!Array.isArray(m.modIds) || m.modIds.length === 0) {
      errors.push(`${at}.modIds 는 하나 이상 있어야 합니다`);
    } else {
      for (const id of m.modIds) {
        if (!MOD_ID.test(id)) errors.push(`${at}.modIds 에 쓸 수 없는 글자가 있습니다: ${JSON.stringify(id)}`);
        if (seenModId.has(id)) errors.push(`${at}.modIds 가 다른 모드와 겹칩니다: ${id}`);
        seenModId.add(id);
      }
    }

    if (!cats.has(m.category)) errors.push(`${at}.category 가 categories 에 없습니다 (받은 값: ${m.category})`);
    if (!KOREAN.includes(m.korean?.status)) {
      errors.push(`${at}.korean.status 는 ${KOREAN.join(", ")} 중 하나여야 합니다 (받은 값: ${m.korean?.status})`);
    }
    if (m.b42?.supported !== true) errors.push(`${at}.b42.supported 가 true 가 아닙니다. B42 에서 확인된 모드만 넣습니다`);
    if (!Number.isInteger(m.loadOrder) || m.loadOrder < 1) errors.push(`${at}.loadOrder 는 1 이상의 정수여야 합니다`);
    if (seenOrder.has(m.loadOrder)) errors.push(`${at}.loadOrder 가 중복입니다: ${m.loadOrder}`);
    seenOrder.add(m.loadOrder);
    if (!String(m.url ?? "").includes(m.workshopId)) errors.push(`${at}.url 이 workshopId 와 맞지 않습니다`);
  });

  errors.push(...validateDependencies(data.mods));

  return errors.length ? { ok: false, errors } : { ok: true };
}
