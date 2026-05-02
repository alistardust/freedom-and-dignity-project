/**
 * Playwright E2E tests — Freedom and Dignity Project
 * Browser: Firefox (isolated profile, never touches your existing Firefox)
 */

const { test, expect } = require('@playwright/test');

// ── SHARED CONSTANTS ──────────────────────────────────────────────────────────
// Update PILLAR_COUNT when adding pillars to data.js.
// All count assertions below derive from this constant.
const PILLAR_COUNT = 25; // pillars in data.js

// ── HOMEPAGE ─────────────────────────────────────────────────────────────────

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Freedom and Dignity/i);
  });

  test('displays hero mission statement', async ({ page }) => {
    const statement = await page.locator('.hero-mission').textContent();
    expect(statement).toBeTruthy();
    expect(statement.trim().length).toBeGreaterThan(20);
  });

  test('renders the FDR block with his quote', async ({ page }) => {
    await expect(page.locator('.fdr-block')).toBeVisible();
    await expect(page.locator('text=Necessitous men are not free men')).toBeVisible();
  });

  test('renders the PolicyOS 3-layer cards', async ({ page }) => {
    // The approach section shows 3 PolicyOS layer cards
    await expect(page.locator('.policyos-layers .layer-card')).toHaveCount(3);
  });

  test('renders all 5 foundation cards', async ({ page }) => {
    await expect(page.locator('.foundations-grid .f-card')).toHaveCount(5);
  });

  test('renders all 4 Get Involved entry cards', async ({ page }) => {
    // 4 entry cards: Explore, Review, Build, Community
    await expect(page.locator('.entry-grid .entry-card')).toHaveCount(4);
  });

  test('nav has 7 links (6 static + About AI injected by app.js)', async ({ page }) => {
    // 6 static: Home, Problem, Approach, Proposals, Get Involved, Roadmap + 1 injected: About AI
    await expect(page.locator('.nav-links a')).toHaveCount(7);
  });

  test('name notice banner is present and dismissible', async ({ page }) => {
    // Banner should appear on fresh page load (no sessionStorage flag)
    const banner = page.locator('.name-notice-banner');
    await expect(banner).toBeAttached();
    await expect(banner).toContainText('placeholder');
    await expect(banner).toContainText('no affiliation');

    // Dismiss button removes the banner
    await page.locator('.name-notice-dismiss').click();
    await expect(banner).not.toBeAttached();
  });
});

// ── PILLARS INDEX ─────────────────────────────────────────────────────────────

test.describe('Pillars index', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/pillars/index.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Pillars/i);
  });

  test('fullview header is visible immediately', async ({ page }) => {
    await expect(page.locator('.pi-fullview')).toBeVisible();
  });

  test('shows all 5 foundation accordions', async ({ page }) => {
    await expect(page.locator('.pil-foundation-accordion')).toHaveCount(5);
  });

  test('all 5 foundation accordions start collapsed by default', async ({ page }) => {
    const accordions = await page.locator('.pil-foundation-accordion').all();
    for (const accordion of accordions) {
      expect(await accordion.getAttribute('open')).toBeNull();
    }
  });

  test(`accordion grid contains all ${PILLAR_COUNT} pillar links`, async ({ page }) => {
    await expect(page.locator('a.pil-pillar-link')).toHaveCount(PILLAR_COUNT);
  });

  test('each pillar link points to a .html page', async ({ page }) => {
    const links = await page.locator('a.pil-pillar-link').all();
    for (const link of links) {
      const href = await link.getAttribute('href');
      expect(href).toMatch(/\.html$/);
    }
  });

  test('clicking a foundation bar opens it and reveals pillar cards', async ({ page }) => {
    const first = page.locator('.pil-foundation-accordion').first();
    await first.locator('summary').click();
    await expect(first).toHaveAttribute('open', '');
    await expect(first.locator('.pil-pillar-card').first()).toBeVisible();
  });
});

// ── INDIVIDUAL PILLAR PAGES ───────────────────────────────────────────────────

