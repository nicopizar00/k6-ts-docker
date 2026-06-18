import http from 'k6/http';
import { check } from 'k6';
import { buildHtml, buildSummaryJson } from './support/report';

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://gateway-api:3000';

export const options = {
  vus: 3,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.60'],
    http_req_duration: ['p(90)<2000'],
    checks: ['rate>0.20'],
  },
};

const productIds = ['prod-001', 'prod-002', 'prod-003'];

export default function () {
  const productId = productIds[Math.floor(Math.random() * productIds.length)];
  const res = http.get(`${BASE_URL}/catalog/${productId}`);
  check(res, {
    'status 200': (r) => r.status === 200,
    'product id matches': (r) => {
      try {
        return (JSON.parse(r.body as string) as { id: string }).id === productId;
      } catch (_e) {
        return false;
      }
    },
  });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function handleSummary(data: any) {
  const meta = { title: 'Catalog Read Performance Gate', testType: 'gate', targetUrl: `${BASE_URL}/catalog` };
  return {
    '/reports/catalog-gate-report.html': buildHtml(data, meta),
    '/reports/catalog-gate.json': JSON.stringify(buildSummaryJson(data, meta), null, 2),
  };
}
