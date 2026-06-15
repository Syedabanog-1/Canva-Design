const { chromium } = require('playwright');
const { spawn } = require('child_process');

const IMAGE_PATH = 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\fte_graphic.png';

const POST_TEXT = `میں نے پچھلے مہینے اپنا پہلا AI ملازم رکھا۔
$1,200/ماہ پر — 168 گھنٹے فی ہفتہ کام۔
میرا بہترین انسانی ملازم $5,000/ماہ لیتا ہے — اور صرف 40 گھنٹے دیتا ہے۔

یہ حساب تکلیف دہ ہے۔ Agent Factory کے یہ 10 نکات نے میری سوچ بدل دی:

1/ 168 گھنٹے بمقابلہ 40
Digital FTE کبھی نہیں سوتا، چھٹی نہیں لیتا، تھکتا نہیں۔ ہفتے میں 4.2 گنا زیادہ آؤٹ پٹ — بغیر اوور ٹائم کے۔

2/ $500–2K بمقابلہ $4K–8K+/ماہ
اپنا بہترین عمل ایک بار AI agent میں ڈھالیں۔ وہ بغیر رکے چلتا رہے گا۔

3/ سالانہ 9,000 گھنٹے بمقابلہ 2,000
ایک Digital FTE کا ایک سال = 4.5 انسانی سال کا کام۔ startup کی رفتار سے۔

4/ 99%+ consistency بمقابلہ 85–95%
انسانوں کے اچھے اور برے دن ہوتے ہیں۔ Digital FTE رات 3 بجے بھی وہی معیار دیتا ہے جو صبح 9 بجے۔

5/ 10-80-10 کا اصول
انسان: intent (10%) → AI: execute (80%) → انسان: verify (10%)۔
آپ replace نہیں ہوتے — promote ہوتے ہیں۔

6/ فوری cloning بمقابلہ مہینوں کی hiring
کوئی workflow کام کر رہا ہے؟ منٹوں میں 10 agents بنائیں — نہ کہ سہ ماہیوں میں۔

7/ Spec-Driven Development
ایک بار لکھیں، ہمیشہ کے لیے deploy کریں۔ آپ کی expertise ایک recipe بنتی ہے — جو آپ کے سوتے وقت چلتی ہے۔

8/ صفر overhead اخراجات
نہ benefits، نہ HR، نہ sick leave، نہ performance reviews۔ صرف outcomes۔

9/ SaaS سے Agent Era تک
Software نے seats بیچی۔ AI outcomes بیچتا ہے۔
کل کا business model آج آ چکا ہے۔

10/ پانچ Maturity Levels
Level 1: AI Awareness (10-20% فائدہ)۔
Level 5: AI-First Enterprise (10x productivity)۔
Digital FTEs وہ پل ہیں جو آپ کو اوپر لے جاتے ہیں۔

جو کمپنیاں levels 3-5 پہلے سمجھ لیں گی — وہ صرف تیز نہیں چلیں گی۔
وہ ایک مختلف category میں ہوں گی۔

آپ کی organization ابھی کس level پر ہے؟

Sir Anas کے ساتھ سیکھ رہی ہوں @GIAIC | Panaversity Agent Factory

#AgentFactory #DigitalFTE #AIEmployee #FutureOfWork #GIAIC #Panaversity #AIAgents #LearnInPublic #10x #AIFirst`;

async function waitForChrome(port, maxWait = 15000) {
  const http = require('http');
  const start = Date.now();
  while (Date.now() - start < maxWait) {
    try {
      await new Promise((resolve, reject) => {
        http.get(`http://localhost:${port}/json/version`, (res) => {
          let data = '';
          res.on('data', d => data += d);
          res.on('end', () => resolve(data));
        }).on('error', reject);
      });
      return true;
    } catch (e) {
      await new Promise(r => setTimeout(r, 500));
    }
  }
  return false;
}