const SAMPLE_PILLARS = [
  { slug: 'executive-power',               title: 'Executive Power' },
  { slug: 'elections-and-representation',  title: 'Elections' },
  { slug: 'anti-corruption',               title: 'Anti-Corruption' },
  { slug: 'equal-justice-and-policing',    title: 'Equal Justice' },
  { slug: 'rights-and-civil-liberties',    title: 'Rights' },
  { slug: 'courts-and-judicial-system',    title: 'Courts' },
  { slug: 'checks-and-balances',           title: 'Checks' },
  { slug: 'taxation-and-wealth',           title: 'Taxation' },
  { slug: 'healthcare',                    title: 'Healthcare' },
  { slug: 'antitrust-and-corporate-power', title: 'Antitrust' },
  { slug: 'information-and-media',         title: 'Information' },
  { slug: 'gun-policy',                    title: 'Gun Policy' },
  { slug: 'term-limits-and-fitness',       title: 'Term Limits' },
  { slug: 'administrative-state',          title: 'Administrative' },
  { slug: 'technology-and-ai',             title: 'Technology' },
  { slug: 'immigration',                   title: 'Immigration' },
  { slug: 'environment-and-agriculture',   title: 'Environment' },
  { slug: 'education',                     title: 'Education' },
  { slug: 'labor-and-workers-rights',      title: 'Labor' },
  { slug: 'housing',                       title: 'Housing' },
  { slug: 'consumer-rights',              title: 'Consumer' },
  { slug: 'legislative-reform',            title: 'Legislative' },
  { slug: 'foreign-policy',               title: 'Foreign Policy' },
  { slug: 'science-technology-space',     title: 'Science Technology Space' },
];

for (const { slug, title } of SAMPLE_PILLARS) {
  test.describe(`Pillar page: ${title}`, () => {
    test.beforeEach(async ({ page }) => { await page.goto(`/pillars/${slug}.html`); });

    test('has correct title', async ({ page }) => {
      await expect(page).toHaveTitle(new RegExp(title.split(' ')[0], 'i'));
    });

    test('has Purpose section', async ({ page }) => {
      await expect(page.locator('#pil-intro')).toBeVisible();
    });

    test('has Full Policy Platform section', async ({ page }) => {
      await expect(page.locator('#pil-policy')).toBeVisible();
    });

    test('has back link to platform', async ({ page }) => {
      await expect(page.locator('a[href*="platform.html"]').first()).toBeVisible();
    });
  });
}

// ── COMPARE PAGES ─────────────────────────────────────────────────────────────

test.describe('Compare index', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/compare/index.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Why This Project Differs/i);
  });

  test('shows all 6 parties', async ({ page }) => {
    for (const name of ['Democratic Party','Republican Party','Libertarian','Democratic Socialists','Working Families','Green Party']) {
      await expect(page.locator(`text=${name}`).first()).toBeVisible();
    }
  });

  test('frames the section as Why This Project Differs', async ({ page }) => {
    await expect(page.locator('h1.hero-title')).toHaveText(/Why This Project Differs/i);
    await expect(page.locator('.hero-statement')).toContainText('distinct structural logic');
  });

  test('compare cards use the new read label', async ({ page }) => {
    await expect(page.locator('.cmp-card')).toHaveCount(6);
    await expect(page.locator('.cmp-card-link')).toHaveCount(6);
    await expect(page.locator('.cmp-card-link').first()).toHaveText(/Read Why We Differ/i);
  });

  test('has quick reference and next-step sections', async ({ page }) => {
    await expect(page.locator('#cmp-table')).toBeVisible();
    await expect(page.locator('.compare-next-card')).toHaveCount(3);
  });
});

const PARTY_PAGES = [
  { file: 'democratic-party.html',       name: 'Democratic Party' },
  { file: 'republican-party.html',       name: 'Republican Party' },
  { file: 'libertarian-party.html',      name: 'Libertarian' },
  { file: 'dsa.html',                    name: 'Democratic Socialists' },
  { file: 'working-families-party.html', name: 'Working Families' },
  { file: 'green-party.html',            name: 'Green Party' },
];

