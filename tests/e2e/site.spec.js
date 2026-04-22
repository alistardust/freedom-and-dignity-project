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

  test('nav has 4 links', async ({ page }) => {
    await expect(page.locator('.nav-links a')).toHaveCount(4);
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

  test('has 18 total pillar cards across all foundations', async ({ page }) => {
    await expect(page.locator('a.f-pillar-card')).toHaveCount(18);
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

  test('fullview contains all 17 pillar links (18 with shared rights pillar)', async ({ page }) => {
    await expect(page.locator('a.pi-fv-pill')).toHaveCount(18);
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

  test('shows all 17 pillar index links', async ({ page }) => {
    await expect(page.locator('a.pillar-index-link')).toHaveCount(17);
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
  { slug: 'executive-power',           title: 'Executive Power' },
  { slug: 'healthcare',                title: 'Healthcare' },
  { slug: 'gun-policy',                title: 'Gun Policy' },
  { slug: 'environment-and-agriculture', title: 'Environment' },
];

for (const { slug, title } of SAMPLE_PILLARS) {
  test.describe(`Pillar page: ${title}`, () => {
    test.beforeEach(async ({ page }) => { await page.goto(`/pillars/${slug}.html`); });

    test('has correct title', async ({ page }) => {
      await expect(page).toHaveTitle(new RegExp(title.split(' ')[0], 'i'));
    });

    test('has Why This Matters section', async ({ page }) => {
      await expect(page.locator('text=Why This Matters')).toBeVisible();
    });

    test('has What It Demands and What It Rejects sections', async ({ page }) => {
      await expect(page.locator('text=What It Demands')).toBeVisible();
      await expect(page.locator('text=What It Rejects')).toBeVisible();
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
