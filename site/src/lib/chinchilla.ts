/** Hoffmann et al. (2022) IsoFLOP / Chinchilla loss fit */
export const A = 406.4;
export const B = 410.7;
export const E = 1.69;
export const ALPHA = 0.34;
export const BETA = 0.28;
export const FLOPS_PER_TOKEN_PARAM = 6;

export function loss(n: number, d: number): number {
  return E + A / n ** ALPHA + B / d ** BETA;
}

/**
 * Compute-optimal N*, D* under C = 6ND for L = E + A/N^α + B/D^β.
 * N* = [(α A)/(β B)]^{1/(α+β)} · (C/6)^{β/(α+β)}, D* = C/(6 N*).
 */
export function chinchillaOptimalNd(c: number): { n: number; d: number } {
  const coeff = (ALPHA * A) / (BETA * B);
  const n =
    coeff ** (1 / (ALPHA + BETA)) *
    (c / FLOPS_PER_TOKEN_PARAM) ** (BETA / (ALPHA + BETA));
  const d = c / (FLOPS_PER_TOKEN_PARAM * n);
  return { n, d };
}

export function effectiveTokens(
  dHuman: number,
  dSynthetic: number,
  quality: number,
): number {
  return dHuman + quality * dSynthetic;
}

export function tokensUnderBudget(c: number, n: number): number {
  return c / (FLOPS_PER_TOKEN_PARAM * n);
}

/**
 * Compute budget where unconstrained D* first hits D_eff.
 * From D* = (1/k)(C/6)^{α/(α+β)} with k = [(α A)/(β B)]^{1/(α+β)}.
 */
export function dataWallCompute(dEff: number): number {
  const k = ((ALPHA * A) / (BETA * B)) ** (1 / (ALPHA + BETA));
  return FLOPS_PER_TOKEN_PARAM * (k * dEff) ** ((ALPHA + BETA) / ALPHA);
}

export function lossPenaltyVsChinchilla(lActual: number, lChin: number): number {
  if (lChin <= 0) return 0;
  return (lActual - lChin) / lChin;
}

export type LossCurvePoint = {
  logC: number;
  unconstrained: number;
  capped: number;
};

/** Sweep compute budgets and compare unconstrained vs data-capped loss. */
export function buildLossCurves(
  dEff: number,
  logMin = 23,
  logMax = 28,
  steps = 80,
): LossCurvePoint[] {
  const out: LossCurvePoint[] = [];
  for (let i = 0; i <= steps; i++) {
    const logC = logMin + ((logMax - logMin) * i) / steps;
    const c = 10 ** logC;
    const { n: nStar, d: dStar } = chinchillaOptimalNd(c);
    const unconstrained = loss(nStar, dStar);

    let capped: number;
    if (dStar <= dEff) {
      capped = unconstrained;
    } else {
      // Data-capped: fix D = D_eff, put remaining FLOPs into N
      const nCapped = c / (FLOPS_PER_TOKEN_PARAM * dEff);
      capped = loss(nCapped, dEff);
    }
    out.push({ logC, unconstrained, capped });
  }
  return out;
}

export function formatScientific(n: number, digits = 2): string {
  if (!Number.isFinite(n) || n === 0) return "0";
  const exp = Math.floor(Math.log10(Math.abs(n)));
  const mant = n / 10 ** exp;
  return `${mant.toFixed(digits)}×10${toSuperscript(exp)}`;
}

function toSuperscript(n: number): string {
  const map: Record<string, string> = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "-": "⁻",
  };
  return String(n)
    .split("")
    .map((c) => map[c] ?? c)
    .join("");
}

export function formatParams(n: number): string {
  if (n >= 1e12) return `${(n / 1e12).toFixed(2)} T`;
  if (n >= 1e9) return `${(n / 1e9).toFixed(2)} B`;
  if (n >= 1e6) return `${(n / 1e6).toFixed(2)} M`;
  return n.toExponential(2);
}

export function formatTokens(d: number): string {
  if (d >= 1e12) return `${(d / 1e12).toFixed(2)} T`;
  if (d >= 1e9) return `${(d / 1e9).toFixed(2)} B`;
  return d.toExponential(2);
}
