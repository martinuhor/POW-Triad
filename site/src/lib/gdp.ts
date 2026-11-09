export const YEARS = 10;

export type GdpRow = {
  year: number;
  adoptionEasy: number;
  adoptionHard: number;
  autoEasyShare: number;
  autoHardShare: number;
  tfp: number;
  gdp: number;
  gdpDigitalOnly: number;
  tfpGrowthCumPct: number;
  gdpGrowthCumPct: number;
};

/**
 * Acemoglu-style discrete-time task automation → TFP → GDP.
 * GDP is TFP attenuated by physical capital / deployment drag.
 */
export function simulatePaths(opts: {
  exposure: number;
  savingsEasy: number;
  savingsHard: number;
  easyShare: number;
  adoptionHalflifeEasy: number;
  adoptionHalflifeHard: number;
  capitalDrag: number;
}): GdpRow[] {
  const {
    exposure,
    savingsEasy,
    savingsHard,
    easyShare,
    adoptionHalflifeEasy,
    adoptionHalflifeHard,
    capitalDrag,
  } = opts;

  const hardShare = 1 - easyShare;
  const exposedEasy = exposure * easyShare;
  const exposedHard = exposure * hardShare;

  const rows: GdpRow[] = [];
  for (let t = 0; t <= YEARS; t++) {
    const adoptEasy = 1 - 0.5 ** (t / Math.max(adoptionHalflifeEasy, 1e-6));
    const adoptHard = 1 - 0.5 ** (t / Math.max(adoptionHalflifeHard, 1e-6));
    const autoEasy = exposedEasy * adoptEasy;
    const autoHard = exposedHard * adoptHard;
    const logTfp = savingsEasy * autoEasy + savingsHard * autoHard;
    const tfp = Math.exp(logTfp);
    const gdp = Math.exp(logTfp * (1 - capitalDrag));
    const gdpDigitalOnly = tfp;

    rows.push({
      year: t,
      adoptionEasy: adoptEasy,
      adoptionHard: adoptHard,
      autoEasyShare: autoEasy,
      autoHardShare: autoHard,
      tfp,
      gdp,
      gdpDigitalOnly,
      tfpGrowthCumPct: 100 * (tfp - 1),
      gdpGrowthCumPct: 100 * (gdp - 1),
    });
  }
  return rows;
}
