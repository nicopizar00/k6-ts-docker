// Minimal Browser test template — illustrative only and CURRENTLY DEFERRED.
//
// The reference k6 image (grafana/k6:0.55.0) does not ship Chromium. The
// MVP placeholder lives at src/tests/browser-smoke.ts.example and is NOT
// built into dist/. Do not add a Browser test to the esbuild entry list
// without a Plan that accepts the image-size / build-time / CI-cost trade.
//
// Boundary reminder: even Browser tests do NOT own orchestration. They
// drive a page; they do not bring up containers or write outside /reports/.

// import { browser } from 'k6/browser';   // commented: do not use in built tests
// import { check } from 'k6';

/*
// Sample shape — DO NOT enable in production tests today.

export const options = {
  scenarios: {
    ui: {
      executor: 'shared-iterations',
      vus: 1,
      iterations: 1,
      options: {
        browser: { type: 'chromium' },
      },
    },
  },
  thresholds: {
    browser_web_vital_lcp: ['p(95)<2500'],   // ms
    browser_web_vital_cls: ['p(95)<0.1'],    // unitless
    checks: ['rate>0.99'],
  },
};

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://gateway-api:3000';

export default async function () {
  const page = await browser.newPage();
  try {
    await page.goto(BASE_URL);
    const headingPresent = await page.locator('h1').isVisible();
    check(null, { 'heading visible': () => headingPresent });
  } finally {
    await page.close();
  }
}

export function handleSummary(data) {
  return {
    'stdout': '\n',
    '/reports/browser-example.json': JSON.stringify(data),
    // '/reports/browser-example.html': buildHtmlReport(data),
  };
}
*/

export {};   // keep this file as a valid empty module so the placeholder lints clean
