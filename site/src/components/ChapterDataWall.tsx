import { Formula } from "./Formula";
import { ChinchillaSim } from "./ChinchillaSim";

export function ChapterDataWall() {
  return (
    <section className="chapter chapter-lab" id="data-wall">
      <div className="chapter-inner">
        <p className="chapter-index">01 · The Data Wall</p>
        <h2>Chinchilla optimality meets human-token exhaustion</h2>
        <div className="prose">
          <p className="lede">
            Under unconstrained Chinchilla scaling, parameters and tokens
            grow together. Once unique human text saturates, every additional
            FLOP spent without raising effective data is parameter
            over-training—and the loss frontier bends.
          </p>
          <p>
            Hoffmann et al. fit a parametric loss surface. With dense
            transformer FLOPs approximated by <Formula tex="C \approx 6ND" />,
            the familiar prescription is to scale <Formula tex="N" /> and{" "}
            <Formula tex="D" /> in tandem:
          </p>
          <div className="equation-block">
            <Formula
              display
              tex="L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}},\quad C\approx 6ND"
            />
          </div>
          <p>
            Villalobos et al. bound the practical stock of high-quality human
            tokens near <Formula tex="10^{13}" />–<Formula tex="10^{14}" />{" "}
            depending on quality cuts. Past that ceiling, effective data is
            not inventable by scraping alone:
          </p>
          <div className="equation-block">
            <Formula
              display
              tex="D_{\mathrm{eff}}=D_{\mathrm{human}}+\delta\,D_{\mathrm{synthetic}}"
            />
          </div>
          <p>
            Here <Formula tex="\delta \in [0,1]" /> is a quality multiplier.
            Unfiltered self-imitation behaves like{" "}
            <Formula tex="\delta \ll 1" />; process-filtered trajectories
            (compilers, unit tests, PRMs) push <Formula tex="\delta" /> up.
            The strategic implication: data-wall CapEx is verification
            infrastructure, not more scrapers.
          </p>
        </div>

        <ChinchillaSim />
      </div>
    </section>
  );
}
