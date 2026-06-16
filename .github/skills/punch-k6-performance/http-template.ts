// Minimal HTTP test template — illustrative only.
//
// Real, stronger examples live in src/tests/*.ts. This template is a
// structural hint for an agent starting a new test; do not import it,
// do not copy-paste verbatim, and do not let it overwrite the conventions
// already established in src/tests/smoke.ts, catalog-gate.ts, and
// order-journey.ts.
//
// Boundary reminder: k6 does NOT own orchestration. Tests must not start
// containers, poll state, shell out, or write outside /reports/.

import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

// Thresholds live at the top of the file — they are the gate.
export const options = {
  thresholds: {
    http_req_failed: ['rate<0.01'],          // < 1% errors
    http_req_duration: ['p(95)<500'],        // 95th percentile under 500ms
    checks: ['rate>0.99'],                   // > 99% check pass
  },
  // Pick ONE scenario shape per file; do not mix scenarios casually.
  vus: 5,
  duration: '30s',
};

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://gateway-api:3000';

// Shared fixtures via SharedArray — never re-read mid-iteration.
const productIds = new SharedArray('product-ids', () => [
  'prod-001',
  'prod-002',
  'prod-003',
]);

export default function () {
  const id = productIds[Math.floor(Math.random() * productIds.length)];
  const res = http.get(`${BASE_URL}/catalog/${id}`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body has id': (r) => typeof r.body === 'string' && r.body.includes(id),
  });

  sleep(1);
}

// handleSummary is mandatory. Real tests should import the shared HTML
// builder from src/tests/support/report.ts and emit both an HTML and a
// compact JSON summary under /reports/.
export function handleSummary(data: unknown) {
  return {
    'stdout': '\n', // keep terminal output quiet
    '/reports/example.json': JSON.stringify(data),
    // '/reports/example.html': buildHtmlReport(data),   // from support/report.ts
  };
}
