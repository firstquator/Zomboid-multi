// 캐릭터 만들기 계산 규칙. 페이지의 계산기와 테스트가 같이 쓴다.
//
// 게임의 포인트 규칙: 남은 포인트 = 직업 포인트 − Σ(특성 비용) 이 0 이상이어야 시작할 수 있다.
// 긍정 특성은 비용이 양수라 포인트를 쓰고, 부정 특성은 음수라 포인트를 돌려준다.
// (무직은 +8, 퇴역 군인은 −8 처럼 직업 포인트 자체가 양수·음수다.)

/**
 * 멀티에서 잠 설정(SleepAllowed, SleepNeeded)이 둘 다 켜져 있지 않으면 캐릭터 생성 화면에서
 * 고를 수 없는 특성. 게임 CharacterCreationProfession.lua 의 isTraitEnabled 그대로다.
 * 우리 서버는 두 설정을 기본값(false)으로 둔다.
 */
export const SLEEP_TRAITS = ["insomniac", "needslesssleep", "needsmoresleep"];

/** 남은 포인트. */
export function remainingPoints(profession, traits) {
  return (profession?.cost ?? 0) - traits.reduce((sum, t) => sum + t.cost, 0);
}

/**
 * 고른 특성들 사이, 그리고 직업이 주는 특성과 부딪히는 쌍을 찾는다.
 * @returns {[string, string][]} 부딪히는 특성 id 쌍
 */
export function conflicts(profession, traits) {
  const ids = new Set([...traits.map((t) => t.id), ...(profession?.granted ?? [])]);
  const out = [];
  for (const t of traits) {
    for (const ex of t.exclusive) {
      if (ids.has(ex) && !out.some(([a, b]) => (a === ex && b === t.id) || (a === t.id && b === ex))) {
        out.push([t.id, ex]);
      }
    }
  }
  return out;
}

/**
 * 직업과 특성이 주는 기술 보너스를 합친다. 같은 기술은 더한다.
 * @returns {{ skill: string, name: string, level: number }[]} 높은 순
 */
export function skillTotals(profession, traits) {
  const map = new Map();
  for (const src of [profession, ...traits]) {
    for (const x of src?.xp ?? []) {
      const cur = map.get(x.skill) ?? { skill: x.skill, name: x.name, level: 0 };
      cur.level += x.level;
      map.set(x.skill, cur);
    }
  }
  return [...map.values()].filter((x) => x.level !== 0).sort((a, b) => b.level - a.level);
}

/** 조합을 주소 해시로 바꾼다. 친구에게 링크로 보낼 때 쓴다. 예: #b=fireofficer.thickskinned.keenhearing */
export const encodeBuild = (professionId, traitIds) => `b=${[professionId, ...traitIds].join(".")}`;

/** 주소 해시에서 조합을 읽는다. 형식이 아니면 null. */
export function decodeBuild(hash) {
  const m = /(?:^#?|&)b=([a-z0-9_.]+)/i.exec(hash ?? "");
  if (!m) return null;
  const [professionId, ...traitIds] = m[1].split(".").filter(Boolean);
  return professionId ? { professionId, traitIds } : null;
}
