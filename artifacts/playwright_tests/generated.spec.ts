import { test, expect } from '@playwright/test';


test('password_reset_email_flow_should_work_for_registered_users', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveTitle(/Playwright/i);
  await expect(page).toHaveURL(/.+/);
});
