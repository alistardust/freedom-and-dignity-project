'use strict';

const fs    = require('fs');
const path  = require('path');
const parse5 = require('parse5');

// ── Serializer ────────────────────────────────────────────────────────────────
// Minimal HTML serializer — converts a parse5 node back to an HTML string.
function serialize(node) {
  if (node.nodeName === '#text') return node.value;
  if (node.nodeName === '#comment') return `<!--${node.data}-->`;
  if (node.nodeName === '#document' || node.nodeName === '#document-fragment') {
    return (node.childNodes || []).map(serialize).join('');
  }
  const tag = node.tagName;
  const attrs = (node.attrs || [])
    .map(a => a.value === '' ? a.name : `${a.name}="${a.value.replace(/"/g, '&quot;')}"`)
    .join(' ');
  const attrStr = attrs ? ` ${attrs}` : '';
  const voidTags = new Set([
    'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'
  ]);
  if (voidTags.has(tag)) return `<${tag}${attrStr}>`;
  const inner = (node.childNodes || []).map(serialize).join('');
  return `<${tag}${attrStr}>${inner}</${tag}>`;
}

// ── DOM helpers ───────────────────────────────────────────────────────────────
function walk(node, fn) {
  fn(node);
  for (const child of (node.childNodes || [])) walk(child, fn);
}

function findOne(root, pred) {
  const results = [];
  walk(root, n => { if (pred(n)) results.push(n); });
  return results[0] || null;
}

function attr(node, name) {
  return ((node.attrs || []).find(a => a.name === name) || {}).value;
}

function hasClass(node, cls) {
  return (attr(node, 'class') || '').split(' ').includes(cls);
}

function metaContent(doc, propName, propValue) {
  const node = findOne(doc, n =>
    n.tagName === 'meta' && attr(n, propName) === propValue
  );
  return node ? attr(node, 'content') : null;
}

// ── File walker ───────────────────────────────────────────────────────────────
function walkHtml(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (full === path.join(dir, 'superpowers')) continue;
      walkHtml(full, results);
    } else if (entry.name.endsWith('.html')) {
      results.push(full);
    }
  }
  return results;
}

