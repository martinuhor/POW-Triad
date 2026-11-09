export function Synthesis() {
  return (
    <section className="chapter" id="synthesis">
      <div className="chapter-inner prose">
        <p className="chapter-index">03 · Synthesis</p>
        <h2>CapEx as a two-wall portfolio</h2>
        <p className="lede">
          Villalobos-style data limits and Erdil-style physical timelines are
          not rival religions. They are two binding constraints on the same
          objective: minimize loss subject to compute, effective data, and
          watts—then translate capability into tasks the economy can absorb.
        </p>

        <div className="matrix" role="table" aria-label="CapEx decision matrix">
          <div className="matrix-head" role="row">
            <span>Signal</span>
            <span>Prefer CapEx toward</span>
            <span>Hedge</span>
          </div>
          <div className="matrix-row" role="row">
            <span>
              <strong>Data binds first</strong>
              <small>Loss flattens under rising N with fixed unique D</small>
            </span>
            <span>Synthetic verification stack; licensed private corpora</span>
            <span>Land + interconnect options</span>
          </div>
          <div className="matrix-row" role="row">
            <span>
              <strong>Hardware binds first</strong>
              <small>GPUs idle for power; interconnect slips</small>
            </span>
            <span>Grid interconnects, PPAs, cooling, multi-site schedule</span>
            <span>Algorithmic efficiency + higher δ</span>
          </div>
          <div className="matrix-row" role="row">
            <span>
              <strong>Both bind</strong>
              <small>Most likely at the frontier</small>
            </span>
            <span>Barbell: long-lead energy + verification platform</span>
            <span>Mid-training checkpoints; mixed data curricula</span>
          </div>
        </div>

        <h3>Operating principles</h3>
        <ol>
          <li>
            Never train on unfiltered self-imitation at scale—raise{" "}
            <em>δ</em> with process filters.
          </li>
          <li>
            Instrument unique-token growth, megawatts delivered, and idle-GPU
            hours as first-class strategy metrics.
          </li>
          <li>
            Gate major pretrains on a documented verifier regime and a
            diversity / collapse report.
          </li>
        </ol>
      </div>
    </section>
  );
}
