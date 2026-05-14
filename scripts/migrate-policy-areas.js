#!/usr/bin/env node
/**
 * migrate-policy-areas.js — Rename "pillars" to "policy areas" across the codebase.
 *
 * Usage:
 *   node scripts/migrate-policy-areas.js          # dry run (prints changes, no writes)
 *   node scripts/migrate-policy-areas.js --apply  # apply all changes
 *   node scripts/migrate-policy-areas.js --verify # scan for remaining violations
 *
 * Design spec: docs/superpowers/specs/2026-05-12-pillars-to-policy-areas-design.md
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const parse5 = require('parse5');

const REPO_ROOT = path.resolve(__dirname, '..');

const APPLY  = process.argv.includes('--apply');
const VERIFY = process.argv.includes('--verify');

// ---------------------------------------------------------------------------
// Phase 3: CSS class rename table — sorted longest-match-first (enforced by
// migrate-phase3-sort.test.js). Do not reorder without updating tests.
// ---------------------------------------------------------------------------

const CLASS_RENAMES_RAW = [
  // .pil-* prefix renames
  ['.pil-pillar-card',             '.area-card'],
  ['.pil-pillar-title',            '.area-card-title'],
  ['.pil-pillar-desc',             '.area-card-desc'],
  ['.pil-pillar-link',             '.area-link'],
  ['.pil-pillar-grid',             '.area-grid'],
  ['.pil-foundation-accordion',    '.area-foundation-accordion'],
  ['.pil-foundation-bar-left',     '.area-foundation-bar-left'],
  ['.pil-foundation-bar-right',    '.area-foundation-bar-right'],
  ['.pil-foundation-bar-text',     '.area-foundation-bar-text'],
  ['.pil-foundation-bar',          '.area-foundation-bar'],
  ['.pil-foundation-name',         '.area-foundation-name'],
  ['.pil-foundation-num',          '.area-foundation-num'],
  ['.pil-foundation-teaser',       '.area-foundation-teaser'],
  ['.pil-fv-pill',                 '.pi-fv-area-pill'],
  ['.pil-grid-closing',            '.area-grid-closing'],
  ['.pil-idx-wrap',                '.area-idx-wrap'],
  ['.pil-chevron',                 '.area-chevron'],
  ['.pil-hero',                    '.area-hero'],
  ['.pil-intro',                   '.area-intro'],
  ['.pil-summary',                 '.area-summary'],
  ['.pil-snav',                    '.area-snav'],
  ['.pil-title',                   '.area-title'],
  // Other pillar-named classes
  ['.adv-pillar-header',           '.adv-area-header'],
  ['.adv-pillar-title',            '.adv-area-title'],
  ['.adv-pillar-badge',            '.adv-area-badge'],
  ['.adv-pillar-body',             '.adv-area-body'],
  ['.adv-pillar',                  '.adv-area'],
  ['.cov-pillar',                  '.cov-area'],
  ['.f-pillar-grid',               '.f-area-grid'],
  ['.f-pillar-card',               '.f-area-card'],
  ['.f-pillars-header',            '.f-areas-header'],
  ['.mission-pillars-grid',        '.mission-areas-grid'],
  ['.mission-pillar-card',         '.mission-area-card'],
  ['.pi-fv-pillars',               '.pi-fv-areas'],
  ['.pfc-pillars',                 '.pfc-areas'],
  ['.pillar-filter-btn',           '.policy-area-filter-btn'],
  ['.pillar-filters',              '.policy-area-filters'],
  ['.pillar-grid',                 '.policy-area-grid'],
  ['.pillar-index-section',        '.policy-area-index-section'],
  ['.pillar-card',                 '.policy-area-card'],
  ['.pillar-status-pill',          '.policy-area-status-pill'],
  ['.roadmap-pillar-table',        '.roadmap-area-table'],
  ['.cmp-th-pillar',               '.cmp-th-area'],
  ['.cmp-td-pillar',               '.cmp-td-area'],
  ['.fd-pillar-tag',               '.fd-policy-area-tag'],
  ['.fd-pillars',                  '.fd-policy-areas'],
  // IDs renamed in Phase 3 (HTML/njk files)
  ['id="pil-snav"',                'id="area-snav"'],
  ['id="pil-related"',             'id="area-related"'],
  ['#pil-snav',                    '#area-snav'],
  ['#pil-related',                 '#area-related'],
];

// Sorted longest-match-first — the canonical order enforced by the unit test.
const CLASS_RENAMES = CLASS_RENAMES_RAW.sort(([a], [b]) => b.length - a.length);

module.exports = { CLASS_RENAMES };

// ---------------------------------------------------------------------------
// File discovery helpers
// ---------------------------------------------------------------------------

const EXCLUDED_DIRS = new Set([
  'node_modules',
  '.git',
]);

const EXCLUDED_PREFIXES = [
  'policy/catalog',
  'policy/policyos',
  'policy/foundations',
  'docs/superpowers',
];

function isExcluded(absPath) {
  const rel = path.relative(REPO_ROOT, absPath);
  const first = rel.split(path.sep)[0];
  if (EXCLUDED_DIRS.has(first)) return true;
  return EXCLUDED_PREFIXES.some(p => rel.startsWith(p));
}

function walkFiles(dir, ext) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!EXCLUDED_DIRS.has(entry.name) && !isExcluded(full)) {
        results.push(...walkFiles(full, ext));
      }
    } else if (!ext || (Array.isArray(ext) ? ext.some(e => entry.name.endsWith(e)) : entry.name.endsWith(ext))) {
      if (!isExcluded(full)) results.push(full);
    }
  }
  return results;
}

function htmlFiles()   { return walkFiles(path.join(REPO_ROOT, 'docs'), '.html'); }
function xmlFiles()    { return walkFiles(path.join(REPO_ROOT, 'docs'), '.xml'); }
function njkFiles()    { return walkFiles(path.join(REPO_ROOT, 'src/pages'), '.njk'); }
function jsFiles()     { return walkFiles(path.join(REPO_ROOT, 'docs/assets/js'), '.js'); }
function cssFiles()    { return [path.join(REPO_ROOT, 'docs/assets/css/style.css')].filter(f => fs.existsSync(f)); }
function testFiles()   { return walkFiles(path.join(REPO_ROOT, 'tests'), '.js'); }
function scriptFiles() { return walkFiles(path.join(REPO_ROOT, 'scripts'), '.js'); }

// ---------------------------------------------------------------------------
// Write helper
// ---------------------------------------------------------------------------

function writeFile(filePath, newContent, originalContent) {
  if (newContent === originalContent) return false;
  if (APPLY) {
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`  [write] ${path.relative(REPO_ROOT, filePath)}`);
  } else {
    console.log(`  [would write] ${path.relative(REPO_ROOT, filePath)}`);
  }
  return true;
}

// ---------------------------------------------------------------------------
// Phase 1: File moves
// ---------------------------------------------------------------------------

function phase1() {
  console.log('\n--- Phase 1: File moves ---');

  // Capture pre-move file list for Phase 6 fail-loudly check (before any moves)
  const preMoveHtml = walkFiles(path.join(REPO_ROOT, 'docs/pillars'), '.html');
  const preMoveNjk  = walkFiles(path.join(REPO_ROOT, 'src/pages/pillars'), '.njk');
  const expectedCompletionStatusFiles = [
    ...preMoveHtml.map(f => f.replace(path.sep + 'docs' + path.sep + 'policy' + path.sep,
                                      path.sep + 'docs' + path.sep + 'policy' + path.sep)),
    ...preMoveNjk.map(f => f.replace(path.sep + 'src' + path.sep + 'pages' + path.sep + 'policy' + path.sep,
                                     path.sep + 'src' + path.sep + 'pages' + path.sep + 'policy' + path.sep)),
  ];

  const moves = [
    [path.join(REPO_ROOT, 'docs/pillars'),      path.join(REPO_ROOT, 'docs/policy')],
    [path.join(REPO_ROOT, 'src/pages/pillars'), path.join(REPO_ROOT, 'src/pages/policy')],
  ];

  for (const [absFrom, absTo] of moves) {
    if (!fs.existsSync(absFrom)) {
      console.log(`  [skip] ${path.relative(REPO_ROOT, absFrom)} does not exist`);
      continue;
    }
    if (APPLY) {
      fs.mkdirSync(absTo, { recursive: true });
      for (const file of fs.readdirSync(absFrom)) {
        fs.renameSync(path.join(absFrom, file), path.join(absTo, file));
      }
      fs.rmdirSync(absFrom);
      console.log(`  [move] ${path.relative(REPO_ROOT, absFrom)}/ -> ${path.relative(REPO_ROOT, absTo)}/`);
    } else {
      const files = fs.readdirSync(absFrom);
      console.log(`  [would move] ${path.relative(REPO_ROOT, absFrom)}/ -> ${path.relative(REPO_ROOT, absTo)}/ (${files.length} files)`);
    }
  }

  // Rename new-pillar.js -> new-policy-area.js
  const oldGenerator = path.join(REPO_ROOT, 'scripts/new-pillar.js');
  const newGenerator = path.join(REPO_ROOT, 'scripts/new-policy-area.js');
  if (fs.existsSync(oldGenerator)) {
    if (APPLY) {
      fs.renameSync(oldGenerator, newGenerator);
      console.log('  [rename] scripts/new-pillar.js -> scripts/new-policy-area.js');
    } else {
      console.log('  [would rename] scripts/new-pillar.js -> scripts/new-policy-area.js');
    }
  }

  // Delete build_pillar_pages.py
  const buildScript = path.join(REPO_ROOT, 'scripts/build_pillar_pages.py');
  if (fs.existsSync(buildScript)) {
    if (APPLY) {
      fs.unlinkSync(buildScript);
      console.log('  [delete] scripts/build_pillar_pages.py');
    } else {
      console.log('  [would delete] scripts/build_pillar_pages.py');
    }
  }

  return expectedCompletionStatusFiles;
}

// ---------------------------------------------------------------------------
// Phase 2: URL and path replacements
// ---------------------------------------------------------------------------

function phase2() {
  console.log('\n--- Phase 2: URL/path replacements ---');

  // Pre-phase path.join audit (halt on unaccounted pillars path segments in scripts)
  const knownPathJoinScripts = new Set(['backfill-rule-notes.js', 'strip-card-status.js', 'migrate-policy-areas.js']);
  for (const file of scriptFiles()) {
    const base = path.basename(file);
    if (knownPathJoinScripts.has(base)) continue;
    const content = fs.readFileSync(file, 'utf8');
    const pathJoinMatch = /path\.join\([^)]*['"]pillars['"]/m.test(content);
    if (pathJoinMatch) {
      throw new Error(
        `ABORT: Unaccounted path.join('policy') found in scripts/${base}. ` +
        'Update the script or add it to knownPathJoinScripts before migrating.'
      );
    }
  }

  const allFiles = [
    ...htmlFiles(), ...xmlFiles(), ...njkFiles(),
    ...jsFiles(), ...testFiles(), ...scriptFiles(),
  ];

  const replacements = [
    ['/policy/', '/policy/'],
    ["'policy'", "'policy'"],
    ['policy/',  'policy/'],
  ];

  for (const file of allFiles) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;

    // Targeted explicit replacement for regex literal in site.spec.js
    if (path.basename(file) === 'site.spec.js') {
      content = content.replace(/\/pillars\\\//g, '/policy\\/');
    }

    for (const [from, to] of replacements) {
      content = content.split(from).join(to);
    }

    writeFile(file, content, original);
  }
}

// ---------------------------------------------------------------------------
// Phase 3: CSS class renames (longest-match-first, includes tests/**/*.js)
// ---------------------------------------------------------------------------

