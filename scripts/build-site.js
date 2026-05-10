'use strict';

const nunjucks = require('nunjucks');
const fs       = require('fs');
const path     = require('path');

// FileSystemLoader needs both paths:
//   src/templates — so _base.njk resolves when extended from a page file
//   src/pages     — so page files resolve when env.render(relToPages, ctx) is called
const env = new nunjucks.Environment(
  new nunjucks.FileSystemLoader(['src/templates', 'src/pages'])
  // autoescape defaults to true — do NOT set false.
  // Block content from child templates is never auto-escaped.
  // {{ variable }} expressions (nav labels, hrefs, body_class) ARE escaped, which is correct.
);

/**
 * Compute the base path prefix for asset hrefs from an output file path.
 * docs/index.html         → ''
 * docs/pillars/foo.html   → '../'
 * docs/foo/bar/baz.html   → '../../'
 */
function computeBase(outputPath) {
  const depth = outputPath.replace(/^docs\//, '').split('/').length - 1;
  return '../'.repeat(depth);
}

/**
 * Compute currentPage (used to set aria-current="page" on matching nav item).
 * docs/index.html                    → 'index.html'
 * docs/pillars/healthcare.html       → 'pillars/healthcare.html'
 * docs/compare/republican-party.html → 'compare/republican-party.html'
 *
 * Nav items have hrefs like 'index.html', 'problem.html' — only root pages match.
 * Pillar and compare pages correctly produce no aria-current match.
 */
function computeCurrentPage(outputPath) {
  return outputPath.replace(/^docs\//, '');
}

function walkNjk(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkNjk(full, results);
    } else if (entry.name.endsWith('.njk')) {
      results.push(full);
    }
  }
  return results;
}

async function main() {
  let nav, footerLinks;
  try {
    nav         = JSON.parse(fs.readFileSync('src/data/nav.json', 'utf8'));
    footerLinks = JSON.parse(fs.readFileSync('src/data/footer-links.json', 'utf8'));
  } catch (err) {
    console.error(`ERROR loading data files: ${err.message}`);
    process.exit(1);
  }

  if (!fs.existsSync('src/pages')) {
    console.log('Build complete: 0 pages (src/pages does not exist yet)');
    return;
  }

  const pageFiles = walkNjk('src/pages');
  let warnings = 0;
  let errors   = 0;

  for (const pageFile of pageFiles) {
    const relToPages = path.relative('src/pages', pageFile);
    const outputPath = path.join('docs', relToPages.replace(/\.njk$/, '.html'));
    const base        = computeBase(outputPath);
    const currentPage = computeCurrentPage(outputPath);

    try {
      const rendered = env.render(relToPages, { nav, footerLinks, base, currentPage });

      if (!rendered.includes('<meta name="description"')) {
        console.warn(`WARNING: no description meta in ${outputPath}`);
        warnings++;
      }

      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, rendered, 'utf8');
    } catch (err) {
      console.error(`ERROR rendering ${pageFile}: ${err.message}`);
      errors++;
    }
  }

  console.log(
    `Build complete: ${pageFiles.length} pages, ${warnings} warnings, ${errors} errors`
  );
  if (errors > 0) process.exit(1);
}

if (require.main === module) {
  main().catch(err => { console.error(err); process.exit(1); });
}

module.exports = { computeBase, computeCurrentPage };
