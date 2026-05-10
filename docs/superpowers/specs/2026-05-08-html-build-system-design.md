# HTML Build System Design

**Date:** 2026-05-08
**Status:** Approved for implementation
**Scope:** Phase 1 — shell migration (nav, head, footer) into a Nunjucks base template; pillar page content unchanged

---

## Problem

The site's ~45 HTML pages were hand-authored. Over time, three different nav authoring patterns diverged, producing:

- `policyos.html` with a text-only nav and no logo SVG
- `policy-library.html` with 4 hamburger buttons (hand-coded nav plus `app.js` injection on top)
- Inconsistent footer structures across compare pages
- No enforced single source of truth for the nav/footer shell

Every new page is at risk of diverging again. The current `app.js` nav/footer-injection pattern is a footgun: it assumes the page shell is already correct and fails silently when it is not.

---

## Decision

Introduce a Nunjucks-based static build system. A canonical base template (`_base.njk`) owns the entire shell. Per-page source files extend it and supply only their content. The build script renders everything into `docs/`. GitHub Pages deploys from the built output via the official Actions artifact workflow.

This is Phase 1 only. Pillar page content (policy cards, hero sections, etc.) stays as-is in Nunjucks blocks. No content is rewritten.

---

## Directory layout

```
src/
  templates/
    _base.njk          # canonical shell (nav, head, footer, scripts)
  pages/
    index.njk
    policy-library.njk
    get-involved.njk
    about-ai.njk
    pillars/
      healthcare.njk
      ...              # one .njk per pillar
    compare/
      republican-party.njk
      ...              # one .njk per compare page
    policyos.njk       # content block only; generate-policyos.py writes this file
  data/
    nav.json           # shared top nav item list
    footer-links.json  # shared footer link list

scripts/
  build-site.js        # Nunjucks renderer: src/ → docs/
  migrate-to-njk.js    # one-time migration script
  check-html.js        # conformance assertions on docs/
  check-parity.js      # diffs regenerated vs original during migration

docs/                  # build output; committed; GH Pages deploys from here
tests/
  visual/
    visual.spec.js     # Playwright visual regression tests
                       # snapshots stored alongside spec by Playwright default
                       # (tests/visual/visual.spec.js-snapshots/)
```

---

## Section 1: Base template (`_base.njk`)

