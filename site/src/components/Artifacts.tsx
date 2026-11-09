import { ARTIFACT_LINKS } from "../config";

const ITEMS = [
  {
    kind: "Simulator",
    title: "Chinchilla / data exhaustion",
    blurb:
      "Live loss-wall laboratory embedded above. Python Streamlit twin lives in the repo for Spaces mirrors.",
    href: "#sim-chinchilla",
  },
  {
    kind: "Simulator",
    title: "Acemoglu task → GDP",
    blurb:
      "Ten-year TFP/GDP paths with capital drag—running entirely in-browser on this page.",
    href: "#sim-gdp",
  },
  {
    kind: "Code",
    title: "mini-prm-rejection-sampler",
    blurb:
      "Step-level PRM vs outcome filtering for synthetic trajectory quality—how you raise δ.",
    href: ARTIFACT_LINKS.prm,
  },
  {
    kind: "Code",
    title: "refusal-vector-steering",
    blurb:
      "Defensive mech-interp: difference-in-means refusal directions and orthogonal ablation.",
    href: ARTIFACT_LINKS.refusal,
  },
  {
    kind: "Memo",
    title: "Hardware Wall vs Data Wall",
    blurb:
      "Executive CapEx memorandum for lab leadership and venture committees.",
    href: ARTIFACT_LINKS.memoHardware,
  },
  {
    kind: "Memo",
    title: "Weight theft & SCIF protocols",
    blurb:
      "National-security teardown of exfiltration risk above 10²⁶ FLOPs.",
    href: ARTIFACT_LINKS.memoTheft,
  },
];

export function Artifacts() {
  return (
    <section className="chapter" id="artifacts">
      <div className="chapter-inner">
        <p className="chapter-index">04 · Portfolio</p>
        <h2>Artifacts behind the argument</h2>
        <p className="prose lede">
          The dissertation is the spine. The triad—code, simulators,
          strategy memos—is the proof of work.
        </p>

        <ul className="artifact-list">
          {ITEMS.map((item) => (
            <li key={item.title}>
              <a
                href={item.href}
                {...(item.href.startsWith("http")
                  ? { target: "_blank", rel: "noreferrer" }
                  : {})}
              >
                <span className="artifact-kind">{item.kind}</span>
                <strong>{item.title}</strong>
                <span className="artifact-blurb">{item.blurb}</span>
              </a>
            </li>
          ))}
        </ul>

        <div className="refs prose" id="references">
          <h3>Selected references</h3>
          <ul>
            <li>
              Hoffmann et al., <em>Training Compute-Optimal Large Language
              Models</em> (Chinchilla), 2022.
            </li>
            <li>
              Villalobos et al., Epoch AI work on human-text data exhaustion
              bounds.
            </li>
            <li>
              Acemoglu / Restrepo task-based automation and TFP frameworks.
            </li>
            <li>
              Ege Erdil, multi-decade timeline / physical bottleneck arguments.
            </li>
            <li>
              Leopold Aschenbrenner, <em>Situational Awareness</em> (capability
              and security framing).
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}
