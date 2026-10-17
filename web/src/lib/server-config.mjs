// 서버 설정 파일(<서버이름>.ini)에 들어갈 줄을 mods.json 에서 만든다.
//
// 설치 스크립트, 모드팩 화면의 "직접 넣기" 칸, 내려받는 ini 파일이 모두
// 이 함수들을 거친다. 셋이 각자 줄을 만들면 언젠가 서로 달라진다.

/**
 * Mods= 줄의 Mod ID 앞에 붙일 글자.
 *
 * 42.20 무렵 가이드들은 B42 서버에 역슬래시(\ModA)를 붙이라고 했다. 42.21 서버는
 * Mods= 값에서 역슬래시를 전부 지우고 읽어서 붙이든 말든 결과가 같다. 반면 게임의
 * "서버 설정 → 모드" 화면은 접두 없는 ID 로 저장하고, 접두가 붙은 항목은
 * "알 수 없는 모드" 로 보여 준다. 모두 42.21 을 써야 접속할 수 있으므로 게임이
 * 직접 쓰는 형식(접두 없음)을 따른다. 근거: docs/research/hosting.md 4절.
 */
export const MOD_PREFIX = "";

/** loadOrder 순으로 정렬한 사본. 원본 배열 순서에 기대지 않는다. */
export const ordered = (mods) => [...mods].sort((a, b) => a.loadOrder - b.loadOrder);

/** WorkshopItems= 값. 창작마당 아이템 번호를 세미콜론으로 잇는다. 중복은 한 번만. */
export function workshopItems(mods) {
  const seen = new Set();
  const ids = [];
  for (const m of ordered(mods)) {
    if (!seen.has(m.workshopId)) {
      seen.add(m.workshopId);
      ids.push(m.workshopId);
    }
  }
  return ids.join(";");
}

/** Mods= 값. 한 아이템에 Mod ID 가 여러 개면 전부 넣는다. */
export function modIds(mods) {
  return ordered(mods)
    .flatMap((m) => m.modIds)
    .map((id) => `${MOD_PREFIX}${id}`)
    .join(";");
}

/**
 * 설치 스크립트가 덮어쓸 ini 키와 값.
 * 여기 없는 키는 게임이 만든 기본값을 그대로 둔다.
 * @param {{ key: string, value: string }[]} [extra] mods.json 의 vanilla 중 ini 값(지도 표시 등)
 */
export function iniOverrides(mods, extra = []) {
  return {
    WorkshopItems: workshopItems(mods),
    Mods: modIds(mods),
    // 친구끼리 협동이라 서로 공격하지 않게 끈다. 게임 기본값은 true.
    PVP: "false",
    // 서버 목록에 공개하지 않는다. 들어오는 길은 호스트의 Steam 초대뿐이다.
    Public: "false",
    // 아무도 없으면 시간을 멈춘다(게임 기본값과 같지만 명시해 둔다).
    PauseEmpty: "true",
    ...Object.fromEntries(extra.map((e) => [e.key, e.value])),
  };
}

/** 사람이 직접 붙여 넣을 때 보여 줄 두 줄. */
export function manualLines(mods) {
  return [`WorkshopItems=${workshopItems(mods)}`, `Mods=${modIds(mods)}`];
}