for (const { file, name } of PARTY_PAGES) {
  test.describe(`Compare: ${name}`, () => {
    test.beforeEach(async ({ page }) => { await page.goto(`/compare/${file}`); });

    test('loads with nav visible', async ({ page }) => {
      await expect(page.locator('.site-nav')).toBeVisible();
    });

    test('has a coverage/gap section', async ({ page }) => {
      const count = await page.locator('[class*="cov"], [class*="coverage"], [class*="gap"]').count();
      expect(count).toBeGreaterThan(0);
    });

    test('does not mention coalition likelihood', async ({ page }) => {
      const body = await page.locator('body').textContent();
      expect(body.toLowerCase()).not.toContain('coalition likelihood');
      expect(body.toLowerCase()).not.toContain('coalition score');
    });

    test('section nav uses the rewritten labels', async ({ page }) => {
      await expect(page.locator('.cmp-snav')).toContainText('What This Page Clarifies');
      await expect(page.locator('.cmp-snav')).toContainText('Why This Project Differs');
    });

    test('has sources and next-step sections', async ({ page }) => {
      await expect(page.locator('#cmp-sources')).toBeVisible();
      await expect(page.locator('.compare-next-card')).toHaveCount(3);
    });
  });
}

// ── NAVIGATION ────────────────────────────────────────────────────────────────

test.describe('Navigation', () => {
  test('home → proposals', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="policy-library.html"]');
    await expect(page).toHaveURL(/proposals/);
  });

  test('platform → proposals page', async ({ page }) => {
    await page.goto('/platform.html');
    await page.click('.nav-links a[href*="proposals"]');
    await expect(page).toHaveURL(/proposals/);
  });

  test('pillars index → pillar page', async ({ page }) => {
    await page.goto('/pillars/index.html');
    // Verify the first link points to a .html file (href integrity)
    const href = await page.locator('a.pil-pillar-link').first().getAttribute('href');
    expect(href).toMatch(/\.html$/);
    // Navigate directly to confirm that target page is valid
    await page.goto(`/pillars/${href}`);
    await expect(page.locator('.site-nav')).toBeVisible();
  });

  test('pillar page → back to platform', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    await page.locator('a[href*="platform.html"]').first().click();
    await expect(page).toHaveURL(/platform/);
  });

  test('pillars index → compare', async ({ page }) => {
    await page.goto('/pillars/index.html');
    await page.click('a[href="../compare/index.html"]');
    await expect(page).toHaveURL(/compare/);
  });
});

// ── ABOUT AI PAGE ─────────────────────────────────────────────────────────────

test.describe('About AI page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/about-ai.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/AI|Artificial/i);
  });

  test('renders main transparency statement heading', async ({ page }) => {
    await expect(page.locator('.ai-hero h1')).toBeVisible();
  });

  test('nav About AI link is active', async ({ page }) => {
    await expect(page.locator('.nav-links a.active')).toHaveText(/About AI/i);
  });

  test('footer has standard links', async ({ page }) => {
    // about-ai footer omits the self-referential AI link; verify standard items
    await expect(page.locator('.footer-links a[href*="platform"]')).toBeAttached();
    await expect(page.locator('.footer-links a[href*="about-us"]')).toBeAttached();
    await expect(page.locator('.footer-links a[href*="compare"]')).toBeAttached();
  });

  test('AI harms section is present', async ({ page }) => {
    // The "Real Cost of AI" section must exist with all three harm categories
    const body = await page.locator('.ai-body').textContent();
    expect(body).toMatch(/Real Cost of AI/i);
    expect(body).toMatch(/Economic disruption/i);
    expect(body).toMatch(/Algorithmic harm/i);
    expect(body).toMatch(/Environmental cost/i);
  });

  test('"no going back" pullquote is present', async ({ page }) => {
    const pullquotes = page.locator('.ai-pullquote');
    // Page has multiple pullquotes; one must reference un-inventing AI
    const texts = await pullquotes.allTextContents();
    expect(texts.some(t => /un-inventing|no longer whether/i.test(t))).toBe(true);
  });

  test('Technology & AI pillar link is present in harms section', async ({ page }) => {
    const link = page.locator('.ai-body a[href*="technology-and-ai"]').first();
    await expect(link).toBeAttached();
  });

  test('models section includes ChatGPT', async ({ page }) => {
    const grid = await page.locator('.ai-models-grid').textContent();
    expect(grid).toMatch(/ChatGPT/i);
  });

  test('completeness note about missed models is present', async ({ page }) => {
    const note = await page.locator('.ai-note').first().textContent();
    // The first .ai-note is the technical note; check the completeness note
    const notes = await page.locator('.ai-note').allTextContents();
    expect(notes.some(n => /completeness|not.*logged|earlier.*phase/i.test(n))).toBe(true);
  });

  test('references section has at least 6 citations', async ({ page }) => {
    // 2 original + 6 new harms citations = 8 total
    const refs = page.locator('.ai-footnotes p[id^="fn"]');
    const count = await refs.count();
    expect(count).toBeGreaterThanOrEqual(6);
  });
});

