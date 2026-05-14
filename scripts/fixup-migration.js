#!/usr/bin/env node
'use strict';
// One-time fixup script to catch items missed by migrate-policy-areas.js --apply
// Run: node scripts/fixup-migration.js

const fs   = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..');
let changed = [];

function patch(relPath, fn) {
  const file = path.join(REPO, relPath);
  if (!fs.existsSync(file)) { console.log('[skip]', relPath); return; }
  const src = fs.readFileSync(file, 'utf8');
  const out = fn(src);
  if (out !== src) {
    fs.writeFileSync(file, out, 'utf8');
    changed.push(relPath);
    console.log('[write]', relPath);
  } else {
    console.log('[unchanged]', relPath);
  }
}

// ── app.js ───────────────────────────────────────────────────────────────────
patch('docs/assets/js/app.js', s => {
  // Regex literal /\/(pillars|compare)\// in JS source
  s = s.split('/\\/(pillars|compare)\\//')
       .join('/\\/(policy|compare)\\//')

  // Variable name missed by Phase 4
  s = s.split('pillarGrid').join('policyAreaGrid');

  // className string assignments without dot prefix (missed by Phase 3)
  s = s.split("'pillar-filter-btn'").join("'policy-area-filter-btn'");
  s = s.split('"pillar-filter-btn"').join('"policy-area-filter-btn"');
  s = s.split("'pillar-card'").join("'policy-area-card'");
  s = s.split('"pillar-card"').join('"policy-area-card"');

  // SELECTORS array -- .pillar-intro p and .pillar-summary (missed by Phase 3)
  s = s.split("'.pillar-intro p'").join("'.area-intro p'");
  s = s.split("'.pillar-summary'").join("'.area-summary'");

  // classList bare names (no dot -- missed by Phase 3)
  s = s.split("'pil-grid-closing'").join("'area-grid-closing'");
  s = s.split('"pil-grid-closing"').join('"area-grid-closing"');

  // Comments
  s = s.replace(/for very tall sections \(like #pil-policy\)/g,
                'for very tall sections (like #area-policy)');
  s = s.replace(/repeated in every pillar HTML file/g,
                'repeated in every policy area HTML file');
  s = s.replace(/on pillar pages\./g, 'on policy area pages.');
  s = s.replace(/\/\* ── PILLAR SECTION SCROLLSPY/g,
                '/* ── POLICY AREA SECTION SCROLLSPY');
  s = s.replace(/\/\* ── PILLAR FILTER/g, '/* ── POLICY AREA FILTER');

  return s;
});

// ── data.js ───────────────────────────────────────────────────────────────────
patch('docs/assets/js/data.js', s => {
  // Foundation pillars: property declarations (indented, no preceding dot in source)
  s = s.replace(/^(\s+)pillars: \[/gm, '$1policyAreas: [');
  // PolicyOS summary string
  s = s.split('"apply to every pillar."').join('"apply to every policy area."');
  s = s.split("'apply to every pillar.'").join("'apply to every policy area.'");
  return s;
});

// ── style.css ─────────────────────────────────────────────────────────────────
patch('docs/assets/css/style.css', s => {
  // CSS keyframe names
  s = s.split('pil-grid-in').join('area-grid-in');
  s = s.split('pil-grid-out').join('area-grid-out');
  // Comments
  s = s.replace(/References sections on pillar pages/g,
                'References sections on policy area pages');
  s = s.replace(/\/\* ── PILLARS PAGE/g, '/* ── POLICY AREAS PAGE');
  return s;
});

// ── HTML/njk: bare class names, section IDs, href anchors ────────────────────
//
// Phase 3 CLASS_RENAMES used CSS dot-prefix syntax (e.g. .pil-snav) which
// correctly handles CSS selectors and JS querySelector strings, but does NOT
// match bare class names inside HTML class="..." attributes. This pass fixes
// that by operating on class attribute values, id attributes, and href anchors.

const PIL_BARE_SPECIAL = [
  // These don't follow the simple pil- → area- prefix pattern
  ['pil-pillar-card',  'area-card'],
  ['pil-pillar-title', 'area-card-title'],
  ['pil-pillar-desc',  'area-card-desc'],
  ['pil-pillar-link',  'area-link'],
  ['pil-pillar-grid',  'area-grid'],
  ['pil-fv-pill',      'pi-fv-area-pill'],
];

function fixBareClass(val) {
  // Apply special cases first (before the general pil- → area- rule)
  for (const [from, to] of PIL_BARE_SPECIAL) {
    val = val.split(from).join(to);
  }
  // General rule: pil-xxx → area-xxx for all remaining pil- prefixed tokens
  val = val.replace(/\bpil-([a-z][a-z0-9-]*)/g, 'area-$1');
  return val;
}

function fixHtmlNjk(s) {
  // class="..." attribute values
  s = s.replace(/\bclass="([^"]*)"/g, (m, val) => `class="${fixBareClass(val)}"`);
  // id="pil-..." attributes
  s = s.replace(/\bid="pil-([a-z][a-z0-9-]*)"/g, 'id="area-$1"');
  // href="#pil-..." anchors
  s = s.replace(/href="#pil-([a-z][a-z0-9-]*)"/g, 'href="#area-$1"');
  // aria-controls="pil-..." if any
  s = s.replace(/aria-controls="pil-([a-z][a-z0-9-]*)"/g, 'aria-controls="area-$1"');
  return s;
}

function walkFiles(dir, ext) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!['node_modules', '.git'].includes(entry.name)) {
        results.push(...walkFiles(full, ext));
      }
    } else if (entry.name.endsWith(ext)) {
      results.push(full);
    }
  }
  return results;
}

const htmlFiles = [
  ...walkFiles(path.join(REPO, 'docs'), '.html'),
].filter(f => !f.includes('/superpowers/'));

const njkFiles = walkFiles(path.join(REPO, 'src/pages'), '.njk');

for (const file of [...htmlFiles, ...njkFiles]) {
  patch(path.relative(REPO, file), fixHtmlNjk);
}

// ── about-ai.njk: SAMPLE_PILLARS ─────────────────────────────────────────────
// The pre-Phase-5 targeted replacement ran on about-ai.html but not .njk
patch('src/pages/about-ai.njk', s =>
  s.split('<code>SAMPLE_PILLARS</code>').join('<code>SAMPLE_POLICY_AREAS</code>')
);

console.log('\nDone. Files changed:', changed.length);
