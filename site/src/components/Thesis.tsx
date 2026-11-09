import { motion } from "framer-motion";
import { Formula } from "./Formula";

export function Thesis() {
  return (
    <section className="chapter" id="thesis">
      <div className="chapter-inner prose">
        <p className="chapter-index">00 · Abstract</p>
        <motion.h2
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          Two walls, one objective function
        </motion.h2>
        <p className="lede">
          Frontier scaling is usually narrated as a race in floating-point
          operations. That race is real—but incomplete. The next decade of
          capability and economic impact is jointly constrained by a{" "}
          <strong>data wall</strong> (finite high-quality human tokens), a{" "}
          <strong>hardware wall</strong> (watts, interconnects, fab lead
          times), and a <strong>macro lag</strong> between laboratory
          performance and measured TFP/GDP.
        </p>
        <p>
          This monograph presents the argument as a proof-of-work portfolio:
          executable math you can manipulate, not a slide deck of vibes. The
          first laboratory maps Hoffmann et al.&apos;s Chinchilla allocation{" "}
          <Formula tex="C \approx 6ND" /> against Villalobos-style exhaustion
          bounds. The second implements an Acemoglu-style task model where
          exposure, cost savings, and capital drag decide how much digital
          progress shows up in national accounts.
        </p>
        <blockquote>
          Claim. CapEx that funds only compute—or only scrapers—will discover
          the unfunded wall on the critical path. The firms that compound
          through 2026–2030 look boringly dual-stack: verification-rich
          synthetic data <em>and</em> grid-realistic power.
        </blockquote>
      </div>
    </section>
  );
}