function phase3() {
  console.log('\n--- Phase 3: CSS class renames ---');

  const allFiles = [
    ...htmlFiles(), ...njkFiles(), ...jsFiles(),
    ...cssFiles(), ...testFiles(),
  ];

  for (const file of allFiles) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;

    for (const [from, to] of CLASS_RENAMES) {
      content = content.split(from).join(to);
    }

    writeFile(file, content, original);
  }
}

// ---------------------------------------------------------------------------
// Phase 4: JS identifier renames (app.js + data.js only)
// ---------------------------------------------------------------------------

const JS_IDENTIFIER_RENAMES = [
  // data.js — most specific first
  ['siteData.getPillarsByFoundation', 'siteData.getPolicyAreasByFoundation'],
  ['getPillarsByFoundation',          'getPolicyAreasByFoundation'],
  ['foundation.pillars:',             'foundation.policyAreas:'],
  ['"apply to every pillar."',        '"apply to every policy area."'],
  ["'apply to every pillar.'",        "'apply to every policy area.'"],
  ['siteData.pillars',                'siteData.policyAreas'],
  // app.js block comments (longest first)
  ['/* ── PILLARS INDEX ACCORDION ANIMATION ─────────────── */',
   '/* ── POLICY AREAS INDEX ACCORDION ANIMATION ─────────────── */'],
  ['/* ── PILLAR FILTER + RENDER ─── */',
   '/* ── POLICY AREA FILTER + RENDER ─── */'],
  ['/* ── POLICYOS PILLAR OVERLAY */',
   '/* ── POLICYOS POLICY AREA OVERLAY */'],
  ['/* ── PILLAR SECTION SCROLLSPY */',
   '/* ── POLICY AREA SECTION SCROLLSPY */'],
  // app.js inline comments
  ["// Injects a PolicyOS design-rules section after #pil-related on pillar pages.",
   "// Injects a PolicyOS design-rules section after #area-related on policy area pages."],
  ["// Highlights the active section in the sticky pillar sub-nav.",
   "// Highlights the active section in the sticky policy area sub-nav."],
  // app.js strings
  ["'System design rules that apply to this pillar under the PolicyOS framework.'",
   "'System design rules that apply to this policy area under the PolicyOS framework.'"],
  // app.js identifiers and DOM references
  ['renderPillars',                   'renderPolicyAreas'],
  ['pillarOverlays',                  'policyAreaOverlays'],
  ['pillarCount',                     'policyAreaCount'],
  ["getElementById('pil-snav')",      "getElementById('area-snav')"],
  ['getElementById("pil-snav")',       'getElementById("area-snav")'],
  ["getElementById('pil-related')",   "getElementById('area-related')"],
  ['getElementById("pil-related")',    'getElementById("area-related")'],
  ["section.id = 'pil-policyos'",     "section.id = 'area-policyos'"],
  ['href="#pil-policyos"',            'href="#area-policyos"'],
  ["getElementById('pillar-filters')", "getElementById('policy-area-filters')"],
  ['getElementById("pillar-filters")', 'getElementById("policy-area-filters")'],
  ["'All Pillars'",                   "'All Policy Areas'"],
  ['"All Pillars"',                   '"All Policy Areas"'],
  ['/(pillars|compare)/',             '/(policy|compare)/'],
  // General property accesses — last (most general)
  ['.pillars',                        '.policyAreas'],
];

