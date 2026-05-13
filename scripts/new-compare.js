#!/usr/bin/env node
/**
 * new-compare.js — Scaffold a new platform comparison page.
 *
 * Usage:
 *   node scripts/new-compare.js \
 *     --id party-or-platform-id \
 *     --party "Full Party Name" \
 *     --color "#336699" \
 *     --tagline "One-sentence description of the platform."
 *
 * Writes docs/compare/<id>.html and prints next steps.
 * After generating, add the page to docs/compare/index.html manually.
 */

// ⚠️  BYPASS WARNING: This script writes a complete HTML file directly to docs/.
// After the Nunjucks migration (Phase 1), this script must be updated to write
// src/pages/compare/<id>.njk (a content-block .njk, not full HTML) and call
// 'npm run build'. Until updated, do not run this script after migration —
// it will produce a page without the canonical _base.njk shell.
// Tracked in: GitHub issue #1

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Parse CLI args ─────────────────────────────────────────────────────────────
const args = {};
process.argv.slice(2).forEach((arg, i, arr) => {
  if (arg.startsWith('--')) {
    const next = arr[i + 1];
    args[arg.slice(2)] = (next && !next.startsWith('--')) ? next : true;
  }
});

if (args.help) {
  console.log(`Usage:
  node scripts/new-compare.js \\
    --id <slug>          # e.g. green-party
    --party "Name"       # e.g. "Green Party"
    --color "#hex"       # brand/accent color for the page
    --tagline "..."      # one-sentence description shown in hero

Optional:
  --help               Show this help message
`);
  process.exit(0);
}

if (!args.help) {
  const required = ['id', 'party', 'color', 'tagline'];
  const missing  = required.filter(k => !args[k]);
  if (missing.length) {
    console.error(`Missing required arguments: ${missing.map(k => '--' + k).join(', ')}`);
    console.error('Run with --help for usage.');
    process.exit(1);
  }
}

const { party, color, tagline } = args;
const slug      = args.id.toLowerCase().replace(/[^a-z0-9-]/g, '-');
const outputDir = path.resolve(__dirname, '../docs/compare');
const outFile   = path.join(outputDir, `${slug}.html`);

if (fs.existsSync(outFile)) {
  console.error(`File already exists: ${outFile}`);
  console.error('Delete it first if you want to regenerate.');
  process.exit(1);
}

// ── Scaffold ───────────────────────────────────────────────────────────────────
const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${party} vs. Freedom and Dignity — Freedom and Dignity Project</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

<nav class="site-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-brand">
      <img src="../assets/img/logo.svg" alt="Freedom and Dignity Project seal">
      <span class="nav-wordmark">Freedom and Dignity<span>Project</span></span>
    </a>
    <button class="nav-hamburger" aria-label="Menu">☰</button>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="../policy/index.html">Policy Areas</a></li>
      <li><a href="index.html" class="active">Perspectives</a></li>
    </ul>
  </div>
</nav>

<div class="page-hero">
  <div class="wrap">
    <div class="hero-logo-wrap"><img src="../assets/img/logo.svg" alt="Freedom and Dignity Project seal" style="width:80px;height:80px;"></div>
    <p class="hero-eyebrow">Platform Comparison</p>
    <h1 class="hero-title">${party}</h1>
    <p class="hero-statement">${tagline}</p>
  </div>
</div>

<div class="cmp-scorecard bg-dark on-dark">
  <div class="wrap">
    <div class="cmp-score"><div class="cmp-score-n">—</div><div class="cmp-score-label">Policy Areas Aligned</div></div>
    <div class="cmp-score"><div class="cmp-score-n">—</div><div class="cmp-score-label">Key Divergences</div></div>
    <div class="cmp-score"><div class="cmp-score-n">—</div><div class="cmp-score-label">Where They Exceed Us</div></div>
    <div class="cmp-score"><div class="cmp-score-n">—</div><div class="cmp-score-label">Coverage Gaps</div></div>
  </div>
</div>

<nav class="cmp-snav" aria-label="Jump to section">
  <div class="cmp-snav-inner">
    <a href="#cmp-overview">Overview</a>
    <a href="#cmp-align">Common Ground</a>
    <a href="#cmp-diff">Where We Differ</a>
    <a href="#cmp-gaps">Coverage Analysis</a>
    <a href="#cmp-strengths">What They Get Right</a>
    <a href="#cmp-wrongs">Our Perspective</a>
    <a href="#cmp-sources">Sources</a>
  </div>
