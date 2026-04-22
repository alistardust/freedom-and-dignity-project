/**
 * Playwright E2E tests — American Renewal Project
 * Browser: Firefox (isolated profile, never touches your existing Firefox)
 */

const { test, expect } = require('@playwright/test');

// ── HOMEPAGE ─────────────────────────────────────────────────────────────────

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/American Renewal/i);
  });

  test('displays the core quote without quotation marks', async ({ page }) => {
    await expect(page.locator('text=You can\'t be free if you\'re sick, homeless, or in debt').first()).toBeVisible();
    const content = await page.locator('.hero-statement.strong').textContent();
    expect(content).not.toMatch(/^[""\u201C]/);
  });

  test('renders the FDR block with his quote', async ({ page }) => {
    await expect(page.locator('.fdr-block')).toBeVisible();
    await expect(page.locator('text=Necessitous men are not free men')).toBeVisible();
  });

  test('renders all 8 FDR rights', async ({ page }) => {
    await expect(page.locator('.fdr-rights li')).toHaveCount(8);
  });

  test('renders all 5 foundation cards', async ({ page }) => {
    await expect(page.locator('.foundations-grid .f-card')).toHaveCount(5);
  });

  test('renders the 10 demands list', async ({ page }) => {
    await expect(page.locator('.demand-list li')).toHaveCount(10);
  });

  test('nav has 7 links (4 static + Mission, Constitution, About AI injected by app.js)', async ({ page }) => {
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

// ── FOUNDATIONS PAGE ──────────────────────────────────────────────────────────

test.describe('Foundations page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/foundations.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Foundations/i);
  });

  test('fullview grid shows all 5 foundations immediately', async ({ page }) => {
    await expect(page.locator('.fo-fullview')).toBeVisible();
    await expect(page.locator('a.fo-fv-card')).toHaveCount(5);
  });

  test('each foundation card links to its section', async ({ page }) => {
    for (const id of ['accountable-power','clean-democracy','equal-justice','real-freedom','freedom-to-thrive']) {
      await expect(page.locator(`a.fo-fv-card[href="#${id}"]`)).toBeVisible();
    }
  });

  test('renders all 5 foundation sections by id', async ({ page }) => {
    for (const id of ['accountable-power','clean-democracy','equal-justice','real-freedom','freedom-to-thrive']) {
      await expect(page.locator(`#${id}`)).toBeAttached();
    }
  });

  test('pillar cards are links to pillar pages', async ({ page }) => {
    const firstCard = page.locator('a.f-pillar-card').first();
    await expect(firstCard).toBeVisible();
    await expect(firstCard).toHaveAttribute('href', /pillars\//);
  });

  test('has architecture intro explaining foundations and pillars', async ({ page }) => {
    await expect(page.locator('.arch-intro')).toBeVisible();
    await expect(page.locator('text=What Is a Foundation').first()).toBeVisible();
  });

  test('has 23 total pillar cards across all foundations', async ({ page }) => {
    await expect(page.locator('a.f-pillar-card')).toHaveCount(23);
  });

  test('has 10 demand/reject blocks across 5 foundations', async ({ page }) => {
    await expect(page.locator('.f-block')).toHaveCount(10);
  });
});

// ── PILLARS INDEX ─────────────────────────────────────────────────────────────

test.describe('Pillars index', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/pillars/index.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Pillars/i);
  });

  test('fullview grid is visible immediately', async ({ page }) => {
    await expect(page.locator('.pi-fullview')).toBeVisible();
  });

  test('shows all 5 foundation columns in fullview', async ({ page }) => {
    await expect(page.locator('.pi-fv-col')).toHaveCount(5);
  });

  test('fullview contains all 22 pillar links (23 with shared rights pillar)', async ({ page }) => {
    await expect(page.locator('a.pi-fv-pill')).toHaveCount(23);
  });

  test('each fullview pillar pill links to a .html page', async ({ page }) => {
    const pills = await page.locator('a.pi-fv-pill').all();
    for (const pill of pills) {
      const href = await pill.getAttribute('href');
      expect(href).toMatch(/\.html$/);
    }
  });

  test('foundation headers link to foundations page', async ({ page }) => {
    const foundations = await page.locator('a.pi-fv-foundation').all();
    for (const f of foundations) {
      const href = await f.getAttribute('href');
      expect(href).toMatch(/foundations\.html#/);
    }
  });

  test('shows all 5 foundation index sections below fullview', async ({ page }) => {
    await expect(page.locator('.pillar-index-section')).toHaveCount(5);
  });

  test('shows all 22 pillar index links', async ({ page }) => {
    await expect(page.locator('a.pillar-index-link')).toHaveCount(22);
  });

  test('each pillar index link points to a .html page', async ({ page }) => {
    const links = await page.locator('a.pillar-index-link').all();
    for (const link of links) {
      const href = await link.getAttribute('href');
      expect(href).toMatch(/\.html$/);
    }
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

    test('has back link to foundations', async ({ page }) => {
      await expect(page.locator('a[href*="foundations.html"]').first()).toBeVisible();
    });
  });
}

