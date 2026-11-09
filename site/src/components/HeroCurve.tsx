import { useMemo } from "react";
import {
  buildLossCurves,
  dataWallCompute,
  effectiveTokens,
} from "../lib/chinchilla";

/** Full-bleed loss-wall visualization for the hero plane. */
export function HeroCurve() {
  const { pathUnc, pathCap, wallX } = useMemo(() => {
    const dEff = effectiveTokens(1e14, 1e14, 0.55);
    const pts = buildLossCurves(dEff, 23, 28, 64);
    const w = 1200;
    const h = 720;
    const pad = { t: 80, r: 40, b: 60, l: 40 };
    const xs = pts.map((p) => p.logC);
    const ys = pts.flatMap((p) => [p.unconstrained, p.capped]);
    const x0 = Math.min(...xs);
    const x1 = Math.max(...xs);
    const y0 = Math.min(...ys) * 0.98;
    const y1 = Math.max(...ys) * 1.02;

    const sx = (x: number) =>
      pad.l + ((x - x0) / (x1 - x0)) * (w - pad.l - pad.r);
    const sy = (y: number) =>
      pad.t + ((y1 - y) / (y1 - y0)) * (h - pad.t - pad.b);

    const toPath = (key: "unconstrained" | "capped") =>
      pts
        .map((p, i) => `${i === 0 ? "M" : "L"} ${sx(p.logC)} ${sy(p[key])}`)
        .join(" ");

    const wallLog = Math.log10(dataWallCompute(dEff));
    const clampedWall = Math.min(Math.max(wallLog, x0), x1);

    return {
      pathUnc: toPath("unconstrained"),
      pathCap: toPath("capped"),
      wallX: sx(clampedWall),
    };
  }, []);

  return (
    <svg
      className="hero-curve"
      viewBox="0 0 1200 720"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="capFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#e0a45a" stopOpacity="0.28" />
          <stop offset="100%" stopColor="#e0a45a" stopOpacity="0" />
        </linearGradient>
        <linearGradient id="uncStroke" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#5ec4a8" stopOpacity="0.15" />
          <stop offset="40%" stopColor="#5ec4a8" stopOpacity="0.9" />
          <stop offset="100%" stopColor="#8fd4c1" stopOpacity="0.35" />
        </linearGradient>
      </defs>

      {Array.from({ length: 12 }).map((_, i) => (
        <line
          key={`v-${i}`}
          className="hero-grid"
          x1={(i + 1) * 100}
          y1="0"
          x2={(i + 1) * 100}
          y2="720"
        />
      ))}
      {Array.from({ length: 8 }).map((_, i) => (
        <line
          key={`h-${i}`}
          className="hero-grid"
          x1="0"
          y1={(i + 1) * 90}
          x2="1200"
          y2={(i + 1) * 90}
        />
      ))}

      <path d={`${pathCap} L 1160 660 L 40 660 Z`} fill="url(#capFill)" />
      <path
        className="hero-path-unc"
        d={pathUnc}
        fill="none"
        stroke="url(#uncStroke)"
        strokeWidth="2.5"
      />
      <path
        className="hero-path-cap"
        d={pathCap}
        fill="none"
        stroke="#e0a45a"
        strokeWidth="2.75"
      />
      <line
        className="hero-wall"
        x1={wallX}
        y1="40"
        x2={wallX}
        y2="680"
        stroke="#9aa7b5"
        strokeDasharray="4 8"
        strokeWidth="1.25"
      />
      <text x={wallX + 10} y="70" className="hero-wall-label">
        data exhaustion wall
      </text>
    </svg>
  );
}
