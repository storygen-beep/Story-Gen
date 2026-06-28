// nsfw_harvest.js — FAST HARVEST. Extracts thumbnails + video URLs from PornHub GIF
// search results in a single page load.
//
// Interface:
//   Input:  edit the QUERIES array below. HARD CAP: max 5 items per run.
//           Requires Tor running on 127.0.0.1:9050 and playwright installed at /tmp.
//   Output: /tmp/nsfw_previews/<name>/
//           - {i}_{gifId}.jpg  — thumbnail
//           - {i}_{gifId}.webm — video (downloaded in-line; URLs expire in ~4 hours)
//           - {i}_{gifId}.json — metadata { id, title, videoUrl, thumbnail }
//   Exit:   0 on successful harvest. Non-zero on FATAL error (see stderr).
//
// Run:  node <absolute-path-to>/nsfw_harvest.js
//
// This script ONLY harvests candidates. After running: VIEW each thumbnail with
// the Read tool, SCORE against references/scoring_rubric.md, and PICK the best
// above threshold. Then download the winning video (which is already saved here).
//
// Tor note: use socks5:// NOT socks5h:// — Playwright has a documented bug with
// socks5h that throws ERR_NO_SUPPORTED_PROXIES. Chromium's SOCKS5 client routes
// DNS through the proxy anyway.

const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const PREVIEW_DIR = '/tmp/nsfw_previews';

// PornHub's video CDN (el2.phncdn.com) returns 410 Gone to requests with no browser
// User-Agent → every .webm saves as 0 bytes. UA + Referer fixes it. The thumbnail CDN
// tolerates a missing UA, but we send the same headers there for parity/robustness.
const BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
const REFERER = 'https://www.pornhub.com/';

// ============ EDIT THIS FOR EACH BATCH ============
const QUERIES = [
  { name: 'cherry_video',         search: 'amateur+nude+promo+tease+selfie',     desc: 'Nude promo tease link in bio selfie' },
];
// ==================================================

async function harvestFromSearchPage(page, search) {
  await page.goto(
    `https://www.pornhub.com/gifs/search?search=${search}`,
    { waitUntil: 'domcontentloaded', timeout: 45000 }
  );

  // Dismiss age gate if present
  try {
    const btn = await page.$('button:has-text("I am 18 or older")');
    if (btn) { await btn.click(); await page.waitForTimeout(3000); }
  } catch (e) {}

  // Wait for video elements to populate (ads/tracking don't matter — we only
  // need DOM data from <video> tags)
  await page.waitForTimeout(8000);

  // Extract ALL data from search results in one shot:
  // GIF IDs + thumbnail URLs + video URLs from <video> data attributes.
  return await page.evaluate(() => {
    const data = [];
    const seen = new Set();
    const gifLinks = document.querySelectorAll('a[href*="/gif/"]');

    for (const a of gifLinks) {
      const m = a.href.match(/\/gif\/(\d+)/);
      if (!m || seen.has(m[1])) continue;
      seen.add(m[1]);

      const gifId = m[1];
      const title = (a.textContent || '').trim().substring(0, 80);
      const parent = a.closest('li, div');
      const video = parent ? parent.querySelector('video') : null;

      let thumbnail = null;
      let videoUrl = null;

      if (video) {
        thumbnail = video.getAttribute('data-poster') || video.poster || null;
        videoUrl = video.getAttribute('data-webm') || video.getAttribute('data-mp4') || null;
        if (thumbnail && thumbnail.startsWith('data:')) thumbnail = null;
      }

      if (thumbnail || videoUrl) {
        data.push({ gifId, title, thumbnail, videoUrl });
      }
      if (data.length >= 15) break;
    }
    return data;
  });
}

(async () => {
  // Hard cap: larger batches exhaust Tor circuits and produce stale video URLs
  // (PornHub signs URLs with short validfrom/validto, so late items in a big
  // batch often have expired links before you view the thumbnails).
  if (QUERIES.length > 5) {
    console.error(`FATAL: QUERIES has ${QUERIES.length} items; max is 5 per batch.`);
    console.error('Split into multiple runs of 5 or fewer.');
    process.exit(1);
  }
  if (QUERIES.length === 0) {
    console.error('FATAL: QUERIES is empty. Add 1-5 items to the array above.');
    process.exit(1);
  }

  fs.mkdirSync(PREVIEW_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    proxy: { server: 'socks5://127.0.0.1:9050' }
  });
  const page = await browser.newPage();

  for (const q of QUERIES) {
    console.log(`\n=== ${q.name}: "${q.desc}" ===`);
    const subdir = path.join(PREVIEW_DIR, q.name);
    // Clean only THIS item's subdir — preserve sibling items' data
    if (fs.existsSync(subdir)) fs.rmSync(subdir, { recursive: true });
    fs.mkdirSync(subdir, { recursive: true });

    const results = await harvestFromSearchPage(page, q.search);
    console.log(`Found ${results.length} candidates with thumbnails+video URLs`);

    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      if (!r.thumbnail) continue;

      const thumbPath = path.join(subdir, `${i}_${r.gifId}.jpg`);
      try {
        execSync(
          `curl -s --socks5-hostname 127.0.0.1:9050 -H "User-Agent: ${BROWSER_UA}" -H "Referer: ${REFERER}" -o "${thumbPath}" "${r.thumbnail}" --max-time 10`,
          { timeout: 15000 }
        );
        const size = fs.statSync(thumbPath).size;
        if (size < 500) { fs.unlinkSync(thumbPath); continue; }
      } catch (e) { continue; }

      fs.writeFileSync(
        path.join(subdir, `${i}_${r.gifId}.json`),
        JSON.stringify({ id: r.gifId, title: r.title, videoUrl: r.videoUrl || '', thumbnail: r.thumbnail })
      );

      // Download video immediately — signed URLs expire in ~4 hours
      if (r.videoUrl) {
        const videoPath = path.join(subdir, `${i}_${r.gifId}.webm`);
        try {
          execSync(
            `curl -s --socks5-hostname 127.0.0.1:9050 -H "User-Agent: ${BROWSER_UA}" -H "Referer: ${REFERER}" -o "${videoPath}" "${r.videoUrl}" --max-time 30`,
            { timeout: 35000 }
          );
          const vSize = fs.statSync(videoPath).size;
          if (vSize < 50000) {
            fs.unlinkSync(videoPath);
            console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ video ${vSize}B (<50KB), removed`);
          } else {
            console.log(`  [${i}] ${r.gifId} "${r.title}" — ✓ ${(vSize/1024).toFixed(0)}KB`);
          }
        } catch (e) {
          console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ video download failed`);
        }
      } else {
        console.log(`  [${i}] ${r.gifId} "${r.title}" — ✗ no video URL`);
      }
    }

    await page.waitForTimeout(1500);
  }

  await browser.close();
  console.log(`\n=== HARVEST COMPLETE ===`);
  console.log('NEXT STEP: View EVERY thumbnail with the Read tool.');
  console.log('Score each against references/scoring_rubric.md. Pick the highest above 60.');
  console.log('If none above 60, trigger CRITIQUE cycle with a new query variation.');
  console.log('DO NOT auto-pick. DO NOT skip evaluation.');
})().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
