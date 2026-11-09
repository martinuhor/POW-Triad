import { Formula } from "./Formula";
import { GdpSim } from "./GdpSim";

export function ChapterMacro() {
  return (
    <section className="chapter chapter-lab" id="macro">
      <div className="chapter-inner">
        <p className="chapter-index">02 · The Macro Lag</p>
        <h2>Task exposure, capital drag, and why GDP trails the lab</h2>
        <div className="prose">
          <p className="lede">
            Accelerationist timelines extrapolate effective compute. Macro
            skeptics ask a different question: which tasks are exposed, how
            fast can they adopt, and how much complementary physical capital
            is required before measured productivity moves?
          </p>
          <p>
            Following Acemoglu&apos;s task-based production view, AI does not
            raise TFP uniformly. It automates a subset of tasks with
            heterogeneous cost savings. Easy tasks adopt quickly; hard tasks
            require redesign, regulation, energy, and human–tool integration.
            We encode that as exposure-weighted automation with separate
            half-lives, then attenuate TFP into GDP by a capital-drag factor{" "}
            <Formula tex="\kappa" />:
          </p>
          <div className="equation-block">
            <Formula
              display
              tex="\mathrm{GDP}_t=\exp\!\big(\log\mathrm{TFP}_t\cdot(1-\kappa)\big)"
            />
          </div>
          <p>
            The teal &ldquo;digital-only&rdquo; path is what a frontier lab
            can feel internally. The amber path is closer to what national
            accounts may report over a decade. That gap is the reconciliation
            between Situational Awareness–style capability forecasts and
            Erdil / Acemoglu-style deployment skepticism.
          </p>
        </div>

        <GdpSim />
      </div>
    </section>
  );
}
