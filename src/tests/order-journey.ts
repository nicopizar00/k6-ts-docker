import http from 'k6/http';
import { check } from 'k6';
import { buildHtml, buildSummaryJson } from './support/report';

const BASE_URL = __ENV.TARGET_BASE_URL || 'http://gateway-api:3000';

export const options = {
  vus: 2,
  duration: '20s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const payload = JSON.stringify({ product_id: 'prod-001', quantity: 1 });
  const params = { headers: { 'Content-Type': 'application/json' } };

  const createRes = http.post(`${BASE_URL}/orders`, payload, params);
  const createOk = check(createRes, {
    'order created 201': (r) => r.status === 201,
    'order has numeric id': (r) => {
      try {
        return typeof (JSON.parse(r.body as string) as { id: unknown }).id === 'number';
      } catch (_e) {
        return false;
      }
    },
  });

  if (!createOk) return;

  const orderId = (JSON.parse(createRes.body as string) as { id: number }).id;

  const readRes = http.get(`${BASE_URL}/orders/${orderId}`, {
    tags: { name: `${BASE_URL}/orders/:id` },
  });
  check(readRes, {
    'order read 200': (r) => r.status === 200,
    'order id matches': (r) => {
      try {
        return (JSON.parse(r.body as string) as { id: number }).id === orderId;
      } catch (_e) {
        return false;
      }
    },
    'order product matches': (r) => {
      try {
        return (JSON.parse(r.body as string) as { product_id: string }).product_id === 'prod-001';
      } catch (_e) {
        return false;
      }
    },
  });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function handleSummary(data: any) {
  const meta = { title: 'Order Create-Read Journey', testType: 'journey', targetUrl: BASE_URL };
  const summary = buildSummaryJson(data, meta);
  const stateContext = {
    ...summary,
    pattern: 'POST /orders → GET /orders/:id',
    timestamp: new Date().toISOString(),
  };

  return {
    '/reports/order-journey-report.html': buildHtml(data, meta),
    '/reports/order-journey.json': JSON.stringify(summary, null, 2),
    '/reports/state/test-context.json': JSON.stringify(stateContext, null, 2),
  };
}