// ── ABOUT AI ACCESSIBILITY (all pages) ───────────────────────────────────────

test.describe('About AI link reachable from all page types', () => {
  const pages = [
    { url: '/',                          label: 'Homepage' },
    { url: '/policy-library.html',          label: 'Proposals' },
    { url: '/pillars/index.html',        label: 'Pillars index' },
    { url: '/pillars/healthcare.html',   label: 'Pillar page' },
    { url: '/compare/index.html',        label: 'Compare index' },
    { url: '/compare/republican-party.html', label: 'Compare page' },
  ];

  for (const { url, label } of pages) {
    test(`${label} has About AI in nav`, async ({ page }) => {
      await page.goto(url);
      const link = page.locator('.nav-links a[href*="about-ai"]');
      await expect(link).toBeAttached();
      const href = await link.getAttribute('href');
      // Must not be a broken cross-root path (../about-ai.html from root pages was the bug)
      // Navigate to it and expect the About AI page to load
      await page.goto(href.startsWith('http') ? href : new URL(href, page.url()).toString());
      await expect(page).toHaveTitle(/AI|Artificial/i);
    });
  }
});

// ── BACK-TO-TOP BUTTON ────────────────────────────────────────────────────────

test.describe('Back-to-top button', () => {
  test('is hidden at page top', async ({ page }) => {
    await page.goto('/');
    const btn = page.locator('#back-to-top');
    await expect(btn).toBeAttached();
    // Should not have btt-visible class at the top
    await expect(btn).not.toHaveClass(/btt-visible/);
  });

  test('appears after scrolling down on a tall page', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    await page.evaluate(() => window.scrollTo(0, 1000));
    await expect(page.locator('#back-to-top')).toHaveClass(/btt-visible/);
  });

  test('scrolls back to top when clicked', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    await page.evaluate(() => window.scrollTo(0, 1000));
    await page.locator('#back-to-top').click();
    await page.waitForFunction(() => window.scrollY < 50);
    const y = await page.evaluate(() => window.scrollY);
    expect(y).toBeLessThan(50);
  });
});

// ── HOMEPAGE AI TRANSPARENCY SECTION ─────────────────────────────────────────

test.describe('Homepage AI transparency section', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); });

});

// ── POLICY RULES SECTION VISIBILITY ──────────────────────────────────────────

test.describe('Policy rules section renders content', () => {
  // Tests the IntersectionObserver threshold:0 fix — #pil-policy must become
  // visible when scrolled into view (not stay at opacity:0 forever)
  const pillarWithRules = 'healthcare'; // 184 rules — guaranteed to have content

  test('policy section is attached to DOM', async ({ page }) => {
    await page.goto(`/pillars/${pillarWithRules}.html`);
    await expect(page.locator('#pil-policy')).toBeAttached();
  });

  test('policy section contains at least one rule card after scroll', async ({ page }) => {
    await page.goto(`/pillars/${pillarWithRules}.html`);
    await page.locator('#pil-policy').scrollIntoViewIfNeeded();
    // Wait for IntersectionObserver to fire and .visible class to be applied
    await expect(page.locator('#pil-policy')).toHaveClass(/visible/, { timeout: 3000 });
    await expect(page.locator('#pil-policy .policy-card').first()).toBeAttached();
  });

  test('policy section has more than one rule card', async ({ page }) => {
    await page.goto(`/pillars/${pillarWithRules}.html`);
    await page.locator('#pil-policy').scrollIntoViewIfNeeded();
    const count = await page.locator('#pil-policy .policy-card').count();
    expect(count).toBeGreaterThan(1);
  });
});

// ── MISSION PAGE ──────────────────────────────────────────────────────────────