function phase4() {
  console.log('\n--- Phase 4: JS identifier renames ---');

  const targetFiles = [
    path.join(REPO_ROOT, 'docs/assets/js/app.js'),
    path.join(REPO_ROOT, 'docs/assets/js/data.js'),
  ].filter(f => fs.existsSync(f));

  for (const file of targetFiles) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;

    for (const [from, to] of JS_IDENTIFIER_RENAMES) {
      content = content.split(from).join(to);
    }

    writeFile(file, content, original);
  }
}

// ---------------------------------------------------------------------------
// Phase 5: Prose replacements (HTML/njk/XML only — never JS or test files)
// ---------------------------------------------------------------------------

const PROSE_REPLACEMENTS_EXACT = [
  // Most specific phrases first
  ['Policy Pillars', 'Policy Areas'],
  ['Policy Pillar',  'Policy Area'],
  ['policy pillars', 'policy areas'],
  ['policy pillar',  'policy area'],
];

function phase5() {
  console.log('\n--- Phase 5: Prose replacements ---');

  const proseFiles = [...htmlFiles(), ...njkFiles(), ...xmlFiles()];

  for (const file of proseFiles) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;

    // Targeted pre-phase replacement: SAMPLE_PILLARS inside <code> in about-ai.html
    if (path.basename(file) === 'about-ai.html') {
      content = content.split('<code>SAMPLE_PILLARS</code>').join('<code>SAMPLE_POLICY_AREAS</code>');
    }

    // Exact multi-word phrases
    for (const [from, to] of PROSE_REPLACEMENTS_EXACT) {
      content = content.split(from).join(to);
    }

    // Word-boundary replacements for standalone occurrences
    content = content.replace(/\bPillars\b/g, 'Policy Areas');
    content = content.replace(/\bPillar\b/g,  'Policy Area');
    content = content.replace(/\bpillars\b/g, 'policy areas');
    content = content.replace(/\bpillar\b/g,  'policy area');

    writeFile(file, content, original);
  }
}