</nav>

<section class="bg-parchment" id="cmp-overview">
  <div class="wrap">
    <p class="eyebrow">Overview</p>
    <h2>Platform at a Glance</h2>
    <p><!-- TODO: Write 2–3 paragraph overview of ${party}'s platform and positioning. Cite sources. --></p>
  </div>
</section>

<section class="bg-white" id="cmp-align">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">Common Ground</p>
    <h2>Where We Agree</h2>
    <!-- TODO: Add cmp-agree-item blocks for areas of alignment. -->
    <div class="cmp-agree-item">
      <strong><!-- Area of agreement --></strong>
      <p><!-- Description of shared position --></p>
    </div>
  </div>
</section>

<section class="bg-parchment" id="cmp-diff">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">Where We Differ</p>
    <h2>Key Divergences</h2>
    <!-- TODO: Add cmp-diff-item blocks. -->
    <div class="cmp-diff-item">
      <strong><!-- Point of divergence --></strong>
      <p><!-- Explanation of the difference --></p>
    </div>
  </div>
</section>

<section class="bg-white" id="cmp-gaps">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">Coverage Analysis</p>
    <h2>Policy Area by Policy Area</h2>
    <div class="cov-legend">
      <span class="cov-key cov-match">Full Match</span>
      <span class="cov-key cov-partial">Partial</span>
      <span class="cov-key cov-diff">Addressed Differently</span>
      <span class="cov-key cov-none">Not Covered</span>
    </div>
    <div class="cov-table">
      <!-- TODO: Add one cov-row per policy area. Use cov-level classes: cov-match, cov-partial, cov-diff, cov-none -->
      <!--
      <div class="cov-row">
        <div class="cov-policy-area">Policy Area Name</div>
        <div class="cov-level cov-partial">Partial Match</div>
        <div class="cov-gap">Explanation of gap or alignment.</div>
      </div>
      -->
    </div>
  </div>
</section>

<section class="bg-parchment" id="cmp-strengths">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">What They Get Right</p>
    <h2>Where ${party} Leads</h2>
    <!-- TODO: Honest assessment of where this platform exceeds ours or has stronger specifics. -->
    <ul>
      <li><!-- Strength 1 --></li>
    </ul>
  </div>
</section>

<section class="bg-white" id="cmp-wrongs">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">Our Perspective</p>
    <h2>Where We Part Ways</h2>
    <!-- TODO: Core critiques of this platform from the Freedom and Dignity perspective. -->
    <p><!-- Main critique paragraph --></p>
  </div>
</section>

<section class="bg-parchment" id="cmp-sources">
  <div class="wrap">
    <p class="eyebrow">Sources</p>
    <h2>References</h2>
    <ol class="footnotes">
      <!-- TODO: Add APA 7th edition references.
      <li id="fn1"><a href="#ref1">↩</a> Author, A. (Year). Title. Publisher. URL</li>
      -->
    </ol>
  </div>
</section>

<footer class="site-footer">
  <div class="wrap">
    <span class="footer-brand">Freedom and Dignity Project</span>
    <ul class="footer-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="../policy/index.html">Policy Areas</a></li>
      <li><a href="index.html">Perspectives</a></li>
    </ul>
    <span class="footer-note">A Third Bill of Rights for the 21st Century. · <a href="../about-ai.html" style="color:inherit;opacity:.7">On the Use of AI</a></span>
  </div>
</footer>

</body>
</html>
`;

fs.writeFileSync(outFile, html, 'utf8');

// ── Next steps ────────────────────────────────────────────────────────────────
console.log(`
✅  Created: docs/compare/${slug}.html

Next steps:
  1. Fill in the TODO sections in the generated file
  2. Update the scorecard numbers (Policy Areas Aligned, Key Divergences, etc.)
  3. Add policy-area-by-policy-area cov-row entries in the #cmp-gaps section
  4. Add all APA 7th edition footnotes in #cmp-sources
  5. Add a link card to docs/compare/index.html:

     <a href="${slug}.html" class="cmp-card">
       <span class="cmp-card-name">${party}</span>
       <span class="cmp-card-desc">${tagline}</span>
     </a>

  6. Add the new page to SAMPLE_POLICY_AREAS (or a compare-page test) in tests/e2e/site.spec.js
  7. Run: npm run test:unit && npm run test:e2e
`);
