// @ts-check
import { test, expect } from '@playwright/test';

/**
 * HOT-002 — Hot Topics page integrity
 *
 * Guards against the page being silently replaced by the mermaid flatmap at
 * /docs/hot-topics. The navbar "Hot Topics" link MUST point to /hot-topics
 * (the React filter page), not /docs/hot-topics (the generated docs section).
 *
 * See test log entry HOT-002 in a11yhub-test-log.md for full context.
 */

const HOT_TOPICS_URL = '/accessibility-hub/hot-topics';
const HOME_URL = '/accessibility-hub/';

test.describe('Hot Topics page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(HOT_TOPICS_URL);
  });

  // ── Navigation ─────────────────────────────────────────────────────────────

  test('navbar Hot Topics link resolves to the filter page', async ({ page }) => {
    await page.goto(HOME_URL);
    await page.getByRole('link', { name: 'Hot Topics' }).first().click();
    await expect(page).toHaveURL(/\/hot-topics\/?$/);
  });

  test('page is NOT the mermaid flatmap index', async ({ page }) => {
    await expect(page.locator('pre.mermaid, .mermaid')).not.toBeVisible();
  });

  // ── Filter UI presence ──────────────────────────────────────────────────────

  test('filter group is visible', async ({ page }) => {
    await expect(page.getByRole('group', { name: 'Filter topics by category' })).toBeVisible();
  });

  test('filter buttons are present and have correct ARIA', async ({ page }) => {
    const buttons = page.getByRole('button', { name: /Filter by category/i });
    await expect(buttons).toHaveCount(4);

    for (const btn of await buttons.all()) {
      await expect(btn).toHaveAttribute('aria-pressed', 'false');
    }
  });

  test('topic cards are visible on load', async ({ page }) => {
    const cards = page.locator('[aria-describedby="filter-context"] li');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });

  // ── Filter behaviour ────────────────────────────────────────────────────────

  test('activating a filter updates aria-pressed and live region', async ({ page }) => {
    const toolBtn = page.getByRole('button', { name: /Filter by category: Tool/i });
    await toolBtn.click();
    await expect(toolBtn).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('#filter-context')).not.toBeEmpty();
  });

  test('deactivating all filters restores full list', async ({ page }) => {
    const toolBtn = page.getByRole('button', { name: /Filter by category: Tool/i });
    await toolBtn.click();
    await toolBtn.click();
    await expect(toolBtn).toHaveAttribute('aria-pressed', 'false');
    await expect(page.locator('#filter-context')).toContainText('all');
  });

  // ── Keyboard accessibility ──────────────────────────────────────────────────

  test('filter button is keyboard-activatable with Space', async ({ page }) => {
    const toolBtn = page.getByRole('button', { name: /Filter by category: Tool/i });
    await toolBtn.focus();
    await page.keyboard.press('Space');
    await expect(toolBtn).toHaveAttribute('aria-pressed', 'true');
  });
});