// ---------------------------------------------------------------------------
// Phase 6: Element removals
// ---------------------------------------------------------------------------

function findNodeInTree(node, predicate) {
  if (predicate(node)) return node;
  for (const child of (node.childNodes || [])) {
    const found = findNodeInTree(child, predicate);
    if (found) return found;
  }
  return null;
}

function isCompletionStatusDiv(node) {
  return node.tagName === 'div' &&
    (node.attrs || []).some(a => a.name === 'class' && a.value.split(' ').includes('completion-status'));
}

function removeCompletionStatusHtml(filePath) {
  const source = fs.readFileSync(filePath, 'utf8');
  const doc = parse5.parse(source);
  const target = findNodeInTree(doc, isCompletionStatusDiv);
  if (!target) return null;

  const parent = target.parentNode;
  parent.childNodes = parent.childNodes.filter(n => n !== target);

  return { newContent: parse5.serialize(doc), original: source };
}

function removeCompletionStatusNjk(filePath) {
  const source = fs.readFileSync(filePath, 'utf8');
  const doc = parse5.parse(source, { sourceCodeLocationInfo: true });
  const target = findNodeInTree(doc, isCompletionStatusDiv);
  if (!target) return null;

  const loc = target.sourceCodeLocation;
  if (!loc) throw new Error(`sourceCodeLocation missing in ${path.relative(REPO_ROOT, filePath)}`);

  const newContent = source.slice(0, loc.startOffset) + source.slice(loc.endOffset);
  return { newContent, original: source };
}