test.describe('Mission page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/problem.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Problem|Mission.*Freedom and Dignity/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.page-hero-standard h1')).toBeVisible();
  });

  test('hero contains "Problem" text', async ({ page }) => {
    const text = await page.locator('.page-hero-standard h1').textContent();
    expect(text).toMatch(/Problem/i);
  });

  test('nav Mission link is present', async ({ page }) => {
    // Mission link is baked into the HTML nav as "Problem"
    const link = page.locator('.nav-links a[href*="mission"]');
    await expect(link).toBeAttached();
  });

  test('nav Mission link is marked active on mission page', async ({ page }) => {
    const link = page.locator('.nav-links a[href*="mission"].active');
    await expect(link).toBeAttached();
  });

  test('footer Mission link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="mission"]')).toBeAttached();
  });

  test('footer Rights link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="rights"]')).toBeAttached();
  });

  test('renders 5 foundation cards', async ({ page }) => {
    // Six Commitments replaced with Five Structural Foundations (fo-fv-grid)
    await expect(page.locator('.fo-fv-grid .fo-fv-card')).toHaveCount(5);
  });

  test('nav has About AI link', async ({ page }) => {
    await expect(page.locator('.nav-links a[href*="about-ai"]')).toBeAttached();
  });

  test('references section is present', async ({ page }) => {
    await expect(page.locator('#page-refs')).toBeAttached();
  });
});

// ── PROPOSALS PAGE ───────────────────────────────────────────────────────────

test.describe('Proposals page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/policy-library.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Proposals.*Freedom and Dignity/i);
  });

  test('renders 3 PolicyOS layer cards', async ({ page }) => {
    await expect(page.locator('.policyos-layers .layer-card')).toHaveCount(3);
  });

  test('renders 5 foundation cards', async ({ page }) => {
    await expect(page.locator('.fo-fv-card')).toHaveCount(5);
  });

  test('renders 3 rights framework cards', async ({ page }) => {
    await expect(page.locator('.rights-cards-grid .rights-card')).toHaveCount(3);
  });

  test('proposals link is active in nav', async ({ page }) => {
    await expect(page.locator('.nav-links a.active[href*="proposals"]')).toBeAttached();
  });
});

// ── RIGHTS PAGE ───────────────────────────────────────────────────────────────

test.describe('Rights page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/rights.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Rights.*Freedom and Dignity/i);
  });

  test('renders New Bill of Rights section', async ({ page }) => {
    await expect(page.locator('#new-bill-of-rights')).toBeAttached();
  });

  test('renders Workers Rights section', async ({ page }) => {
    await expect(page.locator('#workers-rights')).toBeAttached();
  });

  test('renders Indigenous Rights section', async ({ page }) => {
    await expect(page.locator('#indigenous-rights')).toBeAttached();
  });

  test('rights-item entries are present', async ({ page }) => {
    const count = await page.locator('.rights-item').count();
    expect(count).toBeGreaterThan(10);
  });

  test('footer Rights link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="rights"]')).toBeAttached();
  });
});

// ── PLATFORM PAGE ─────────────────────────────────────────────────────────────

test.describe('Platform page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/platform.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Platform.*Freedom and Dignity/i);
  });

  test('renders all 5 foundation sections', async ({ page }) => {
    for (const id of ['accountable-power','clean-democracy','equal-justice','real-freedom','freedom-to-thrive']) {
      await expect(page.locator(`#${id}`)).toBeAttached();
    }
  });

  test('pillar cards are links to pillar pages', async ({ page }) => {
    const firstCard = page.locator('a.f-pillar-card').first();
    await expect(firstCard).toBeVisible();
    await expect(firstCard).toHaveAttribute('href', /pillars\//);
  });

  test(`has ${PILLAR_COUNT} total pillar cards across all foundations`, async ({ page }) => {
    // PILLAR_COUNT + 1 because rights_and_civil_liberties is a cross-pillar card appearing in both Foundation III and IV
    await expect(page.locator('a.f-pillar-card')).toHaveCount(PILLAR_COUNT + 1);
  });

  test('footer Platform link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="platform"]')).toBeAttached();
  });

  test('footer About link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="about-us"]')).toBeAttached();
  });

  test('footer Perspectives link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="compare"]')).toBeAttached();
  });
});

// ── ROADMAP PAGE ──────────────────────────────────────────────────────────────