```nunjucks
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Freedom and Dignity Project{% endblock %}</title>
  {% if description %}
  <meta name="description" content="{{ description | escape }}">
  {% endif %}

  {# Open Graph / Twitter — per-page values override defaults #}
  <meta property="og:type"       content="website">
  <meta property="og:site_name"  content="Freedom and Dignity Project">
  <meta property="og:image"      content="https://alistardust.github.io/freedom-and-dignity-project/og-image.png">
  <meta property="og:image:alt"  content="Freedom and Dignity Project">
  <meta name="twitter:card"      content="summary_large_image">
  <meta name="twitter:image"     content="https://alistardust.github.io/freedom-and-dignity-project/og-image.png">
  <meta property="og:title"      content="{% block og_title %}Freedom and Dignity Project{% endblock %}">
  <meta property="og:description" content="{% block og_description %}An open project to rebuild America's rights, institutions, and economy for everyone.{% endblock %}">
  <meta property="og:url"        content="https://alistardust.github.io/freedom-and-dignity-project/{% block og_url %}{% endblock %}">
  <meta name="twitter:title"     content="{% block twitter_title %}Freedom and Dignity Project{% endblock %}">
  <meta name="twitter:description" content="{% block twitter_description %}An open project to rebuild America's rights, institutions, and economy for everyone.{% endblock %}">

  <link rel="icon" href="{{ base }}favicon.ico">
  <link rel="stylesheet" href="{{ base }}assets/css/style.css">

  {% block head_extra %}{% endblock %}
</head>
<body class="{{ body_class | default('') }}">
<a href="#main-content" class="skip-link sr-only focusable">Skip to main content</a>

<nav class="site-nav" aria-label="Site navigation">
  <div class="nav-inner">
    <a href="{{ base }}index.html" class="nav-brand">
      <img src="{{ base }}assets/img/logo.svg"
           alt="Freedom and Dignity Project seal" width="36" height="36">
      <span class="nav-wordmark">Freedom and Dignity<span>Project</span></span>
    </a>
    <ul class="nav-links">
      {% for item in nav %}
      <li>
        <a href="{{ base }}{{ item.href }}"
           {% if currentPage == item.href %}aria-current="page"{% endif %}>
          {{ item.label }}
        </a>
      </li>
      {% endfor %}
    </ul>
    <button type="button" class="nav-hamburger" aria-label="Open site menu"
            aria-expanded="false" aria-controls="site-tree">&#9776;</button>
  </div>
</nav>

{# Static placeholder — app.js populates this element rather than creating a new one #}
<nav id="site-tree" class="site-tree" hidden aria-label="Site menu"></nav>

<main id="main-content">
  {% block content %}{% endblock %}
</main>

<footer class="site-footer">
  <div class="wrap">
    <span class="footer-brand">Freedom and Dignity Project</span>
    <ul class="footer-links">
      {% for item in footerLinks %}
      <li><a href="{{ base }}{{ item.href }}">{{ item.label }}</a></li>
      {% endfor %}
    </ul>
    <span class="footer-note">
      Freedom and Dignity Project &middot;
      <a href="{{ base }}about-ai.html" class="footer-ai-link">On the Use of AI</a>
    </span>
  </div>
</footer>

<script src="{{ base }}assets/js/data.js" defer></script>
<script src="{{ base }}assets/js/app.js" defer></script>
</body>
</html>
```

### Key decisions

**Nav links rendered statically** from `src/data/nav.json`. `app.js` handles behavior only (hamburger toggle, active-link `.active` class, mobile tree menu). This eliminates the runtime injection footgun.

**`aria-current="page"` set at build time** by comparing `currentPage` to each nav item's `href`. For pages that are not themselves nav destinations (pillar pages, compare pages), no nav item is marked active at build time. `app.js` can still add `.active` class at runtime via URL comparison for these pages.

**Active link class is `.active`** throughout — this matches the existing CSS selectors (`.nav-links a.active`) and e2e test assertions. Do not rename to `.is-active`. `aria-current="page"` is the semantic accessibility attribute set at build time; `.active` is the visual CSS class always set by `app.js` at runtime. For nav-destination pages, both will be present, set independently from different mechanisms.

**`#site-tree` is a static `<nav>` placeholder** in the shell. The element must be `<nav>` (not `<div>`) to be semantically correct for the role it plays. `app.js` `buildPanel()` is rewritten to:
1. Find the existing element: `const panel = document.getElementById('site-tree')`
2. Populate it (append `st-header`, `st-root`, `ul[role="tree"]`) rather than creating a new element
3. Remove the `hidden` attribute when populating the panel (`panel.removeAttribute('hidden')`); visibility continues to be toggled via `.st-open` class as before — no CSS changes needed (`.site-tree.st-open` already defined in `style.css`)
4. The `burger.setAttribute('aria-controls', 'site-tree')` line in app.js is removed (it is now in static HTML)
5. The overlay (`div.site-overlay`) continues to be created and appended to `document.body` by app.js — this is fine since it is purely presentational

**`<main id="main-content">`** wraps the content block in the shell so skip links always work and pages cannot omit it.

**`base` computed from output path depth** in `build-site.js`:
```js
const depth = outputPath.replace(/^docs\//, '').split('/').length - 1;
const base = '../'.repeat(depth);
```
Root pages (`docs/*.html`) → `base = ""`. One-level subdir (`docs/pillars/*.html`) → `base = "../"`. Generic: a third level would produce `"../../"` automatically.

