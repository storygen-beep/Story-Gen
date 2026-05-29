const { chromium } = require('playwright');
const TARGET_URL = 'https://sgsits.mponline.gov.in/welcome/loginAplication';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 80 });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 45000 });

  const modalState = () => page.evaluate(() => {
    const m = document.querySelector('#loginmodal');
    const u = document.querySelector('#username');
    return { modalDisplay: m ? getComputedStyle(m).display : 'NO MODAL',
             usernameVisible: u ? (u.offsetParent !== null) : 'NO FIELD' };
  });

  console.log('BEFORE click:', JSON.stringify(await modalState()));

  // Click the visible "Login" button
  try {
    await page.click('button:has-text("Login")', { timeout: 4000 });
    await page.waitForTimeout(800);
  } catch (e) { console.log('login click:', e.message); }
  console.log('AFTER clicking Login button:', JSON.stringify(await modalState()));

  // Now force the modal open via Bootstrap (simulating what custom.js would do)
  await page.evaluate(() => { if (window.jQuery) jQuery('#loginmodal').modal('show'); });
  await page.waitForTimeout(800);
  console.log('AFTER forcing modal open (jQuery):', JSON.stringify(await modalState()));
  await page.screenshot({ path: '/tmp/sgsits-modal-forced.png', fullPage: false });
  console.log('Screenshot of revealed form: /tmp/sgsits-modal-forced.png');

  await browser.close();
})();