// ── COMPARE PAGES ─────────────────────────────────────────────────────────────

test.describe('Compare index', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/compare/index.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Comparison|Compare/i);
  });

  test('shows all 6 parties', async ({ page }) => {
    for (const name of ['Democratic Party','Republican Party','Libertarian','Democratic Socialists','Working Families','Green Party']) {
      await expect(page.locator(`text=${name}`).first()).toBeVisible();
    }
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
  });
}

// ── NAVIGATION ────────────────────────────────────────────────────────────────

test.describe('Navigation', () => {
  test('home → foundations', async ({ page }) => {
    await page.goto('/');
    await page.click('a[href="foundations.html"]');
    await expect(page).toHaveURL(/foundations/);
  });

  test('foundations → pillars index', async ({ page }) => {
    await page.goto('/foundations.html');
    await page.click('a[href="pillars/index.html"]');
    await expect(page).toHaveURL(/pillars/);
  });

  test('pillars index → pillar page', async ({ page }) => {
    await page.goto('/pillars/index.html');
    // Verify the first link points to a .html file (href integrity)
    const href = await page.locator('a.pillar-index-link').first().getAttribute('href');
    expect(href).toMatch(/\.html$/);
    // Navigate directly to confirm that target page is valid
    await page.goto(`/pillars/${href}`);
    await expect(page.locator('.site-nav')).toBeVisible();
  });

  test('pillar page → back to foundations', async ({ page }) => {
    await page.goto('/pillars/healthcare.html');
    await page.locator('a[href*="foundations.html"]').first().click();
    await expect(page).toHaveURL(/foundations/);
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

  test('footer About AI link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="about-ai"]')).toBeAttached();
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
    { url: '/foundations.html',          label: 'Foundations' },
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

  test('renders AI transparency section', async ({ page }) => {
    await expect(page.locator('.ai-transparency-section')).toBeVisible();
  });

  test('AI transparency section has 3 fact cards', async ({ page }) => {
    await expect(page.locator('.ai-fact')).toHaveCount(3);
  });

  test('CTA button links to about-ai.html', async ({ page }) => {
    const cta = page.locator('.ai-transparency-section a[href*="about-ai"]');
    await expect(cta).toBeVisible();
    await cta.click();
    await expect(page).toHaveTitle(/AI|Artificial/i);
  });
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
    await expect(page.locator('#pil-policy .rule-card').first()).toBeAttached();
  });

  test('policy section has more than one rule card', async ({ page }) => {
    await page.goto(`/pillars/${pillarWithRules}.html`);
    await page.locator('#pil-policy').scrollIntoViewIfNeeded();
    const count = await page.locator('#pil-policy .rule-card').count();
    expect(count).toBeGreaterThan(1);
  });
});

// ── MISSION PAGE ──────────────────────────────────────────────────────────────

test.describe('Mission page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/mission.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Mission.*American Renewal/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.mission-hero h1')).toBeVisible();
  });

  test('hero contains "Mission" text', async ({ page }) => {
    const text = await page.locator('.mission-hero h1').textContent();
    expect(text).toMatch(/Mission/i);
  });

  test('nav Mission link is present', async ({ page }) => {
    // Mission link is injected by app.js — test presence and correct href
    const link = page.locator('.nav-links a[href*="mission"]');
    await expect(link).toBeAttached();
  });

  test('nav Mission link is marked active on mission page', async ({ page }) => {
    // Injected links get class="active" from pageName detection in app.js
    const link = page.locator('.nav-links a[href*="mission"].active');
    await expect(link).toBeAttached();
  });

  test('footer Mission link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="mission"]')).toBeAttached();
  });

  test('footer Constitution link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="constitution"]')).toBeAttached();
  });

  test('renders 6 commitment cards', async ({ page }) => {
    // 6 What It Does commitments
    await expect(page.locator('.mission-commit')).toHaveCount(6);
  });

  test('nav has About AI link', async ({ page }) => {
    await expect(page.locator('.nav-links a[href*="about-ai"]')).toBeAttached();
  });

  test('references section is present', async ({ page }) => {
    await expect(page.locator('#page-refs')).toBeAttached();
  });
});

