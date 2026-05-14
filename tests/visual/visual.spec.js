// @ts-check
// BASELINE WORKFLOW: Snapshots must be generated on Linux (ubuntu-latest).
// To establish or update baselines:
//   1. Push branch to GitHub
//   2. Trigger the build-and-deploy workflow manually from Actions tab
//   3. Set update_snapshots = true
//   4. Download the 'visual-snapshots-updated' artifact
//   5. Commit the downloaded snapshots to tests/visual/visual.spec.js-snapshots/

const { test, expect } = require('@playwright/test');

// Five representative page types at two viewports each = 10 screenshots.
// Server: npx serve docs -p 5500 -n (defined in playwright.config.js webServer)
// Paths are relative to http://localhost:5500 — no /freedom-and-dignity-project/ prefix.

const PAGES = [
  { name: 'home',             path: '/' },
  { name: 'policy-area-healthcare', path: '/policy/healthcare.html' },
  { name: 'compare-republican', path: '/compare/republican-party.html' },
  { name: 'policyos',         path: '/policyos.html' },
  { name: 'policy-library',   path: '/policy-library.html' },
];

const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'mobile',  width: 390,  height: 844 },
];

for (const pg of PAGES) {
  for (const vp of VIEWPORTS) {
    test(`${pg.name} @ ${vp.name}`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto(pg.path);
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`${pg.name}-${vp.name}.png`, {
        maxDiffPixelRatio: 0.001,  // 0.1% threshold
        // fullPage omitted: policy area pages exceed the 32767px CDP screenshot limit.
        // Viewport-only screenshots are sufficient to catch layout/nav regressions.
      });
    });
  }
}
