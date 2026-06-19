// @ts-check
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? 'github' : 'list',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  // Serve the pre-built site during tests.
  // In CI the build job runs first and produces the artifact;
  // locally you should run `npm run build` before `npm run test:e2e`.
  webServer: {
    command: 'npm run serve -- --port 3000 --no-open',
    url: 'http://localhost:3000/accessibility-hub/',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
  ],
});
