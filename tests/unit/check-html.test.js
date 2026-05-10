/**
 * Unit tests for check-html.js conformance assertions.
 * Each test uses a minimal inline fixture — no files on disk.
 */
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { checkFile } = require('../../scripts/check-html.js');

// Minimal valid HTML — passes all assertions
const VALID = `<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <meta name="description" content="A real description.">
</head>
<body>
<nav class="site-nav"><div class="nav-inner">
  <ul class="nav-links"><li><a href="index.html">Home</a></li></ul>
  <button type="button" class="nav-hamburger" aria-label="Open site menu">&#9776;</button>
</div></nav>
<nav id="site-tree" hidden></nav>
<main id="main-content"><p>Content here.</p></main>
<footer class="site-footer"><div class="wrap">
  <ul class="footer-links"><li><a href="index.html">Home</a></li></ul>
</div></footer>
</body></html>`;

describe('checkFile — valid HTML passes all assertions', () => {
  it('returns no errors for fully valid HTML', () => {
    expect(checkFile(VALID, 'test.html')).toHaveLength(0);
  });
});

describe('checkFile — site-nav assertion', () => {
  it('returns error when site-nav is absent', () => {
    const html = VALID.replace('class="site-nav"', 'class="other-nav"');
    expect(checkFile(html, 'test.html').some(e => e.includes('site-nav'))).toBe(true);
  });
  it('returns error when site-nav appears twice', () => {
    const html = VALID.replace('<nav class="site-nav">', '<nav class="site-nav"><nav class="site-nav">');
    expect(checkFile(html, 'test.html').some(e => e.includes('site-nav'))).toBe(true);
  });
});

describe('checkFile — main#main-content assertion', () => {
  it('returns error when main-content id is missing', () => {
    const html = VALID.replace('id="main-content"', 'id="other"');
    expect(checkFile(html, 'test.html').some(e => e.includes('main-content'))).toBe(true);
  });
  it('returns error when main has no child elements', () => {
    const html = VALID.replace('<p>Content here.</p>', '');
    expect(checkFile(html, 'test.html').some(e =>
      e.includes('empty') || e.includes('main')
    )).toBe(true);
  });
});

describe('checkFile — site-footer assertion', () => {
  it('returns error when site-footer is absent', () => {
    const html = VALID.replace('class="site-footer"', 'class="other-footer"');
    expect(checkFile(html, 'test.html').some(e => e.includes('site-footer'))).toBe(true);
  });
});

describe('checkFile — nav-hamburger assertion', () => {
  it('returns error when nav-hamburger is absent', () => {
    const html = VALID.replace('class="nav-hamburger"', 'class="menu-btn"');
    expect(checkFile(html, 'test.html').some(e => e.includes('nav-hamburger'))).toBe(true);
  });
});

describe('checkFile — site-tree assertion', () => {
  it('returns error when site-tree nav is absent', () => {
    const html = VALID.replace('<nav id="site-tree" hidden></nav>', '');
    expect(checkFile(html, 'test.html').some(e => e.includes('site-tree'))).toBe(true);
  });
});

describe('checkFile — nav-links not-empty assertion', () => {
  it('returns error when nav-links has no li children', () => {
    const html = VALID.replace(
      '<ul class="nav-links"><li><a href="index.html">Home</a></li></ul>',
      '<ul class="nav-links"></ul>'
    );
    expect(checkFile(html, 'test.html').some(e => e.includes('nav-links'))).toBe(true);
  });
});

describe('checkFile — footer-links not-empty assertion', () => {
  it('returns error when footer-links has no li children', () => {
    const html = VALID.replace(
      '<ul class="footer-links"><li><a href="index.html">Home</a></li></ul>',
      '<ul class="footer-links"></ul>'
    );
    expect(checkFile(html, 'test.html').some(e => e.includes('footer-links'))).toBe(true);
  });
});

describe('checkFile — no empty description meta', () => {
  it('returns error when description meta has empty content', () => {
    const html = VALID.replace('content="A real description."', 'content=""');
    expect(checkFile(html, 'test.html').some(e => e.includes('description'))).toBe(true);
  });
});

describe('lintSources — source-level rules', () => {
  const { lintSource } = require('../../scripts/check-html.js');

  it('returns error for .njk containing forbidden site-nav pattern', () => {
    const errors = lintSource('<nav class="site-nav">', 'src/pages/test.njk');
    expect(errors.some(e => e.includes('site-nav'))).toBe(true);
  });

  it('returns no errors for clean .njk content', () => {
    const errors = lintSource('<main id="main-content"><p>clean</p></main>', 'src/pages/test.njk');
    expect(errors).toHaveLength(0);
  });
});
