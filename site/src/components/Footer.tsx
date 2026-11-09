const COPYRIGHT_YEAR = 2026;

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div>
          <strong>Proof of Work Triad</strong>
          <p>
            Built as a public AGI strategy / safety portfolio. Simulators run
            entirely client-side for Cloudflare Pages.
          </p>
        </div>
        <div className="footer-meta">
          <span>© {COPYRIGHT_YEAR}</span>
          <a href="#top">Back to top</a>
        </div>
      </div>
    </footer>
  );
}
