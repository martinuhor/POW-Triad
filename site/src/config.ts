/** GitHub remote for martinuhor (create/push when ready). */
export const REPO_URL =
  import.meta.env.VITE_REPO_URL ?? "https://github.com/martinuhor/POW-Triad";

export const ARTIFACT_LINKS = {
  prm: `${REPO_URL}/tree/main/code/mini-prm-rejection-sampler`,
  refusal: `${REPO_URL}/tree/main/code/refusal-vector-steering`,
  memoHardware: `${REPO_URL}/blob/main/memos/hardware-wall-vs-data-wall.md`,
  memoTheft: `${REPO_URL}/blob/main/memos/weight-theft-risks.md`,
  streamlitChinchilla: `${REPO_URL}/tree/main/simulators/chinchilla-data-exhaustion-app`,
  streamlitGdp: `${REPO_URL}/tree/main/simulators/task-macro-gdp-simulator`,
} as const;
