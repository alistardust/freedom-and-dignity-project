// @ts-check
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:5500',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      testMatch: ['**/site.spec.js'],
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
      testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 14'] },
      testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
    },
    {
      name: 'mobile-firefox',
      // Playwright has no Firefox mobile device preset — only Desktop Firefox and
      // Desktop Firefox HiDPI exist in the registry. Use a custom narrow viewport.
      // isMobile and hasTouch are not supported in Playwright's Firefox implementation.
      use: {
        browserName: 'firefox',
        viewport: { width: 390, height: 844 },
      },
      testMatch: ['**/site.spec.js', '**/mobile.spec.js'],
    },
    {
      name: 'visual-firefox',
      testDir: './tests/visual',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npx serve docs -p 5500 -n',
    url: 'http://localhost:5500',
    reuseExistingServer: !process.env.CI,
    timeout: 15000,
  },
});
