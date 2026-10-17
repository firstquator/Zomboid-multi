// 등고선 지도 무늬를 빌드 때 만든다.
//
// 그림 파일을 따로 두지 않고 시드로 만드는 이유는, 페이지마다 다른
// 지형을 같은 코드로 얻기 위해서다. 같은 시드는 언제나 같은 모양을 낸다.

/** 시드 고정 난수. 같은 시드면 같은 수열이 나와야 빌드가 결정적이다. */
export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** 닫힌 점 배열을 Catmull-Rom 곡선으로 이어 부드러운 path 로 만든다. */
export function smoothClosedPath(points) {
  const n = points.length;
  const f = (v) => v.toFixed(1);
  let d = `M${f(points[0][0])},${f(points[0][1])}`;
  for (let i = 0; i < n; i++) {
    const p0 = points[(i - 1 + n) % n];
    const p1 = points[i];
    const p2 = points[(i + 1) % n];
    const p3 = points[(i + 2) % n];
    const c1x = p1[0] + (p2[0] - p0[0]) / 6;
    const c1y = p1[1] + (p2[1] - p0[1]) / 6;
    const c2x = p2[0] - (p3[0] - p1[0]) / 6;
    const c2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += `C${f(c1x)},${f(c1y)} ${f(c2x)},${f(c2y)} ${f(p2[0])},${f(p2[1])}`;
  }
  return d + "Z";
}

/**
 * 언덕 몇 개를 놓고 각 언덕에 등고선을 겹겹이 그린다.
 * @returns {{ d: string, major: boolean }[]} 다섯 번째 선마다 major(굵은 선)
 */
export function topoPaths({ seed = 1, width = 1600, height = 900, hills = 3, levels = 9 } = {}) {
  const rand = mulberry32(seed);
  const out = [];
  for (let h = 0; h < hills; h++) {
    const cx = width * (0.12 + rand() * 0.76);
    const cy = height * (0.12 + rand() * 0.76);
    const base = Math.min(width, height) * (0.05 + rand() * 0.05);
    const step = Math.min(width, height) * (0.045 + rand() * 0.025);
    const waves = Array.from({ length: 4 }, (_, j) => ({
      k: j + 2,
      amp: 0.06 + rand() * 0.12,
      phase: rand() * Math.PI * 2,
      drift: (rand() - 0.5) * 0.5,
    }));
    const stretch = 0.75 + rand() * 0.6;
    for (let lv = 0; lv < levels; lv++) {
      const r0 = base + lv * step;
      const pts = [];
      const N = 72;
      for (let i = 0; i < N; i++) {
        const t = (i / N) * Math.PI * 2;
        let r = 1;
        for (const w of waves) r += w.amp * Math.sin(w.k * t + w.phase + lv * w.drift);
        const rr = r0 * r;
        pts.push([cx + Math.cos(t) * rr * stretch, cy + Math.sin(t) * rr]);
      }
      out.push({ d: smoothClosedPath(pts), major: lv % 5 === 4 });
    }
  }
  return out;
}