test.describe('Roadmap page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/roadmap.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Roadmap.*Freedom and Dignity/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.roadmap-hero h1')).toBeVisible();
  });

  test('hero contains "Roadmap" text', async ({ page }) => {
    const text = await page.locator('.roadmap-hero h1').textContent();
    expect(text).toMatch(/Roadmap/i);
  });

  test('renders 6 roadmap tracks', async ({ page }) => {
    // Track 00 (Strategic Direction) + Track 01–06 = 7 total
    await expect(page.locator('.roadmap-track')).toHaveCount(7);
  });

  test('nav has Mission and Roadmap links', async ({ page }) => {
    await expect(page.locator('.nav-links a[href*="mission"]')).toBeAttached();
    await expect(page.locator('.nav-links a[href*="roadmap"]')).toBeAttached();
  });
});

// ── ELECTIONS PILLAR — REFERENDUM AND RECALL ─────────────────────────────────

test.describe('Elections pillar — Referendum and Recall section', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/pillars/elections-and-representation.html'); });

  test('Referendum & Recall section exists', async ({ page }) => {
    await expect(page.locator('#pil-direct-democracy')).toBeAttached();
  });

  test('Referendum & Recall section contains ELE-DIR-001', async ({ page }) => {
    const text = await page.locator('#pil-direct-democracy').textContent();
    expect(text).toMatch(/ELE-DIR-001/);
  });

  test('Referendum & Recall section contains ELE-DIR-002', async ({ page }) => {
    const text = await page.locator('#pil-direct-democracy').textContent();
    expect(text).toMatch(/ELE-DIR-002/);
  });

  test('snav contains Referendum & Recall link', async ({ page }) => {
    await expect(page.locator('.pil-snav a[href="#pil-direct-democracy"]')).toBeAttached();
  });
});

// ── MISSION NAV LINK REACHABLE FROM ALL PAGE TYPES ───────────────────────────

test.describe('Mission nav link from all page types', () => {
  const pages = [
    { url: '/',                               label: 'Homepage' },
    { url: '/policy-library.html',              label: 'Proposals' },
    { url: '/pillars/index.html',            label: 'Pillars index' },
    { url: '/pillars/healthcare.html',       label: 'Pillar page' },
    { url: '/compare/index.html',            label: 'Compare index' },
  ];

  for (const { url, label } of pages) {
    test(`${label} has Mission/Problem in nav`, async ({ page }) => {
      await page.goto(url);
      const link = page.locator('.nav-links a[href*="mission"]');
      await expect(link).toBeAttached();
      const href = await link.getAttribute('href');
      await page.goto(href.startsWith('http') ? href : new URL(href, page.url()).toString());
      await expect(page).toHaveTitle(/Problem|Mission.*Freedom and Dignity/i);
    });
  }
});

// ── GET INVOLVED PAGE ─────────────────────────────────────────────────────────

test.describe('Get Involved page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/get-involved.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Get Involved.*Freedom and Dignity/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.page-hero-standard h1')).toBeVisible();
    const text = await page.locator('.page-hero-standard h1').textContent();
    expect(text).toMatch(/Get Involved/i);
  });

  test('renders 4 entry cards', async ({ page }) => {
    // Discord, GitHub, Policy Review, Research/Writing
    await expect(page.locator('.entry-card')).toHaveCount(4);
  });

  test('renders community need items', async ({ page }) => {
    // 8 gi-need-items in the main connect section
    await expect(page.locator('.gi-need-item')).toHaveCount(12);
  });

  test('GitHub repo link is present and correct', async ({ page }) => {
    const links = page.locator('a[href*="github.com/alistardust"]');
    await expect(links.first()).toBeAttached();
  });

  test('Discord link is present', async ({ page }) => {
    await expect(page.locator('a[href*="discord"]').first()).toBeAttached();
  });

  test('nav has Get Involved as active link', async ({ page }) => {
    const link = page.locator('.nav-links a[href*="get-involved"]');
    await expect(link).toBeAttached();
    await expect(link).toHaveClass(/active/);
  });
});


