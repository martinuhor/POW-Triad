import { useEffect, useState } from "react";
import { REPO_URL } from "../config";

const LINKS = [
  { href: "#thesis", label: "Thesis" },
  { href: "#data-wall", label: "Data Wall" },
  { href: "#macro", label: "Macro Lag" },
  { href: "#synthesis", label: "Synthesis" },
  { href: "#artifacts", label: "Artifacts" },
];

export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`site-nav${scrolled ? " is-scrolled" : ""}`}>
      <a className="nav-brand" href="#top">
        <span className="nav-mark" aria-hidden="true" />
        <span>POW Triad</span>
      </a>
      <nav className="nav-links" aria-label="Primary">
        {LINKS.map((l) => (
          <a key={l.href} href={l.href}>
            {l.label}
          </a>
        ))}
      </nav>
      <a
        className="nav-cta"
        href={REPO_URL}
        target="_blank"
        rel="noreferrer"
        title="Repository (create on GitHub if 404)"
      >
        GitHub
      </a>
    </header>
  );
}