(async () => {
  const PORT = 9222;
  const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const PROFILE = 'C:\\Users\\ThinK Pad\\AppData\\Local\\Google\\Chrome\\User Data';

  // Kill any existing Chrome first (needed to add --remote-debugging-port)
  console.log('Closing any existing Chrome instances...');
  try {
    spawn('taskkill', ['/F', '/IM', 'chrome.exe'], { stdio: 'ignore' });
  } catch (e) { /* ignore if not running */ }
  await new Promise(r => setTimeout(r, 2500));

  console.log('Launching Chrome with remote debugging on port', PORT);
  const chromeProc = spawn(CHROME, [
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${PROFILE}`,
    '--profile-directory=Default',
    '--start-maximized',
    '--no-first-run',
    '--no-default-browser-check',
    'https://www.linkedin.com/feed/'
  ], { detached: true, stdio: 'ignore' });
  chromeProc.unref();

  console.log('Waiting for Chrome to be ready...');
  const ready = await waitForChrome(PORT, 35000);
  if (!ready) throw new Error('Chrome did not start. Try running: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222');
  console.log('Chrome ready. Connecting via CDP...');

  const browser = await chromium.connectOverCDP(`http://localhost:${PORT}`);
  const contexts = browser.contexts();
  const context = contexts[0];
  const pages = context.pages();

  let page = pages.find(p => p.url().includes('linkedin')) || pages[0];
  if (!page) {
    page = await context.newPage();
    await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'load', timeout: 60000 });
  }

  await page.bringToFront();
  await page.waitForTimeout(3000);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(1000);

  const url = page.url();
  console.log('Current URL:', url);
  await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p0_start.png' });

  if (!url.includes('linkedin.com/feed')) {
    throw new Error('Not on LinkedIn feed. URL: ' + url);
  }

  console.log('Logged in! Proceeding to post...');

  // Find "Start a post" button
  const startCoords = await page.evaluate(() => {
    const sels = [
      'button.share-box-feed-entry__trigger',
      '.share-creation-state__trigger',
      'button[aria-label*="post"]',
      'button[aria-label*="Post"]'
    ];
    for (const sel of sels) {
      const el = document.querySelector(sel);
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    for (const el of document.querySelectorAll('button, [role="button"]')) {
      if (el.textContent.trim() === 'Start a post') {
        const r = el.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    return null;
  });

  console.log('Start post button:', startCoords);
  if (startCoords) {
    await page.mouse.click(startCoords.x, startCoords.y);
  } else {
    await page.mouse.click(620, 185);
  }
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p1_modal.png' });

  // Paste post content
  const editorCoords = await page.evaluate(() => {
    const sels = [
      '.ql-editor[contenteditable="true"]',
      'div[role="textbox"][contenteditable="true"]',
      '[contenteditable="true"]'
    ];
    for (const sel of sels) {
      const el = document.querySelector(sel);
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.width > 100) return { x: r.x + r.width / 2, y: r.y + 40 };
      }
    }
    return null;
  });

  console.log('Editor coords:', editorCoords);
  if (editorCoords) {
    await page.mouse.click(editorCoords.x, editorCoords.y);
    await page.waitForTimeout(500);
    await page.evaluate((text) => navigator.clipboard.writeText(text), POST_TEXT);
    await page.keyboard.press('Control+v');
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p2_text.png' });
  console.log('Post text pasted.');

  // Upload image
  const photoCoords = await page.evaluate(() => {
    const sels = [
      'button[aria-label*="Photo"]',
      'button[aria-label*="photo"]',
      'button[aria-label*="Image"]',
      'button[aria-label*="Media"]',
      'button[aria-label*="Add a photo"]',
    ];
    for (const sel of sels) {
      const el = document.querySelector(sel);
      if (el) {
        const r = el.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    // Fallback: search by icon label or data-control-name
    for (const el of document.querySelectorAll('[data-control-name*="photo"], [aria-label*="Photo"], [aria-label*="photo"]')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    }
    return null;
  });

  console.log('Photo button:', photoCoords);
  if (photoCoords) {
    await page.mouse.click(photoCoords.x, photoCoords.y);
    await page.waitForTimeout(2500);
    await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p3_photo_clicked.png' });
  }

  const fileInput = await page.$('input[type="file"]');
  if (fileInput) {
    await fileInput.setInputFiles(IMAGE_PATH);
    console.log('Image uploaded!');
    await page.waitForTimeout(6000);
    await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p4_image_loaded.png' });
  } else {
    console.log('WARNING: file input not found — image not attached');
  }

  // Click Done/Next if present
  const doneCoords = await page.evaluate(() => {
    for (const btn of document.querySelectorAll('button')) {
      const txt = btn.textContent.trim();
      if (txt === 'Done' || txt === 'Next') {
        const r = btn.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    return null;
  });
  if (doneCoords) {
    console.log('Clicking Done/Next...');
    await page.mouse.click(doneCoords.x, doneCoords.y);
    await page.waitForTimeout(2500);
    await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p5_after_next.png' });
  }

  // Click Post button
  const postCoords = await page.evaluate(() => {
    for (const btn of document.querySelectorAll('button')) {
      const txt = btn.textContent.trim();
      const lbl = btn.getAttribute('aria-label') || '';
      if (txt === 'Post' || lbl === 'Post') {
        const r = btn.getBoundingClientRect();
        if (r.width > 0) return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    return null;
  });

  console.log('Post button:', postCoords);
  if (postCoords) {
    await page.mouse.click(postCoords.x, postCoords.y);
    await page.waitForTimeout(7000);
    await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p6_posted.png' });
    console.log('\nSUCCESS! Post published! See p6_posted.png');
  } else {
    console.log('ERROR: Post button not found');
    await page.screenshot({ path: 'D:\\syeda Gulzar Bano\\Quarter5-Assignment\\Q5-Assignment\\p6_error.png' });
  }

  await page.waitForTimeout(4000);
  await browser.close();
})().catch(async (err) => {
  console.error('ERROR:', err.message);
  process.exit(1);
});