test.describe('About Us page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/about-us.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/About Us.*Freedom and Dignity/i);
  });

  test('displays the founder name', async ({ page }) => {
    await expect(page.locator('.profile-name')).toBeVisible();
    await expect(page.locator('.profile-name')).toHaveText('Alice Thomas');
  });

  test('mentions Northwest Whitfield High School', async ({ page }) => {
    await expect(page.locator('text=Northwest Whitfield High School')).toBeVisible();
  });

  test('mentions Southern Polytechnic State University', async ({ page }) => {
    await expect(page.locator('text=Southern Polytechnic State University')).toBeVisible();
  });

  test('faith section is present', async ({ page }) => {
    await expect(page.locator('text=Grove Level Baptist Church')).toBeVisible();
  });

  test('faith section includes key scripture references', async ({ page }) => {
    const body = await page.locator('.about-body').textContent();
    expect(body).toMatch(/Matthew 22:37/);
    expect(body).toMatch(/1 Corinthians 13/);
    expect(body).toMatch(/1 John 4/);
    expect(body).toMatch(/Matthew 25:40/);
  });

  test('values list has 4 items', async ({ page }) => {
    await expect(page.locator('.values-list li')).toHaveCount(4);
  });

  test('mentions the dogs Chipper and Riley', async ({ page }) => {
    const text = await page.locator('.about-body').textContent();
    expect(text).toMatch(/Chipper/);
    expect(text).toMatch(/Riley/);
  });

  test('contributor notice is present and links to about-ai', async ({ page }) => {
    await expect(page.locator('.contrib-notice')).toBeVisible();
    await expect(page.locator('.contrib-notice a[href*="about-ai"]')).toBeAttached();
  });

  test('nav has get-involved link visible', async ({ page }) => {
    // about-us is no longer a nav item; verify core nav links still present
    await expect(page.locator('.nav-links a[href*="get-involved"]')).toBeAttached();
  });

  test('funding disclosure is present', async ({ page }) => {
    const text = await page.locator('.contrib-notice').textContent();
    expect(text).toMatch(/no outside funding|no.*funding/i);
    expect(text).toMatch(/volunteer|compensation/i);
  });

  test('letter from the founder link is present', async ({ page }) => {
    await expect(page.locator('a[href*="letter-from-the-founder"]')).toBeAttached();
  });
});

// ── LETTER FROM THE FOUNDER PAGE ──────────────────────────────────────────────

test.describe('Letter from the Founder page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/letter-from-the-founder.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Letter.*Founder.*Freedom and Dignity/i);
  });

  test('renders the hero heading', async ({ page }) => {
    const h1 = page.locator('.lf-hero h1');
    await expect(h1).toBeVisible();
    const text = await h1.textContent();
    expect(text).toMatch(/Letter from the Founder/i);
  });

  test('letter body opens with verbatim first paragraph', async ({ page }) => {
    const first = page.locator('.lf-letter p').first();
    await expect(first).toContainText('Hi,');
  });

  test('letter body contains key verbatim content', async ({ page }) => {
    const body = await page.locator('.lf-letter').textContent();
    expect(body).toMatch(/Alice Thomas/);
    expect(body).toMatch(/Hank Aaron/);
    expect(body).toMatch(/Dalton/i);
  });

  test('all 18 footnote anchors are present', async ({ page }) => {
    // fn1 through fn18 — in-text citation anchors
    for (let i = 1; i <= 18; i++) {
      await expect(page.locator(`#ref${i}`)).toBeAttached();
    }
  });

  test('references section is present with at least 17 entries', async ({ page }) => {
    const refs = page.locator('.lf-references');
    await expect(refs).toBeAttached();
    const items = page.locator('.lf-ref-list > li');
    const count = await items.count();
    expect(count).toBeGreaterThanOrEqual(17);
  });

  test('nav has mission link visible', async ({ page }) => {
    // letter-from-the-founder is no longer a nav item; verify core nav links still present
    await expect(page.locator('.nav-links a[href*="mission"]')).toBeAttached();
  });

  test('nav and footer are injected', async ({ page }) => {
    // app.js injects nav links and footer — verify both are present
    await expect(page.locator('.nav-links a[href*="mission"]')).toBeAttached();
    await expect(page.locator('.site-footer')).toBeVisible();
  });

  test('footer has standard links', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="platform"]')).toBeAttached();
    await expect(page.locator('.footer-links a[href*="about-us"]')).toBeAttached();
    await expect(page.locator('.footer-links a[href*="compare"]')).toBeAttached();
  });
});
