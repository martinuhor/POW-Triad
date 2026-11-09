# POW Triad — Digital Dissertation Site

Interactive monograph for the Proof-of-Work Triad: Chinchilla / data-exhaustion and Acemoglu task→GDP simulators embedded in a first-class essay for Cloudflare Pages.

## Local development

```bash
cd site
npm install
npm run dev
```

Open the printed local URL (usually `http://localhost:5173`).

## Production build

```bash
cd site
npm run build
npm run preview
```

Output is static in `dist/` — ready for Cloudflare Pages.

## Configure GitHub links

Set the repo URL used by nav + artifact links:

```bash
# .env (optional)
VITE_REPO_URL=https://github.com/martinuhor/POW-Triad
```

Default in `src/config.ts` already points at `martinuhor/POW-Triad`.

## Deploy to GitHub → Cloudflare Pages

### 1. Create empty repo + push monorepo

```bash
# from repo root (requires gh auth)
gh repo create martinuhor/POW-Triad --public --source=. --remote=origin --push
```

Or manually: create `POW-Triad` under **martinuhor** on GitHub, then:

```bash
git add .
git commit -m "Add POW Triad dissertation site with embedded simulators"
git remote add origin https://github.com/martinuhor/POW-Triad.git
git push -u origin main
```

### 2. Cloudflare Pages

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Select `POW-Triad`
3. Build settings:
   - **Framework preset:** Vite
   - **Root directory:** `site`
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
4. Environment variable: `VITE_REPO_URL=https://github.com/martinuhor/POW-Triad`
5. Deploy

CLI alternative (after `npx wrangler login`):

```bash
cd site
npm run build
npx wrangler pages deploy dist --project-name=pow-triad
```

## What’s on the page

| Section | Content |
|---|---|
| Hero | Brand + full-bleed loss-wall visualization |
| Thesis | Two walls, one objective |
| Ch. 1 | Data wall essay + live Chinchilla simulator |
| Ch. 2 | Macro lag essay + live GDP simulator |
| Synthesis | CapEx decision matrix |
| Artifacts | Links to code / memos on GitHub |

Simulators are pure client-side TypeScript (ported from `simulators/*/model.py`) — no Streamlit runtime required on Pages.
