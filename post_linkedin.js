/**
 * LinkedIn Auto-Post — Playwright CDP
 * Uses high-level Playwright locators (not raw page.evaluate for clicks)
 * Clipboard-based paste for reliable Urdu/Unicode text insertion
 */
const fs   = require('fs');
const path = require('path');
const http = require('http');

const BASE = 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment';
const PORT = 9222;

// ── Load config ───────────────────────────────────────────────────────────────
const configPath = process.argv[2] || path.join(BASE, 'post_config.json');
if (!fs.existsSync(configPath)) {
  console.error(`[POST] ERROR: Config not found: ${configPath}`); process.exit(1);
}
const cfg        = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const POST_TEXT  = (cfg.text  || '').trim();
const IMAGE_PATH = (cfg.image || '').trim() || null;
if (!POST_TEXT) { console.error('[POST] ERROR: text empty.'); process.exit(1); }
console.log(`[POST] Text: ${POST_TEXT.length} chars | Image: ${IMAGE_PATH || 'none'}`);

// ── Helpers ───────────────────────────────────────────────────────────────────
async function ss(page, name) {
  try {
    await page.screenshot({ path: path.join(BASE, `${name}.png`), timeout: 10000 });
    console.log(`[POST]   Screenshot: ${name}.png`);
  } catch (e) { console.log(`[POST]   Screenshot ${name} failed: ${e.message}`); }
}

async function cdpReady(port, ms = 3000) {
  const t = Date.now();
  while (Date.now() - t < ms) {
    try {
      await new Promise((ok, ko) => http.get(`http://localhost:${port}/json/version`,
        r => { r.resume(); r.on('end', ok); }).on('error', ko));
      return true;
    } catch { await new Promise(r => setTimeout(r, 400)); }
  }
  return false;
}