function phase6() {
  console.log('\n--- Phase 6: Element removals ---');

  // After Phase 1 moves, files are in docs/policy/ and src/pages/policy/
  const policyHtmlFiles = walkFiles(path.join(REPO_ROOT, 'docs/policy'), '.html');
  const policyNjkFiles  = walkFiles(path.join(REPO_ROOT, 'src/pages/policy'), '.njk');

  for (const file of policyHtmlFiles) {
    const base = path.basename(file);
    if (base === 'index.html') {
      console.log(`  [skip] ${path.relative(REPO_ROOT, file)} (index file)`);
      continue;
    }
    const result = removeCompletionStatusHtml(file);
    if (result) {
      writeFile(file, result.newContent, result.original);
    } else if (APPLY) {
      // Only fail loudly when applying -- in dry-run, div may already be removed
      throw new Error(`completion-status div not found in ${path.relative(REPO_ROOT, file)}`);
    } else {
      console.log(`  [warn] completion-status div already removed in ${path.relative(REPO_ROOT, file)}`);
    }
  }

  for (const file of policyNjkFiles) {
    const base = path.basename(file);
    if (base === 'index.njk') {
      console.log(`  [skip] ${path.relative(REPO_ROOT, file)} (index file)`);
      continue;
    }
    const result = removeCompletionStatusNjk(file);
    if (result) {
      writeFile(file, result.newContent, result.original);
    } else if (APPLY) {
      throw new Error(`completion-status div not found in ${path.relative(REPO_ROOT, file)}`);
    } else {
      console.log(`  [warn] completion-status div already removed in ${path.relative(REPO_ROOT, file)}`);
    }
  }

  // Remove pil-pillar-count spans across all HTML/njk
  for (const file of [...htmlFiles(), ...njkFiles()]) {
    let content = fs.readFileSync(file, 'utf8');
    const original = content;
    content = content.replace(/<span class="pil-pillar-count">[^<]*<\/span>/g, '');
    writeFile(file, content, original);
  }

  // Remove dead case 'pillar-count' branch from app.js
  const appJs = path.join(REPO_ROOT, 'docs/assets/js/app.js');
  if (fs.existsSync(appJs)) {
    let content = fs.readFileSync(appJs, 'utf8');
    const original = content;
    // Remove the stale pillar-count comment line
    content = content.replace(
      /\/\/ Usage: <span data-dynamic="pillar-count">\d+<\/span>.*\n/,
      ''
    );
    // Remove the case branch itself
    content = content.replace(/\s*case ['"]pillar-count['"]:[^\n]*\n[^\n]*\n/g, '\n');
    writeFile(appJs, content, original);
  }

  // Remove dead CSS rules from style.css
  const css = path.join(REPO_ROOT, 'docs/assets/css/style.css');
  if (fs.existsSync(css)) {
    let content = fs.readFileSync(css, 'utf8');
    const original = content;
    content = content.replace(/\.pil-pillar-count\s*\{[^}]*\}\n?/g, '');
    content = content.replace(/\.pillar-hero,\n/g, '');
    content = content.replace(/\.pillar-tags\s*\{[^}]*\}\n?/g, '');
    content = content.replace(/\.pillar-tag\s*\{[^}]*\}\n?/g, '');
    writeFile(css, content, original);
  }
}