**`description` is conditional** — the meta tag is omitted rather than rendered empty. The build script emits a non-fatal warning for any public page missing a description.

**Footer links rendered statically** from `src/data/footer-links.json`. `app.js` footer-injection code is removed entirely. The inline `style="color:inherit;opacity:.7"` on the AI disclosure link moves to a CSS class `.footer-ai-link` in `style.css`.

**OG/Twitter meta** has site-level defaults in the base template. Per-page pages override using `{% block og_title %}`, `{% block og_description %}`, `{% block og_url %}`, `{% block twitter_title %}`, `{% block twitter_description %}` blocks. The OG image is a site-level constant (same image for all pages).

**`defer`** on both script tags.

### Initial `src/data/nav.json`

```json
[
  { "href": "index.html",       "label": "Home" },
  { "href": "problem.html",     "label": "Problem" },
  { "href": "approach.html",    "label": "Approach" },
  { "href": "get-involved.html","label": "Get Involved" }
]
```

### Initial `src/data/footer-links.json`

```json
[
  { "href": "index.html",          "label": "Home" },
  { "href": "platform.html",       "label": "Platform" },
  { "href": "policy-library.html", "label": "Policy Library" },
  { "href": "problem.html",        "label": "Problem" },
  { "href": "approach.html",       "label": "Approach" },
  { "href": "rights.html",         "label": "Rights" },
  { "href": "get-involved.html",   "label": "Get Involved" },
  { "href": "roadmap.html",        "label": "Roadmap" },
  { "href": "about-us.html",       "label": "About" },
  { "href": "compare/index.html",  "label": "Perspectives" },
  { "href": "about-ai.html",       "label": "About AI" }
]
```

### Page file pattern

```nunjucks
{% extends "_base.njk" %}
{% set description = "Our healthcare policy positions." %}
{% set body_class = "pillar pillar-healthcare" %}

{% block title %}Healthcare — Freedom and Dignity Project{% endblock %}
{% block og_title %}Healthcare — Freedom and Dignity Project{% endblock %}
{% block og_description %}Our healthcare policy positions.{% endblock %}
{% block og_url %}pillars/healthcare.html{% endblock %}
{% block twitter_title %}Healthcare — Freedom and Dignity Project{% endblock %}
{% block twitter_description %}Our healthcare policy positions.{% endblock %}

{% block content %}
  ... existing page HTML, unchanged ...
{% endblock %}
```

### Intermediate templates

`_pillar.njk` and `_compare.njk` extending `_base.njk` are deferred to Phase 2. In Phase 1, all pages extend `_base.njk` directly.

---

## Section 2: Build script (`scripts/build-site.js`)

### Responsibilities

1. Load `src/data/nav.json` and `src/data/footer-links.json`
2. Configure Nunjucks with a `FileSystemLoader` pointing at **both** `src/templates` and `src/pages` (in that order). This lets `env.render('pillars/healthcare.njk', context)` resolve page files via the second path while `{% extends "_base.njk" %}` resolves via the first. Configure with `autoescape: false` — content blocks contain raw HTML and must not be entity-escaped. Example:
   ```js
   const env = new nunjucks.Environment(
     new nunjucks.FileSystemLoader(['src/templates', 'src/pages']),
     { autoescape: false }
   );
   ```
3. For each `src/pages/**/*.njk`:
   - Compute output path under `docs/` (mirror directory structure, `.njk` → `.html`)
   - Compute `base` from output path depth: `'../'.repeat(depth)`
   - Compute `currentPage` as the output filename relative to `docs/` (e.g. `problem.html`, `pillars/healthcare.html`)
   - Render with Nunjucks, passing `{ nav, footerLinks, base, currentPage }`
   - Write to `docs/`
4. Emit a warning (non-fatal) for any page where `description` is not set
5. Exit non-zero if any render fails

### New npm scripts (to be added to `package.json`)

