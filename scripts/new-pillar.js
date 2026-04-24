#!/usr/bin/env node
/**
 * new-pillar.js — Scaffold a new pillar HTML page from the canonical template.
 *
 * Usage:
 *   node scripts/new-pillar.js \
 *     --id my-pillar-name \
 *     --title "My Pillar Title" \
 *     --foundation freedom-to-thrive \
 *     --color "#1a6b8a" \
 *     --prefix "MPL"
 *
 * The script writes docs/pillars/<id>.html and prints next steps.
 * After generating, register the pillar in docs/assets/js/data.js.
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── Parse CLI args ─────────────────────────────────────────────────────────────
const args = {};
process.argv.slice(2).forEach((arg, i, arr) => {
  if (arg.startsWith('--')) args[arg.slice(2)] = arr[i + 1];
});

const required = ['id', 'title', 'foundation', 'color', 'prefix'];
const missing  = required.filter(k => !args[k]);
if (missing.length) {
  console.error(`Missing required arguments: ${missing.map(k => '--' + k).join(', ')}`);
  console.error('Run with --help for usage.');
  process.exit(1);
}

const { id, title, foundation, color, prefix } = args;
const slug      = id.toLowerCase().replace(/[^a-z0-9-]/g, '-');
const outputDir = path.resolve(__dirname, '../docs/pillars');
const outFile   = path.join(outputDir, `${slug}.html`);

if (fs.existsSync(outFile)) {
  console.error(`File already exists: ${outFile}`);
  console.error('Delete it first if you want to regenerate.');
  process.exit(1);
}

// ── Foundation metadata (keep in sync with data.js) ───────────────────────────
const FOUNDATIONS = {
  'accountable-power':  { label: 'Accountable Power',   roman: 'I',   color: '#bf0a30' },
  'clean-democracy':    { label: 'Clean Democracy',      roman: 'II',  color: '#2471a3' },
  'equal-justice':      { label: 'Equal Justice',        roman: 'III', color: '#1e8449' },
  'real-freedom':       { label: 'Real Freedom',         roman: 'IV',  color: '#7d3c98' },
  'freedom-to-thrive':  { label: 'Freedom to Thrive',    roman: 'V',   color: '#1a6b8a' },
};
const fnd = FOUNDATIONS[foundation];
if (!fnd) {
  console.error(`Unknown foundation "${foundation}". Valid values: ${Object.keys(FOUNDATIONS).join(', ')}`);
  process.exit(1);
}

// ── Generate HTML ──────────────────────────────────────────────────────────────
const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title} — Freedom and Dignity Project</title>
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="icon" type="image/svg+xml" href="../assets/img/logo.svg">
<!-- Per-pillar accent color — only this block should remain inline -->
<style>:root { --accent-color: ${color}; }</style>
</head>
<body>

<!-- ═══ NAV (static shell; links injected by app.js) ═══ -->
<nav class="site-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-brand">
      <img src="../assets/img/logo.svg" alt="Freedom and Dignity Project seal" width="36" height="36">
      <span class="nav-wordmark">Freedom and Dignity<span>Project</span></span>
    </a>
    <button class="nav-hamburger" aria-label="Menu">☰</button>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="index.html" class="active">Pillars</a></li>
      <li><a href="../compare/index.html">Perspectives</a></li>
    </ul>
  </div>
</nav>

<!-- ═══ PILLAR SECTION NAV ═══ -->
<nav class="pil-snav" id="pil-snav">
  <ul>
    <li><a href="#pil-intro">Overview</a></li>
    <li><a href="#pil-problem">The Problem</a></li>
    <li><a href="#pil-reform">Reform Areas</a></li>
    <li><a href="#pil-policy">Policy Positions</a></li>
    <li><a href="#pil-research">Research</a></li>
    <li><a href="#pil-refs">References</a></li>
    <li><a href="#pil-related">Related</a></li>
  </ul>
</nav>

<!-- ═══ HERO ═══ -->
<div class="page-hero on-dark" style="background:var(--navy);padding:3rem 0 2.5rem;">
  <div class="wrap">
    <a href="../foundations.html#${foundation}" style="color:rgba(255,255,255,.6);text-decoration:none">
      Foundation ${fnd.roman}: ${fnd.label}
    </a>
    <h1 style="color:#fff;margin:.4rem 0 .8rem">${title}</h1>
    <p class="hero-statement" style="font-size:1rem;max-width:680px;margin:0 auto">
      <!-- TODO: one-sentence mission statement for this pillar -->
    </p>
  </div>
</div>

<!-- ═══ INTRO ═══ -->
<section class="bg-parchment" id="pil-intro">
  <div class="wrap">
    <p class="eyebrow" style="color:${color}">Foundation ${fnd.roman} — ${fnd.label}</p>
    <h2>${title}</h2>

    <details class="design-logic">
      <summary>Design Logic — How These Positions Work Together</summary>
      <div class="design-body">
        <p><!-- TODO: design logic explanation --></p>
        <h3>Family Structure</h3>
        <p>The <span data-dynamic="family-count">0</span> family codes group positions into logical reform areas:</p>
        <ul>
          <!-- TODO: list family codes and their purposes -->
        </ul>
      </div>
    </details>

    <div class="pil-intro">
      <div>
        <h2>The Core Commitment</h2>
        <p><!-- TODO: core commitment statement --></p>
        <ul>
          <!-- TODO: key bullet points -->
        </ul>
      </div>
      <div>
        <h2>What This Pillar Covers</h2>
        <ul>
          <!-- TODO: scope list -->
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ═══ PROBLEM ═══ -->
<section class="bg-dark on-dark" id="pil-problem">
  <div class="wrap">
    <p class="eyebrow">The Problem</p>
    <h2><!-- TODO: problem section heading --></h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin-top:1.5rem">
      <div class="problem-card">
        <h3><!-- Problem 1 title --></h3>
        <p><!-- Problem 1 description --></p>
      </div>
      <!-- Add more .problem-card divs as needed -->
    </div>
  </div>
</section>

<!-- ═══ REFORM ═══ -->
<section class="bg-parchment" id="pil-reform">
  <div class="wrap">
    <p class="eyebrow">Reform Areas</p>
    <h2><!-- TODO: reform section heading --></h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin-top:1.5rem">
      <div class="reform-card">
        <h3><!-- Reform area 1 --></h3>
        <p><!-- Description --></p>
      </div>
      <!-- Add more .reform-card divs as needed -->
    </div>
  </div>
</section>

<!-- ═══ POLICY ═══ -->
<section class="bg-white" id="pil-policy">
  <div class="wrap">
    <p class="eyebrow">Policy Positions</p>
    <h2>${title}: Policy Framework</h2>
    <p style="margin-bottom:2rem">
      <span data-dynamic="policy-count">0</span> positions across
      <span data-dynamic="family-count">0</span> family codes.
    </p>

    <!-- ── FAMILY: ${prefix}-XXX ─────────────────────────── -->
    <div class="policy-family">
      <div class="family-header">
        <span class="family-code">${prefix}-XXX</span>
        <span class="family-title"><!-- Family Title --></span>
        <span class="family-count">0 positions</span>
      </div>

      <div class="policy-card status-proposed" id="${prefix}-XXX-001">
        <div class="rule-header">
          <span class="rule-id">${prefix}-XXX-001</span>
          <span class="rule-badge">Proposed</span>
        </div>
        <div class="rule-title"><!-- Rule title --></div>
        <div class="rule-stmt"><!-- Rule statement --></div>
        <div class="rule-notes"><!-- Notes / rationale --></div>
      </div>

    </div><!-- /.policy-family -->

  </div>
</section>

<!-- ═══ RESEARCH ═══ -->
<section class="bg-dark on-dark" id="pil-research">
  <div class="wrap">
    <p class="eyebrow">Research &amp; Evidence</p>
    <h2>The Evidence Base</h2>
    <div class="research-body" style="color:rgba(255,255,255,.85)">
      <p><!-- TODO: research summary paragraph with citations --></p>
    </div>
  </div>
</section>

<!-- ═══ REFERENCES ═══ -->
<section class="bg-parchment footnotes" id="pil-refs">
  <div class="wrap">
    <h2>References</h2>
    <ol class="footnote-list">
      <li id="fn1"><!-- APA citation 1 --></li>
    </ol>
  </div>
</section>

<!-- ═══ RELATED ═══ -->
<section class="bg-navy on-dark" id="pil-related">
  <div class="wrap" style="text-align:center">
    <p class="eyebrow">Connected Pillars</p>
    <h2>Part of the Larger Framework</h2>
    <div style="display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;margin-top:1.5rem">
      <!-- Add links to related pillars here -->
    </div>
    <div style="margin-top:2rem">
      <a href="../foundations.html#${foundation}" class="btn-primary" style="background:${color}">
        ← Foundation ${fnd.roman}: ${fnd.label}
      </a>
    </div>
  </div>
</section>

<!-- ═══ FOOTER ═══ -->
<footer class="site-footer">
  <div class="wrap">
    <span class="footer-brand">Freedom and Dignity Project</span>
    <ul class="footer-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="index.html">Pillars</a></li>
      <li><a href="../compare/index.html">Perspectives</a></li>
    </ul>
    <span class="footer-note">A Third Bill of Rights for the 21st Century. · <a href="../about-ai.html" style="color:inherit;opacity:.7">On the Use of AI</a></span>
  </div>
</footer>

<script src="../assets/js/data.js"></script>
<script src="../assets/js/app.js"></script>
</body>
</html>
`;

fs.writeFileSync(outFile, html, 'utf8');
console.log(`\n✅  Created: ${outFile}\n`);
console.log('Next steps:');
console.log(`  1. Add pillar to docs/assets/js/data.js — pillars array + foundation "${foundation}" .pillars list`);
console.log(`  2. Update PILLAR_COUNT in tests/unit/data.test.js and tests/e2e/site.spec.js`);
console.log(`  3. Fill in TODOs in the generated HTML`);
console.log(`  4. npm run test:unit && npm run test:e2e\n`);
