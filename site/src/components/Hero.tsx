import { motion } from "framer-motion";
import { HeroCurve } from "./HeroCurve";

export function Hero() {
  return (
    <section className="hero" id="top" aria-labelledby="hero-brand">
      <div className="hero-plane" aria-hidden="true">
        <HeroCurve />
        <div className="hero-veil" />
      </div>

      <div className="hero-copy">
        <motion.p
          className="hero-kicker"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        >
          Digital dissertation · November 2026
        </motion.p>

        <motion.h1
          id="hero-brand"
          className="hero-brand"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.85, delay: 0.08, ease: [0.22, 1, 0.36, 1] }}
        >
          Proof of Work Triad
        </motion.h1>

        <motion.p
          className="hero-lede"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.85, delay: 0.18, ease: [0.22, 1, 0.36, 1] }}
        >
          Where Chinchilla scaling meets the human-data ceiling—and why
          laboratory capability still lags measured GDP.
        </motion.p>

        <motion.div
          className="hero-actions"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          <a className="btn btn-primary" href="#data-wall">
            Open the simulators
          </a>
          <a className="btn btn-ghost" href="#thesis">
            Read the thesis
          </a>
        </motion.div>
      </div>
    </section>
  );
}