```json
"build":       "node scripts/build-site.js",
"check:html":  "node scripts/check-html.js",
"check:parity":"node scripts/check-parity.js",
"test:visual": "playwright test tests/visual/visual.spec.js",
"test:visual:update": "playwright test tests/visual/visual.spec.js --update-snapshots"
```

### New dependencies (to be added to `package.json`)

```json
"devDependencies": {
  "nunjucks": "^3.2.4",
  "parse5": "^7.0.0"
}
```

`serve` is already installed. Playwright is already installed.

---

## Section 3: CI workflow

### Prerequisites (must be done before the new workflow is merged)

1. **Switch GitHub Pages source to "GitHub Actions":** Repository Settings > Pages > Source = "GitHub Actions". If this step is omitted before the workflow is merged, the deploy job will succeed but GitHub Pages will not update.

### Workflow file

New file: `.github/workflows/build-and-deploy.yml`

The existing `.github/workflows/tests.yml` is retained. It continues to run unit and e2e tests. The new workflow adds build, conformance, and deploy steps. Visual regression tests are added to the new workflow's build job (see Section 4).

### Trigger and concurrency

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: pages-${{ github.ref }}
  cancel-in-progress: true
```

### `build` job

```yaml
build:
  runs-on: ubuntu-latest
  permissions:
    contents: read
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: npm
    - run: npm ci
    - run: npx playwright install firefox --with-deps
    - run: npm run build
    - run: |
        git diff --exit-code -- docs/ ':!docs/superpowers/'
        git ls-files --others --exclude-standard docs/ | grep -v '^docs/superpowers/' | grep . && exit 1 || true
      # fail if docs/ (excluding docs/superpowers/) is stale or has untracked new files
    - run: npm run check:html
    - run: npm run test:visual          # visual regression (see Section 4)
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: visual-regression-diffs
        path: test-results/            # Playwright default outputDir for diffs
    - uses: actions/upload-pages-artifact@v3
      with:
        path: docs/
```

### `deploy` job (runs only on push to `main`)

```yaml
deploy:
  needs: build
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  environment:
    name: github-pages
    url: ${{ steps.deployment.outputs.page_url }}
  permissions:
    pages: write
    id-token: write
  steps:
    - id: deployment
      uses: actions/deploy-pages@v4
```

### `docs/` freshness strategy

`docs/` remains committed to the repo as the verified, reviewable build output. Contributors must run `npm run build` locally before committing any changes to `src/`. CI enforces this with a two-step check scoped to exclude `docs/superpowers/` (which contains hand-authored specs and plans, not build output): `git diff --exit-code -- docs/ ':!docs/superpowers/'` (catches modified tracked files) and a filtered `git ls-files --others` pipe (catches new untracked files outside `docs/superpowers/`). If either check fails, the build fails and no artifact is uploaded. This eliminates the "CI commits back to the repo" footgun entirely.

### Conformance check (`npm run check:html` → `scripts/check-html.js`)

Scans every `.html` file in `docs/` (excluding `docs/superpowers/`) and asserts the following. Any violation exits non-zero and prints the offending file and failed assertion.

| Assertion | Expected |
|---|---|
| `<nav class="site-nav">` | Exactly 1 |
| `<main id="main-content">` | Exactly 1 |
| `<footer class="site-footer">` | Exactly 1 |
| `<button class="nav-hamburger">` | Exactly 1 |
| `<nav id="site-tree">` | Exactly 1 |
| `<ul class="nav-links">` with children | Not empty |
| `<ul class="footer-links">` with children | Not empty |
| `<meta name="description" content="">` | Must not exist |

Additionally, a source-level lint over `src/pages/**/*.njk` rejects any file containing `<nav class="site-nav">`, `<footer class="site-footer">`, or `<script src=` — enforcing that page sources never hand-author shell structure.

---

## Section 4: Visual regression testing

### Tool

Playwright (`tests/visual/visual.spec.js`), using the existing Playwright install and Firefox configuration. Playwright's `toHaveScreenshot()` handles pixel diffing. Snapshots are stored alongside the spec file in `tests/visual/visual.spec.js-snapshots/` (Playwright's default; do not override `snapshotDir`).

### Server

The existing `playwright.config.js` already defines:

```js
webServer: {
  command: 'npx serve docs -p 5500 -n',
  url: 'http://localhost:5500',
  reuseExistingServer: !process.env.CI,
},
use: { baseURL: 'http://localhost:5500' }
```

Visual tests use this config. `npx serve docs -p 5500 -n` serves `docs/` as the filesystem root — there is no `/freedom-and-dignity-project/` path prefix in the local dev server. That prefix only exists on GitHub Pages. All test paths are relative to `http://localhost:5500` directly.

