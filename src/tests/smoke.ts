import http from 'k6/http';
import { check } from 'k6';
import { buildHtml, buildSummaryJson } from './support/report';

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://gateway-api:3000';
const CATALOG_URL = __ENV.CATALOG_URL || 'http://catalog-api:3001';
const ORDERS_URL = __ENV.ORDERS_URL || 'http://orders-api:3002';

export const options = {
  vus: 1,
  duration: '10s',
};

export default function () {
  const gwRes = http.get(`${BASE_URL}/health`);
  check(gwRes, {
    'gateway status 200': (r) => r.status === 200,
    'gateway body ok': (r) => typeof r.body === 'string' && r.body.includes('"status":"ok"'),
  });

  const catRes = http.get(`${CATALOG_URL}/health`);
  check(catRes, {
    'catalog status 200': (r) => r.status === 200,
  });

  const ordRes = http.get(`${ORDERS_URL}/health`);
  check(ordRes, {
    'orders status 200': (r) => r.status === 200,
  });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function handleSummary(data: any) {
  const meta = { title: 'k6 Smoke Test', testType: 'smoke', targetUrl: BASE_URL };
  return {
    '/reports/smoke-report.html': buildHtml(data, meta),
    '/reports/smoke.json': JSON.stringify(buildSummaryJson(data, meta), null, 2),
  };
}