// ── Main ──────────────────────────────────────────────────────────────────────
(async () => {
  const chromium = require('playwright').chromium;

  if (!(await cdpReady(PORT, 5000))) {
    console.error('[POST] ERROR: Chrome not on port 9222. Run launch_chrome_debug.bat first.');
    process.exit(1);
  }

  const browser = await chromium.connectOverCDP(`http://localhost:${PORT}`);
  const context = browser.contexts()[0];
  let page = context.pages().find(p => p.url().includes('linkedin')) || context.pages()[0];
  if (!page) page = await context.newPage();

  // 1. Go to feed
  console.log('[POST] Navigating to LinkedIn feed...');
  await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.bringToFront();
  await page.waitForTimeout(3000);

  // Dismiss any dialogs (Restore pages, cookie banners)
  await page.evaluate(() => {
    // Close any open popups/modals by pressing Escape
    document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  });
  await page.waitForTimeout(800);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(800);
  await ss(page, 'p0_feed');

  if (page.url().includes('/login') || page.url().includes('/uas/')) {
    console.error('[POST] ERROR: Not logged in. Please log in first.'); process.exit(1);
  }
  console.log('[POST] Logged in ✓');

  // 2. Click "Start a post" — use Playwright locators (reliable)
  console.log('[POST] Clicking "Start a post"...');

  // Try multiple strategies
  let modalOpened = false;

  // Strategy A: click the share-box trigger button by class
  try {
    await page.locator('.share-box-feed-entry__trigger').first().click({ timeout: 5000 });
    modalOpened = true;
    console.log('[POST]   via .share-box-feed-entry__trigger');
  } catch {}

  // Strategy B: click by exact text
  if (!modalOpened) {
    try {
      await page.getByText('Start a post', { exact: true }).first().click({ timeout: 5000 });
      modalOpened = true;
      console.log('[POST]   via text "Start a post"');
    } catch {}
  }

  // Strategy C: click the placeholder input area
  if (!modalOpened) {
    try {
      await page.locator('[placeholder*="post"], [placeholder*="Post"]').first().click({ timeout: 5000 });
      modalOpened = true;
      console.log('[POST]   via placeholder');
    } catch {}
  }

  if (!modalOpened) { await ss(page, 'p1_error'); throw new Error('Could not open post modal'); }

  // Wait for the post composer modal
  await page.waitForTimeout(3000);
  await ss(page, 'p1_modal');

  // 3. Fill text via clipboard paste (works for Urdu/any script)
  console.log('[POST] Pasting post text via clipboard...');

  // Click the contenteditable editor in the modal
  const editorLoc = page.locator('.ql-editor[contenteditable="true"], div[role="textbox"][contenteditable="true"], [contenteditable="true"]').first();

  try {
    await editorLoc.waitFor({ timeout: 8000 });
    await editorLoc.click({ timeout: 5000 });
    await page.waitForTimeout(500);

    // Write text via clipboard (works for all languages including Urdu)
    await page.evaluate(async (txt) => {
      try {
        await navigator.clipboard.writeText(txt);
      } catch {
        // Fallback: use a hidden textarea to set clipboard
        const ta = document.createElement('textarea');
        ta.value = txt;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
    }, POST_TEXT);

    await page.keyboard.press('Control+a');
    await page.waitForTimeout(200);
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(2500);
    console.log('[POST]   Text pasted via clipboard ✓');
  } catch (e) {
    console.log(`[POST]   Editor error: ${e.message}`);
    // Last resort: type directly (slow)
    await page.keyboard.type(POST_TEXT, { delay: 0 });
    await page.waitForTimeout(2000);
  }

  await ss(page, 'p2_text');

  // 4. Upload image (optional)
  if (IMAGE_PATH && fs.existsSync(IMAGE_PATH)) {
    console.log('[POST] Uploading image:', path.basename(IMAGE_PATH));

    // Click photo/media button using Playwright locators
    const photoBtns = [
      page.getByLabel(/photo/i).first(),
      page.getByLabel(/media/i).first(),
      page.getByLabel(/image/i).first(),
      page.locator('button[aria-label*="Photo"], button[aria-label*="photo"], button[aria-label*="Media"]').first(),
    ];

    let photoClicked = false;
    for (const btn of photoBtns) {
      try {
        await btn.click({ timeout: 3000 });
        photoClicked = true;
        console.log('[POST]   Photo button clicked ✓');
        break;
      } catch {}
    }

    if (!photoClicked) console.log('[POST]   WARNING: photo button not found');
    await page.waitForTimeout(2000);

    // Set file via file input
    const fileInput = page.locator('input[type="file"]').first();
    try {
      await fileInput.waitFor({ timeout: 5000 });
      await fileInput.setInputFiles(IMAGE_PATH);
      console.log('[POST]   Image set via file input ✓');
      await page.waitForTimeout(9000);
      await ss(page, 'p3_image');
    } catch {
      console.log('[POST]   WARNING: file input not found — skipping image');
    }

    // Click Next/Done if present
    for (const label of ['Next', 'Done']) {
      try {
        const btn = page.getByRole('button', { name: label, exact: true });
        await btn.click({ timeout: 3000 });
        console.log(`[POST]   "${label}" clicked ✓`);
        await page.waitForTimeout(3000);
        await ss(page, 'p4_after_next');
        break;
      } catch {}
    }
  }

  // 5. Click Post button
  console.log('[POST] Clicking Post button...');
  await page.waitForTimeout(1000);

  let posted = false;
  try {
    await page.getByRole('button', { name: 'Post', exact: true }).click({ timeout: 5000 });
    posted = true;
    console.log('[POST]   Post button clicked ✓');
  } catch {}

  if (!posted) {
    // Fallback: find button with text "Post"
    try {
      await page.locator('button:has-text("Post"):not(:has-text("repost")):not(:has-text("Repost"))').last().click({ timeout: 5000 });
      posted = true;
      console.log('[POST]   Post button clicked via fallback ✓');
    } catch {}
  }

  await page.waitForTimeout(9000);
  await ss(page, 'p5_posted');

  if (posted) {
    console.log('\n[POST] ✓ SUCCESS — post published! Check p5_posted.png');
  } else {
    console.log('\n[POST] ✗ Post button not found. Check p5_posted.png');
    process.exit(1);
  }

  await page.waitForTimeout(2000);
  await browser.close();

})().catch(err => {
  console.error('\n[POST] FATAL:', err.message);
  process.exit(1);
});
