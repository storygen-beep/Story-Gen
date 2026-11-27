#!/usr/bin/env node
/*
 * Redesign mode: read what an existing website SAYS, and nothing about how it LOOKS.
 *
 *   node extract.cjs <url> [max_pages=6]
 *
 * Prints JSON with the words on the site: headings, body text, button labels, form
 * fields, prices, proof, contact details, structured data. It deliberately collects
 * no colours, fonts, CSS, layout, element positions or screenshots, and it reports
 * headings, text and button labels as separate flat lists rather than as sections —
 * so the old design cannot leak into the new one through this script.
 */
const { chromium } = require('playwright');

// Pages that usually hold answers the brief needs. Matched against link text and path.
const USEFUL_PAGE = /pric|plan|about|story|feature|product|service|how-it-works|faq|contact|review|testimonial|customer|case-stud/i;

// Runs inside the page. Reads text only.
function readWords() {
  const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const seen = new Set();
  const unique = (list) => list.filter((t) => t && !seen.has(t) && seen.add(t));
  const shown = (el) => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const meta = (name) => {
    const el = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
    return el ? clean(el.content) : '';
  };

  const headings = [...document.querySelectorAll('h1, h2, h3')].filter(shown)
    .map((h) => ({ level: Number(h.tagName[1]), text: clean(h.innerText) })).filter((h) => h.text).slice(0, 60);

  const text = unique([...document.querySelectorAll('p, li, blockquote, figcaption, dd, summary')].filter(shown)
    .map((el) => clean(el.innerText)).filter((t) => t.length >= 25 && t.length <= 700)).slice(0, 120);

  const actions = [...document.querySelectorAll('a, button, [role="button"], input[type="submit"]')].filter(shown)
    .map((el) => ({ label: clean(el.innerText || el.value || el.getAttribute('aria-label')), href: el.tagName === 'A' ? el.getAttribute('href') || '' : '' }))
    .filter((a) => a.label && a.label.length <= 40);
  const labelCounts = {};
  for (const a of actions) labelCounts[a.label] = (labelCounts[a.label] || 0) + 1;

  const forms = [...document.querySelectorAll('form')].map((form) => ({
    submitLabel: clean((form.querySelector('button, input[type="submit"]') || {}).innerText || (form.querySelector('input[type="submit"]') || {}).value || ''),
    fields: [...form.querySelectorAll('input:not([type=hidden]):not([type=submit]), select, textarea')].map((f) => ({
      label: clean((f.labels && f.labels[0] && f.labels[0].innerText) || f.getAttribute('aria-label') || f.placeholder || f.name),
      type: f.type || f.tagName.toLowerCase(),
      required: f.required,
    })),
  })).filter((f) => f.fields.length);

  const body = clean(document.body.innerText);
  const prices = unique((body.match(/.{0,60}(?:[$€£₹]\s?\d[\d,.]*|\d[\d,.]*\s?(?:USD|EUR|GBP|INR))(?:\s?\/\s?\w+|\s+per\s+\w+)?.{0,40}/g) || []).map(clean)).slice(0, 25);
  const emails = unique(body.match(/[\w.+-]+@[\w-]+\.[\w.-]+/g) || []).slice(0, 5);
  const phones = unique((body.match(/\+?\d[\d\s().-]{8,16}\d/g) || []).map(clean)).slice(0, 5);

  const structuredData = [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => {
    try { return JSON.parse(s.textContent); } catch (_) { return null; }
  }).filter(Boolean).slice(0, 6);

  // Alt text says what pictures the site uses (product shots, team, logos). The files
  // themselves are not fetched; the user supplies images for the new design.
  const imageDescriptions = unique([...document.querySelectorAll('img[alt]')].filter(shown).map((i) => clean(i.alt)).filter((t) => t.length > 3)).slice(0, 40);

  const links = [...document.querySelectorAll('a[href]')].map((a) => ({ label: clean(a.innerText), href: a.href }));

  return {
    title: clean(document.title),
    metaDescription: meta('description') || meta('og:description'),
    siteName: meta('og:site_name'),
    language: document.documentElement.lang || '',
    headings, text,
    actionLabels: Object.entries(labelCounts).sort((a, b) => b[1] - a[1]).slice(0, 40).map(([label, count]) => ({ label, count })),
    forms, prices, contact: { emails, phones }, structuredData, imageDescriptions,
    links,
  };
}

(async () => {
  const start = process.argv[2];
  const maxPages = Number(process.argv[3] || 6);
  if (!start) {
    console.error('usage: node extract.cjs <url> [max_pages]');
    process.exit(2);
  }
  const origin = new URL(start).origin;
  const proxyServer = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(proxyServer ? { proxy: { server: proxyServer } } : {});
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const report = { source: start, extractedAt: new Date().toISOString(), pages: [], errors: [] };

  const queue = [start];
  const visited = new Set();
  while (queue.length && report.pages.length < maxPages) {
    const url = queue.shift();
    const key = url.replace(/[#?].*$/, '').replace(/\/$/, '');
    if (visited.has(key)) continue;
    visited.add(key);
    const page = await context.newPage();
    try {
      const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      if (!response || response.status() >= 400) throw new Error(`HTTP ${response ? response.status() : 'no response'}`);
      await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {}); // busy sites never go idle
      const words = await page.evaluate(readWords);
      const { links, ...content } = words;
      report.pages.push({ url, ...content });
      if (report.pages.length === 1) {
        const candidates = links
          .filter((l) => l.href.startsWith(origin) && USEFUL_PAGE.test(`${l.label} ${new URL(l.href).pathname}`))
          .map((l) => l.href.replace(/[#?].*$/, ''));
        queue.push(...new Set(candidates));
      }
    } catch (error) {
      report.errors.push(`${url}: ${String(error.message).slice(0, 160)}`);
    }
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(report, null, 2));
  if (!report.pages.length) process.exit(1);
})();
