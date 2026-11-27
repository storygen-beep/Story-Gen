#!/usr/bin/env node
/*
 * Screenshot a page at phone, tablet and desktop widths and measure the things the
 * conversion rules can be checked for mechanically. Prints one JSON report.
 *
 *   node check.cjs <index.html[#tab] | url> <out_dir>
 *
 * It measures; it does not judge. The skill decides what a number means.
 */
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const VIEWPORTS = [
  { name: 'phone', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

// Runs inside the page. Everything here is plain DOM reading.
function measure() {
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
  };
  const text = (document.querySelector('main') || document.body).innerText || '';
  const words = text.match(/[A-Za-z][A-Za-z'’-]*/g) || [];
  const sentences = text.split(/[.!?\n]+/).filter((s) => s.trim().split(/\s+/).length > 2);
  const syllables = (w) => {
    const m = w.toLowerCase().replace(/e\b/, '').match(/[aeiouy]+/g);
    return Math.max(1, m ? m.length : 1);
  };
  const syllableCount = words.reduce((n, w) => n + syllables(w), 0);
  // Flesch-Kincaid grade: the reading-level proxy behind the "write plainly" rule.
  const grade = words.length && sentences.length
    ? 0.39 * (words.length / sentences.length) + 11.8 * (syllableCount / words.length) - 15.59
    : null;

  const primary = [...document.querySelectorAll('[data-cta="primary"]')].filter(visible);
  const first = primary[0];
  const rect = first ? first.getBoundingClientRect() : null;
  const h1 = document.querySelector('h1');

  const smallTargets = [...document.querySelectorAll('a, button, input, select, textarea, [role="button"]')]
    .filter(visible)
    .filter((el) => {
      if (el.tagName === 'A' && getComputedStyle(el).display === 'inline') return false; // inline links are exempt (WCAG 2.5.8)
      const r = el.getBoundingClientRect();
      return r.width < 24 || r.height < 24;
    })
    .map((el) => (el.innerText || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 40));

  return {
    title: document.title,
    h1: h1 ? h1.innerText.trim() : null,
    h1Count: document.querySelectorAll('h1').length,
    wordCount: words.length,
    readingGrade: grade === null ? null : Math.round(grade * 10) / 10,
    primaryCtaCount: primary.length,
    primaryCtaLabels: [...new Set(primary.map((el) => el.innerText.trim()))],
    primaryCtaAboveFold: rect ? rect.top >= 0 && rect.bottom <= window.innerHeight : false,
    primaryCtaSize: rect ? { width: Math.round(rect.width), height: Math.round(rect.height) } : null,
    formFieldCount: [...document.querySelectorAll('form input:not([type=hidden]):not([type=submit]), form select, form textarea')].filter(visible).length,
    fieldsMissingAutocomplete: [...document.querySelectorAll('form input:not([type=hidden]):not([type=submit]):not([type=checkbox]):not([type=radio])')].filter((el) => !el.autocomplete).length,
    imagesMissingAlt: [...document.querySelectorAll('img:not([alt])')].length,
    targetsUnder24px: smallTargets,
    horizontalOverflowPx: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
    pageHeightPx: document.documentElement.scrollHeight,
    longestBodyLineChars: (() => {
      // Widest paragraph, as characters per line: the 50-75ch line-length rule.
      let worst = 0;
      for (const p of document.querySelectorAll('p')) {
        if (!visible(p) || p.innerText.length < 80) continue;
        const style = getComputedStyle(p);
        // "normal" line-height has no pixel value; 1.2 x font size is the browser's usual figure.
        const lineHeight = parseFloat(style.lineHeight) || parseFloat(style.fontSize) * 1.2;
        const lines = Math.max(1, Math.round(p.getBoundingClientRect().height / lineHeight));
        worst = Math.max(worst, Math.round(p.innerText.length / lines));
      }
      return worst;
    })(),
    fontsLoaded: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '')).filter((v, i, a) => a.indexOf(v) === i),
    fontsFailed: [...document.fonts].filter((f) => f.status === 'error').map((f) => f.family.replace(/"/g, '')).filter((v, i, a) => a.indexOf(v) === i),
  };
}

(async () => {
  const [target, outDir] = process.argv.slice(2);
  if (!target || !outDir) {
    console.error('usage: node check.cjs <index.html | url> <out_dir>');
    process.exit(2);
  }
  fs.mkdirSync(outDir, { recursive: true });
  // A "#name" suffix on a file path is kept, so one tab of the options page can be shown: index.html#b
  const [filePart, hash] = target.split('#');
  const url = /^https?:/.test(target) ? target : pathToFileURL(path.resolve(filePart)).href + (hash ? `#${hash}` : '');

  // The container reaches the web through a proxy; Chromium does not read the env vars itself.
  const proxyServer = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(proxyServer ? { proxy: { server: proxyServer } } : {});
  const report = { target: url, viewports: {}, consoleErrors: [], failedRequests: [] };

  for (const viewport of VIEWPORTS) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    let bytes = 0;
    page.on('console', (m) => m.type() === 'error' && report.consoleErrors.push(`${viewport.name}: ${m.text().slice(0, 200)}`));
    page.on('pageerror', (e) => report.consoleErrors.push(`${viewport.name}: ${String(e).slice(0, 200)}`));
    page.on('requestfailed', (r) => report.failedRequests.push(`${viewport.name}: ${r.url().slice(0, 120)}`));
    page.on('response', async (r) => { try { bytes += (await r.body()).length; } catch (_) { /* redirects have no body */ } });

    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch((e) => report.consoleErrors.push(`${viewport.name}: load ${e.message.slice(0, 120)}`));
    await page.evaluate(() => document.fonts.ready);
    const fold = path.join(outDir, `${viewport.name}-fold.png`);
    const full = path.join(outDir, `${viewport.name}-full.png`);
    await page.screenshot({ path: fold });
    await page.screenshot({ path: full, fullPage: true });
    report.viewports[viewport.name] = { ...(await page.evaluate(measure)), transferBytes: bytes, shots: { fold, full } };
    await context.close();
  }
  await browser.close();
  report.consoleErrors = [...new Set(report.consoleErrors)];
  report.failedRequests = [...new Set(report.failedRequests)];
  console.log(JSON.stringify(report, null, 2));
})();
