import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './artifacts/playwright_tests',
  reporter: [['html', { open: 'never' }]],
  use: {
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
});