// ── Migrator ──────────────────────────────────────────────────────────────────
function migrateFile(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const doc  = parse5.parse(html);

  // Verify this page has the expected shell — skip if not
  const siteNav = findOne(doc, n => n.tagName === 'nav' && hasClass(n, 'site-nav'));
  if (!siteNav) {
    console.warn(`SKIP (no site-nav found): ${htmlPath}`);
    return null;
  }

  // Extract title
  const titleNode = findOne(doc, n => n.tagName === 'title');
  const titleText = titleNode
    ? (titleNode.childNodes || []).map(n => n.value || '').join('').trim()
    : '';

  // Extract description
  const description = metaContent(doc, 'name', 'description') || '';

  // Extract OG / Twitter meta
  const ogTitle       = metaContent(doc, 'property', 'og:title') || '';
  const ogDescription = metaContent(doc, 'property', 'og:description') || '';
  const ogUrl         = metaContent(doc, 'property', 'og:url') || '';
  const twitterTitle  = metaContent(doc, 'name', 'twitter:title') || '';
  const twitterDesc   = metaContent(doc, 'name', 'twitter:description') || '';

  // Extract og:url path (strip the site root prefix)
  const ogUrlPath = ogUrl.replace(
    /^https:\/\/alistardust\.github\.io\/freedom-and-dignity-project\//,
    ''
  );

  // Extract accent color inline style from head
  const headNode = findOne(doc, n => n.tagName === 'head');
  let accentStyle = '';
  if (headNode) {
    const styleNode = findOne(headNode, n => {
      if (n.tagName !== 'style') return false;
      const text = (n.childNodes || []).map(c => c.value || '').join('');
      return text.includes('--accent-color');
    });
    if (styleNode) {
      accentStyle = serialize(styleNode);
    }
  }

  // Extract body class
  const bodyNode = findOne(doc, n => n.tagName === 'body');
  const bodyClass = attr(bodyNode, 'class') || '';

  // Extract content: body children minus shell elements
  // Inline <script> blocks (no src) are extracted separately for scripts_extra
  const SHELL_SELECTORS = [
    n => n.tagName === 'a' && (attr(n, 'class') || '').includes('skip-link'),
    n => n.tagName === 'nav' && hasClass(n, 'site-nav'),
    n => n.tagName === 'nav' && attr(n, 'id') === 'site-tree',
    n => n.tagName === 'footer' && hasClass(n, 'site-footer'),
    n => n.tagName === 'script' && attr(n, 'src'),
    n => n.tagName === 'script' && !attr(n, 'src'),  // inline → scripts_extra block
  ];

  // Collect page-specific inline scripts for the scripts_extra block
  const inlineScripts = (bodyNode ? bodyNode.childNodes || [] : []).filter(
    n => n.tagName === 'script' && !attr(n, 'src')
  );
  const scriptsExtraHtml = inlineScripts.map(serialize).join('').trim();

  const contentNodes = (bodyNode ? bodyNode.childNodes || [] : []).filter(n => {
    return !SHELL_SELECTORS.some(pred => pred(n));
  });

  const contentHtml = contentNodes.map(serialize).join('').trim();

  // ── Build .njk output ──────────────────────────────────────────────────────
  const lines = [];

  // Policyos.njk gets a generation header (generate-policyos.py will overwrite)
  if (path.basename(htmlPath) === 'policyos.html') {
    lines.push(
      '{# AUTO-GENERATED by generate-policyos.py — do not edit directly.',
      '   Run: python3 scripts/migrate-policyos-to-db.py && python3 scripts/generate-policyos.py && npm run build #}'
    );
  }

  lines.push('{% extends "_base.njk" %}');

  if (description) {
    lines.push(`{% set description = "${description.replace(/"/g, '\\"')}" %}`);
  }

  if (bodyClass) {
    lines.push(`{% set body_class = "${bodyClass}" %}`);
  }

  if (titleText) {
    lines.push(`{% block title %}${titleText}{% endblock %}`);
  }

  if (ogTitle && ogTitle !== titleText) {
    lines.push(`{% block og_title %}${ogTitle}{% endblock %}`);
  }

  if (ogDescription && ogDescription !== description) {
    lines.push(`{% block og_description %}${ogDescription}{% endblock %}`);
  }

  if (ogUrlPath) {
    lines.push(`{% block og_url %}${ogUrlPath}{% endblock %}`);
  }

  if (twitterTitle && twitterTitle !== ogTitle) {
    lines.push(`{% block twitter_title %}${twitterTitle}{% endblock %}`);
  }

  if (twitterDesc && twitterDesc !== ogDescription) {
    lines.push(`{% block twitter_description %}${twitterDesc}{% endblock %}`);
  }

  if (accentStyle) {
    lines.push(`{% block head_extra %}${accentStyle}{% endblock %}`);
  }

  lines.push('{% block content %}');
  lines.push(contentHtml);
  lines.push('{% endblock %}');

  if (scriptsExtraHtml) {
    lines.push(`{% block scripts_extra %}${scriptsExtraHtml}{% endblock %}`);
  }

  return lines.join('\n') + '\n';
}

// ── Main ──────────────────────────────────────────────────────────────────────
function main() {
  const htmlFiles = walkHtml('docs');
  let skipped = 0;
  let migrated = 0;

  for (const htmlPath of htmlFiles) {
    const rel     = path.relative('docs', htmlPath);
    const njkPath = path.join('src/pages', rel.replace(/\.html$/, '.njk'));
    const result  = migrateFile(htmlPath);

    if (result === null) {
      skipped++;
      continue;
    }

    fs.mkdirSync(path.dirname(njkPath), { recursive: true });
    fs.writeFileSync(njkPath, result, 'utf8');
    console.log(`Migrated: ${htmlPath} → ${njkPath}`);
    migrated++;
  }

  console.log(`\nDone: ${migrated} migrated, ${skipped} skipped`);
  if (skipped > 0) {
    console.log('Skipped files require manual migration. See warnings above.');
  }
}

main();
