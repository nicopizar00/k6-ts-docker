import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';
import { buildHtml, buildSummaryJson } from './support/report';

const TARGET_BASE_URL = __ENV.TARGET_BASE_URL;
if (!TARGET_BASE_URL) {
  throw new Error(
    'TARGET_BASE_URL is required for bff-checkout-journey; set it to a Docker-host-accessible target such as http://host.docker.internal:8080'
  );
}

const BASE_URL = TARGET_BASE_URL;

export const options = {
  vus: 1,
  duration: '60s',
  thresholds: {
    http_req_failed: ['rate<0.60'],
    http_req_duration: ['p(90)<2000'],
    checks: ['rate>0.20'],
  },
};

const productIds = new SharedArray('productIds', () => ['prod-001', 'prod-002', 'prod-003']);
const managementActions = new SharedArray('orderManagementActions', () => ['mark_prepared']);

export default function () {
  const params = { headers: { 'Content-Type': 'application/json' } };
  const productId = productIds[Math.floor(Math.random() * productIds.length)];
  const cartPayload = JSON.stringify({ product_id: productId, quantity: 1 });
  const checkoutPayload = JSON.stringify({ payment_method: 'card' });
  const managePayload = JSON.stringify({ action: managementActions[0] });

  const catalogRes = http.get(`${BASE_URL}/catalog/products`);
  check(catalogRes, {
    'catalog products status 200': (r) => r.status === 200,
    'catalog products body array': (r) => {
      try {
        const body = JSON.parse(r.body as string);
        return Array.isArray(body);
      } catch (_e) {
        return false;
      }
    },
  });

  const addRes = http.post(`${BASE_URL}/cart/items`, cartPayload, params);
  check(addRes, {
    'add cart item succeeded': (r) => r.status === 200 || r.status === 201,
    'cart item added body has product id': (r) => {
      try {
        const body = JSON.parse(r.body as string);
        return body?.product_id === productId;
      } catch (_e) {
        return false;
      }
    },
  });

  const cartRes = http.get(`${BASE_URL}/cart`);
  check(cartRes, {
    'cart status 200': (r) => r.status === 200,
    'cart contains items': (r) => {
      try {
        const body = JSON.parse(r.body as string);
        return Array.isArray(body?.items) && body.items.length > 0;
      } catch (_e) {
        return false;
      }
    },
  });

  const checkoutRes = http.post(`${BASE_URL}/checkout`, checkoutPayload, params);
  const checkoutOk = check(checkoutRes, {
    'checkout succeeded': (r) => r.status === 200 || r.status === 201,
    'checkout returns order id': (r) => {
      try {
        const body = JSON.parse(r.body as string);
        return typeof body?.orderId === 'string' || typeof body?.orderId === 'number';
      } catch (_e) {
        return false;
      }
    },
  });

  if (!checkoutOk) {
    return;
  }

  const orderId = (() => {
    try {
      const body = JSON.parse(checkoutRes.body as string);
      return typeof body.orderId === 'number' || typeof body.orderId === 'string' ? body.orderId : null;
    } catch (_e) {
      return null;
    }
  })();

  if (orderId === null) {
    return;
  }

  const orderRes = http.get(`${BASE_URL}/orders/${orderId}`);
  check(orderRes, {
    'order read status 200': (r) => r.status === 200,
    'order id matches': (r) => {
      try {
        const body = JSON.parse(r.body as string);
        return body?.id === orderId;
      } catch (_e) {
        return false;
      }
    },
  });

  const manageRes = http.post(`${BASE_URL}/orders/${orderId}/manage`, managePayload, params);
  check(manageRes, {
    'order manage succeeded': (r) => r.status === 200 || r.status === 204,
  });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function handleSummary(data: any) {
  const meta = { title: 'BFF Checkout Journey', testType: 'journey', targetUrl: BASE_URL };
  const summary = buildSummaryJson(data, meta);
  const stateContext = {
    ...summary,
    pattern: 'GET /catalog/products → POST /cart/items → POST /checkout → GET /orders/:id → POST /orders/:id/manage',
    timestamp: new Date().toISOString(),
  };

  return {
    '/reports/bff-checkout-journey-report.html': buildHtml(data, meta),
    '/reports/bff-checkout-journey.json': JSON.stringify(summary, null, 2),
    '/reports/state/test-context.json': JSON.stringify(stateContext, null, 2),
  };
}