// ---------------------------------------------------------------------------
// Phase 7: Verify pass (three-check gate)
// ---------------------------------------------------------------------------

const VERIFY_ALLOWLIST = [
  'scripts/migrate-policy-areas.js',
  'scripts/fixup-migration.js',
  'tests/unit/scripts/migrate-phase3-sort.test.js',
  'docs/superpowers',
  'policy/foundations',
  'policy/policyos',
  'policy/catalog',
  // green-party: cites the Green Party's real document "The Four Pillars" and
  // links to gp.org/the_four_pillars — an external URL that cannot be renamed.
  'docs/compare/green-party',
  'src/pages/compare/green-party',
  // classification: references the DB table name `position_pillar_appearances`
  // which is out of scope for this migration (DB schema renamed separately).
  'docs/classification',
  'src/pages/classification',
];

function isAllowlisted(filePath) {
  const rel = path.relative(REPO_ROOT, filePath);
  return VERIFY_ALLOWLIST.some(a => rel.startsWith(a));
}

function phase7Verify() {
  console.log('\n--- Phase 7: Verify pass ---');

  const allFiles = [
    ...htmlFiles(), ...xmlFiles(), ...njkFiles(),
    ...jsFiles(), ...cssFiles(), ...testFiles(), ...scriptFiles(),
  ].filter(f => !isAllowlisted(f));

  const violations = { pillar: [], pilDash: [], completionStatus: [] };

  for (const file of allFiles) {
    const content = fs.readFileSync(file, 'utf8');
    const rel = path.relative(REPO_ROOT, file);

    if (/pillar/i.test(content)) {
      const lines = content.split('\n');
      lines.forEach((line, i) => {
        if (/pillar/i.test(line) && !line.includes('// verify-ok')) {
          violations.pillar.push(`  ${rel}:${i + 1}: ${line.trim().slice(0, 100)}`);
        }
      });
    }

    if (/\bpil-|#pil-/.test(content)) {
      const lines = content.split('\n');
      lines.forEach((line, i) => {
        if (/\bpil-|#pil-/.test(line) && !line.includes('// verify-ok')) {
          violations.pilDash.push(`  ${rel}:${i + 1}: ${line.trim().slice(0, 100)}`);
        }
      });
    }

    if (/completion-status/.test(content)) {
      const lines = content.split('\n');
      lines.forEach((line, i) => {
        if (/completion-status/.test(line)) {
          violations.completionStatus.push(`  ${rel}:${i + 1}: ${line.trim().slice(0, 100)}`);
        }
      });
    }
  }

  let failed = false;

  if (violations.pillar.length) {
    console.error(`\n[FAIL] "pillar" occurrences (${violations.pillar.length}):`);
    violations.pillar.forEach(v => console.error(v));
    failed = true;
  }
  if (violations.pilDash.length) {
    console.error(`\n[FAIL] pil- identifier occurrences (${violations.pilDash.length}):`);
    violations.pilDash.forEach(v => console.error(v));
    failed = true;
  }
  if (violations.completionStatus.length) {
    console.error(`\n[FAIL] completion-status class occurrences (${violations.completionStatus.length}):`);
    violations.completionStatus.forEach(v => console.error(v));
    failed = true;
  }

  if (failed) {
    process.exit(1);
  } else {
    console.log('[PASS] Zero violations — migration complete.');
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

if (!VERIFY) {
  if (!APPLY) {
    console.log('DRY RUN — pass --apply to write changes.\n');
  }

  const expectedCompletionStatusFiles = phase1();
  phase2();
  phase3();
  phase4();
  phase5();
  phase6(expectedCompletionStatusFiles);

  if (!APPLY) {
    console.log('\nDRY RUN complete. Run with --apply to write changes.');
  } else {
    console.log('\nMigration complete. Run with --verify to confirm zero violations.');
  }
} else {
  phase7Verify();
}