// ── CONSTITUTION PAGE ─────────────────────────────────────────────────────────

test.describe('Constitution page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/constitution.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Constitution.*American Renewal/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.const-hero h1')).toBeVisible();
  });

  test('hero contains "Constitution" text', async ({ page }) => {
    const text = await page.locator('.const-hero h1').textContent();
    expect(text).toMatch(/Constitution/i);
  });

  test('nav Constitution link is present', async ({ page }) => {
    // Constitution link is injected by app.js — test presence and correct href
    const link = page.locator('.nav-links a[href*="constitution"]');
    await expect(link).toBeAttached();
  });

  test('footer Constitution link is present', async ({ page }) => {
    await expect(page.locator('.footer-links a[href*="constitution"]')).toBeAttached();
  });

  test('referendum and recall section is present', async ({ page }) => {
    await expect(page.locator('.const-reform-box')).toBeAttached();
  });

  test('referendum and recall section mentions National Referendum', async ({ page }) => {
    const text = await page.locator('.const-reform-box').textContent();
    expect(text).toMatch(/National Referendum/i);
  });

  test('recall section mentions Recall', async ({ page }) => {
    const text = await page.locator('.const-reform-box').textContent();
    expect(text).toMatch(/Recall/i);
  });

  test('references section is present', async ({ page }) => {
    await expect(page.locator('#page-refs')).toBeAttached();
  });

  test('vulnerabilities list renders', async ({ page }) => {
    await expect(page.locator('.const-vuln')).toHaveCount(6);
  });

  test('amendment list renders', async ({ page }) => {
    await expect(page.locator('.const-amend')).toHaveCount(6);
  });
});

// ── ROADMAP PAGE ──────────────────────────────────────────────────────────────

test.describe('Roadmap page', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/roadmap.html'); });

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Roadmap.*American Renewal/i);
  });

  test('renders hero heading', async ({ page }) => {
    await expect(page.locator('.roadmap-hero h1')).toBeVisible();
  });

  test('hero contains "Roadmap" text', async ({ page }) => {
    const text = await page.locator('.roadmap-hero h1').textContent();
    expect(text).toMatch(/Roadmap/i);
  });

  test('renders 6 roadmap tracks', async ({ page }) => {
    // 6 tracks: Policy Dev, Organization, Outreach, Fundraising, Content & Branding, Technical
    await expect(page.locator('.roadmap-track')).toHaveCount(6);
  });

  test('nav has Mission and Constitution links', async ({ page }) => {
    await expect(page.locator('.nav-links a[href*="mission"]')).toBeAttached();
    await expect(page.locator('.nav-links a[href*="constitution"]')).toBeAttached();
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

// ── MISSION/CONSTITUTION REACHABLE FROM ALL PAGE TYPES ───────────────────────

test.describe('Mission and Constitution nav links from all page types', () => {
  const pages = [
    { url: '/',                               label: 'Homepage' },
    { url: '/foundations.html',              label: 'Foundations' },
    { url: '/pillars/index.html',            label: 'Pillars index' },
    { url: '/pillars/healthcare.html',       label: 'Pillar page' },
    { url: '/compare/index.html',            label: 'Compare index' },
  ];

  for (const { url, label } of pages) {
    test(`${label} has Mission in nav`, async ({ page }) => {
      await page.goto(url);
      const link = page.locator('.nav-links a[href*="mission"]');
      await expect(link).toBeAttached();
      const href = await link.getAttribute('href');
      await page.goto(href.startsWith('http') ? href : new URL(href, page.url()).toString());
      await expect(page).toHaveTitle(/Mission.*American Renewal/i);
    });

    test(`${label} has Constitution in nav`, async ({ page }) => {
      await page.goto(url);
      const link = page.locator('.nav-links a[href*="constitution"]');
      await expect(link).toBeAttached();
      const href = await link.getAttribute('href');
      await page.goto(href.startsWith('http') ? href : new URL(href, page.url()).toString());
      await expect(page).toHaveTitle(/Constitution.*American Renewal/i);
    });
  }
});
