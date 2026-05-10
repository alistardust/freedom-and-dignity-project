'use strict';

const fs    = require('fs');
const path  = require('path');
const parse5 = require('parse5');

// ── parse5 DOM traversal helpers ─────────────────────────────────────────────

function walk(node, fn) {
  fn(node);
  for (const child of (node.childNodes || [])) walk(child, fn);
}

function findAll(doc, predicate) {
  const results = [];
  walk(doc, node => { if (predicate(node)) results.push(node); });
  return results;
}

function findOne(doc, predicate) {
  return findAll(doc, predicate)[0] || null;
}

function attr(node, name) {
  return ((node.attrs || []).find(a => a.name === name) || {}).value;
}

function hasClass(node, cls) {
  return (attr(node, 'class') || '').split(' ').includes(cls);
}

function childElements(node) {
  return (node.childNodes || []).filter(
    n => n.nodeName && n.nodeName !== '#text' && n.nodeName !== '#comment'
  );
}

// ── Per-file conformance check ────────────────────────────────────────────────

/**
 * Check a single HTML string for conformance.
 * Returns an array of error strings (empty = pass).
 */
function checkFile(html, filePath) {
  const errors = [];
  const doc = parse5.parse(html);

  // Exactly 1 <nav class="site-nav">
  const siteNavs = findAll(doc, n => n.tagName === 'nav' && hasClass(n, 'site-nav'));
  if (siteNavs.length !== 1) {
    errors.push(`${filePath}: expected exactly 1 <nav class="site-nav">, found ${siteNavs.length}`);
  }

  // Exactly 1 <main id="main-content">
  const mains = findAll(doc, n => n.tagName === 'main' && attr(n, 'id') === 'main-content');
  if (mains.length !== 1) {
    errors.push(`${filePath}: expected exactly 1 <main id="main-content">, found ${mains.length}`);
  } else if (childElements(mains[0]).length === 0) {
    // main must not be empty (catches pages that omit {% block content %})
    errors.push(`${filePath}: <main id="main-content"> has no child elements`);
  }

  // Exactly 1 <footer class="site-footer">
  const footers = findAll(doc, n => n.tagName === 'footer' && hasClass(n, 'site-footer'));
  if (footers.length !== 1) {
    errors.push(`${filePath}: expected exactly 1 <footer class="site-footer">, found ${footers.length}`);
  }

  // Exactly 1 <button class="nav-hamburger">
  const burgers = findAll(doc, n => n.tagName === 'button' && hasClass(n, 'nav-hamburger'));
  if (burgers.length !== 1) {
    errors.push(`${filePath}: expected exactly 1 <button class="nav-hamburger">, found ${burgers.length}`);
  }

  // Exactly 1 <nav id="site-tree">
  const siteTrees = findAll(doc, n => n.tagName === 'nav' && attr(n, 'id') === 'site-tree');
  if (siteTrees.length !== 1) {
    errors.push(`${filePath}: expected exactly 1 <nav id="site-tree">, found ${siteTrees.length}`);
  }

  // <ul class="nav-links"> must exist and have at least 1 li
  const navLinks = findOne(doc, n => n.tagName === 'ul' && hasClass(n, 'nav-links'));
  if (!navLinks) {
    errors.push(`${filePath}: <ul class="nav-links"> not found`);
  } else {
    const items = (navLinks.childNodes || []).filter(n => n.tagName === 'li');
    if (items.length === 0) {
      errors.push(`${filePath}: <ul class="nav-links"> is empty`);
    }
  }

  // <ul class="footer-links"> must exist and have at least 1 li
  const footerLinks = findOne(doc, n => n.tagName === 'ul' && hasClass(n, 'footer-links'));
  if (!footerLinks) {
    errors.push(`${filePath}: <ul class="footer-links"> not found`);
  } else {
    const items = (footerLinks.childNodes || []).filter(n => n.tagName === 'li');
    if (items.length === 0) {
      errors.push(`${filePath}: <ul class="footer-links"> is empty`);
    }
  }

  // No <meta name="description" content=""> (empty content)
  const emptyDesc = findOne(
    doc,
    n => n.tagName === 'meta' && attr(n, 'name') === 'description' && attr(n, 'content') === ''
  );
  if (emptyDesc) {
    errors.push(`${filePath}: <meta name="description"> has empty content attribute`);
  }

  // Duplicate id check — catches the regression where inner templates carry
  // id="main-content" while _base.njk already emits <main id="main-content">.
  const allIdNodes = [];
  (function collectIds(node) {
    const idAttr = (node.attrs || []).find(a => a.name === 'id');
    if (idAttr && idAttr.value) allIdNodes.push(idAttr.value);
    for (const child of (node.childNodes || [])) collectIds(child);
  }(doc));
  const idCounts = {};
  for (const id of allIdNodes) idCounts[id] = (idCounts[id] || 0) + 1;
  for (const [id, count] of Object.entries(idCounts)) {
    if (count > 1) errors.push(`${filePath}: id="${id}" appears ${count} times (must be unique)`);
  }

  return errors;
}

// ── Directory scan ────────────────────────────────────────────────────────────

function checkDir(docsDir) {
  const allErrors = [];
  function scanDir(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (full === path.join(docsDir, 'superpowers')) continue; // hand-authored, not build output
        scanDir(full);
      } else if (entry.name.endsWith('.html')) {
        allErrors.push(...checkFile(fs.readFileSync(full, 'utf8'), full));
      }
    }
  }
  scanDir(docsDir);
  return allErrors;
}

// ── Source-level lint ─────────────────────────────────────────────────────────

// Rejects any src/pages/**/*.njk that hand-authors shell structure.
// These patterns must only appear in _base.njk.
const FORBIDDEN_IN_SOURCE = [
  '<nav class="site-nav">',
  '<footer class="site-footer">',
  '<script src=',
];

function lintSource(source, filePath) {
  const errors = [];
  for (const pattern of FORBIDDEN_IN_SOURCE) {
    if (source.includes(pattern)) {
      errors.push(`${filePath}: contains forbidden shell pattern: ${JSON.stringify(pattern)}`);
    }
  }
  return errors;
}

function lintSources(pagesDir) {
  const allErrors = [];
  if (!fs.existsSync(pagesDir)) return allErrors;
  function scanDir(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        scanDir(full);
      } else if (entry.name.endsWith('.njk')) {
        allErrors.push(...lintSource(fs.readFileSync(full, 'utf8'), full));
      }
    }
  }
  scanDir(pagesDir);
  return allErrors;
}

// ── CLI entrypoint ────────────────────────────────────────────────────────────

if (require.main === module) {
  const docErrors = checkDir('docs');
  const srcErrors = lintSources('src/pages');
  const all = [...docErrors, ...srcErrors];
  if (all.length > 0) {
    all.forEach(e => console.error(e));
    process.exit(1);
  }
  console.log('check:html passed — 0 violations');
}

module.exports = { checkFile, checkDir, lintSource, lintSources };