### Baseline pages and viewports

Ten screenshots: five pages at two viewports each.

| Page | Path |
|---|---|
| Home | `/` |
| Healthcare pillar | `/pillars/healthcare.html` |
| Republican party compare | `/compare/republican-party.html` |
| PolicyOS | `/policyos.html` |
| Policy Library | `/policy-library.html` |

Viewports: desktop (1280×800) and mobile (390×844).

### Threshold

`0.1%` pixel difference (default `maxDiffPixelRatio: 0.001` in `toHaveScreenshot()`). Tight enough to catch real regressions; tolerant enough for minor antialiasing differences between CI and local.

### Baseline workflow

Snapshots must be generated on Linux (ubuntu-latest) to match CI. Playwright appends the OS to snapshot filenames by default (`-linux.png`, `-darwin.png`); snapshots committed from macOS will never match CI and cause permanent "missing snapshot" failures.

- Snapshots committed at `tests/visual/visual.spec.js-snapshots/`
- **To establish or update baselines:** run `npm run test:visual:update` in a CI environment (ubuntu-latest), not locally on macOS. The simplest path: push a branch, trigger CI manually with `--update-snapshots`, download the artifact, commit the new snapshots.
- On every PR, CI runs `npm run test:visual` and diffs against committed snapshots
- Diff exceeding threshold → CI fails; diff images uploaded as CI artifact

### What it catches

Layout breakage, missing logo, footer structure changes, hero section collapse, text going invisible (contrast failures like those seen in the triggering bug reports).

---

## Section 5: Migration strategy

### Approach

A one-time migration script (`scripts/migrate-to-njk.js`) does the mechanical conversion:

1. For each `.html` file in `docs/` (skipping all files under `docs/superpowers/`):
   - Strip `<html>`, `<head>`, `<nav class="site-nav">`, `<footer class="site-footer">`, and `<script>` boilerplate
   - Extract `<title>` text into `{% block title %}`
   - Extract description meta content into `{% set description = '...' %}`
   - Wrap remaining body content in `{% extends "_base.njk" %}` and `{% block content %}`
   - Write to the corresponding path under `src/pages/` with `.njk` extension
2. **Edge case handling:** if the script cannot unambiguously identify the shell boundaries in a page (e.g. `policyos.html` with a non-standard nav, `policy-library.html` with duplicate navs), it skips that file, prints a warning, and continues. Skipped files are migrated manually.
3. Run `npm run build` to regenerate `docs/`
4. Run `npm run check:parity` to diff each regenerated file against the original

### Parity check (`scripts/check-parity.js`)

- Parses both files with `parse5` as DOM trees
- Compares element structure (tag names, ids, classes, text content) — not whitespace or attribute ordering
- Exits non-zero if structural differences are found
- Prints: file path + a list of elements present in one file but not the other
- Whitespace-only differences are not flagged

### Migration order

1. Root pages (`index.html`, `policy-library.html`, `get-involved.html`, etc.) — highest traffic, easiest to verify manually
2. Compare pages — structurally uniform, easy to batch
3. Pillar pages (~22) — most numerous, also structurally uniform
4. Generated pages — update generators last (see below)

### Generator scripts (`generate-policyos.py` etc.)

