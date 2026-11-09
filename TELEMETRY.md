# Agent change telemetry

Readable log of what changed and **why**. Follow this while I work. Auto-hook also appends file paths under `.cursor/hooks/`.

| Time (UTC+1) | Change | Why |
|---|---|---|
| 16:19 | Created `TELEMETRY.md` + Cursor Goal + todos | You asked for telemetry to follow edits |
| 16:19 | Added `.cursor/hooks.json` + `log-edit.sh` | Auto-append each file edit path to this log |
| 16:19 | Baseline: `npm run build` OK; lint warned Footer `Date` impurity; preview 200 | Establish bug baseline |
| 16:20 | Set `REPO_URL` / `.env` → `martinuhor/POW-Triad` | Your GitHub handle; repo not created yet (links 404 until push) |
| 16:20 | Footer: hardcode `© 2026` | Fix oxlint react purity warning |
| 16:21 | Browser QA on `http://127.0.0.1:4173` | Hero renders; GitHub href correct; no JS crash |
| 16:21 | **Bugfix:** wall line used `6·N*·D_eff` / `6·D_eff²` | Wrong C for “data exhaustion wall” under α≠β |
| 16:21 | Aria-labels on Chinchilla sliders | KaTeX in labels was read as letter-by-letter |
| 16:22 | **Bugfix:** `chinchillaOptimalNd` was `N*=D*=√(C/6)` | Inconsistent with Hoffmann α,β → fake **negative** loss penalties |
| 16:22 | Synced Python `model.py` optimum | Keep Streamlit twin + web math aligned |
| 16:22 | Added `dataWallCompute(D_eff)` | Correct wall: solve D*(C)=D_eff for C |
| 16:22 | Updated `site/README.md` deploy docs for martinuhor | Ready for `gh repo create` + CF Pages |

## Still open

- Cloudflare Pages project (after GitHub push)
- Main JS bundle ~1MB (Recharts+KaTeX) — warning only
- Mobile nav menu (desktop links hide &lt;880px)

## How to watch live

1. Open this file: `TELEMETRY.md`
2. Preview site: http://127.0.0.1:4173/
3. Deploy path: GitHub `martinuhor/POW-Triad` → Cloudflare Pages (`site/` root)

| Time (UTC+1) | Change | Why |
|---|---|---|
| 16:25 | Create GitHub repo, first commit, push; CF Pages next | You said the word — ship it |
| 2026-11-09 16:26 | Edited `/Users/mac/POW Triad/.gitignore` | Auto-logged by afterFileEdit hook |
| 2026-11-09 16:26 | Edited `/Users/mac/POW Triad/TELEMETRY.md` | Auto-logged by afterFileEdit hook |