Currently these write complete HTML files. After migration they write only the content block for their `.njk` file. Example of what `generate-policyos.py` would write to `src/pages/policyos.njk`:

```nunjucks
{% extends "_base.njk" %}
{% set description = "The PolicyOS framework — the cross-platform rules layer for all Freedom and Dignity policy." %}
{% set body_class = "policyos" %}
{% block title %}PolicyOS — Freedom and Dignity Project{% endblock %}
{% block og_title %}PolicyOS — Freedom and Dignity Project{% endblock %}
{% block og_url %}policyos.html{% endblock %}
{% block content %}
<section class="pos-hero">
  ... generated hero HTML ...
</section>
<section class="pos-families">
  ... generated families HTML ...
</section>
{% endblock %}
```

The generator reads from the DB, builds the content sections, and writes this file. `npm run build` is then run to produce `docs/policyos.html`.

### `app.js` changes

After migration, `app.js` loses its nav-injection and footer-injection responsibilities. Retained:

- Hamburger toggle: finds `document.getElementById('site-tree')` (already in DOM), populates it if empty, manages `aria-expanded`, toggles visibility
- `buildPanel()` rewrite: find existing `#site-tree` element, append `st-header`, `st-root`, `ul[role="tree"]` to it; do not create a new element
- Overlay: `div.site-overlay` continues to be created and appended to `document.body` by app.js (purely presentational, this is fine)
- Active-link `.active` class: reads current URL, compares to nav link hrefs, adds `.active` class (handles clean URL / no-.html-extension environments on GH Pages)
- Mobile tree menu behavior
- Dynamic value rendering (`data-dynamic` spans for policy/pillar counts)
- Section sub-nav highlighting (pillar and compare pages)
- All other page-behavior logic unrelated to shell structure

Removed from `app.js`:
- All nav link injection code (the `navList.appendChild` block)
- All footer link injection code (the `footerLinks.appendChild` block)
- `burger.setAttribute('aria-controls', 'site-tree')` — now in static HTML
- Skip link injection — now in static HTML

### Atomicity

`docs/` is always either the old hand-authored files or the freshly built files. The switch happens in a single commit that adds all `src/` source files and updates all `docs/` output files simultaneously. There is no intermediate state where `docs/` is partially migrated.

### `.footer-ai-link` CSS class

The inline `style="color:inherit;opacity:.7"` on the AI disclosure link in the footer moves to a CSS class. Add to `style.css`:

```css
.footer-ai-link {
  color: inherit;
  opacity: .7;
}
```

### Adding new pages after migration

Create `src/pages/newpage.njk` extending `_base.njk`. Run `npm run build`. Commit both the `.njk` source and the updated `docs/newpage.html` together. CI's freshness check will catch a missing build step if only one is committed.

---

- Intermediate templates (`_pillar.njk`, `_compare.njk`)
- Generating policy card HTML from the database
- Changing pillar page content structure
- CSS changes other than `.footer-ai-link` above

---

## Success criteria

All are verifiable by automated check or manual inspection:

1. `npm run check:html` passes on every file in `docs/` (0 violations)
2. `npm run check:html` source-level lint passes on every file in `src/pages/` (no hand-authored shell elements)
3. `git diff --exit-code -- docs/ ':!docs/superpowers/'` passes after `npm run build` (docs/ build output is never stale)
4. Visual regression baselines established for all 5 page types at 2 viewports; `npm run test:visual` passes
5. `npm run test:unit` passes (all tests)
6. `npm run test:e2e` passes (all existing assertions)
7. CI build + conformance + visual regression runs on every PR; deploy runs on push to main
8. GH Pages deploys from Actions artifact (not branch)
9. No `<nav class="site-nav">`, `<footer class="site-footer">`, or `<script src=` in any `src/pages/*.njk` file
10. `generate-policyos.py` writes to `src/pages/policyos.njk` (content block only); full HTML is built by `npm run build`
