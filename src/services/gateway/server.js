const http = require('http');

const PORT = Number(process.env.PORT) || 3000;
const CATALOG_URL = process.env.CATALOG_URL || 'http://catalog-api:3001';
const ORDERS_URL = process.env.ORDERS_URL || 'http://orders-api:3002';

function httpGet(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let body = '';
      res.on('data', (c) => { body += c; });
      res.on('end', () => resolve({ status: res.statusCode, body }));
    }).on('error', reject);
  });
}

function httpPost(url, payload) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(payload);
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
      },
    };
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (c) => { body += c; });
      res.on('end', () => resolve({ status: res.statusCode, body }));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (c) => { body += c; });
    req.on('end', () => {
      try { resolve(JSON.parse(body || '{}')); } catch (e) { reject(e); }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  res.setHeader('Content-Type', 'application/json');

  try {
    if (req.method === 'GET' && req.url === '/health') {
      const [catalog, orders] = await Promise.all([
        httpGet(`${CATALOG_URL}/health`),
        httpGet(`${ORDERS_URL}/health`),
      ]);
      const allOk = catalog.status === 200 && orders.status === 200;
      res.writeHead(allOk ? 200 : 503);
      res.end(JSON.stringify({
        status: allOk ? 'ok' : 'degraded',
        service: 'gateway-api',
        downstream: {
          catalog: catalog.status === 200 ? 'ok' : 'error',
          orders: orders.status === 200 ? 'ok' : 'error',
        },
      }));
      return;
    }

    if (req.method === 'GET' && req.url === '/catalog') {
      const result = await httpGet(`${CATALOG_URL}/products`);
      res.writeHead(result.status);
      res.end(result.body);
      return;
    }

    const catalogMatch = req.url && req.url.match(/^\/catalog\/([\w-]+)$/);
    if (req.method === 'GET' && catalogMatch) {
      const result = await httpGet(`${CATALOG_URL}/products/${catalogMatch[1]}`);
      res.writeHead(result.status);
      res.end(result.body);
      return;
    }

    if (req.method === 'POST' && req.url === '/orders') {
      const body = await readBody(req);
      const result = await httpPost(`${ORDERS_URL}/orders`, body);
      res.writeHead(result.status);
      res.end(result.body);
      return;
    }

    const ordersMatch = req.url && req.url.match(/^\/orders\/(\d+)$/);
    if (req.method === 'GET' && ordersMatch) {
      const result = await httpGet(`${ORDERS_URL}/orders/${ordersMatch[1]}`);
      res.writeHead(result.status);
      res.end(result.body);
      return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'not found' }));
  } catch (err) {
    console.error(err);
    res.writeHead(502);
    res.end(JSON.stringify({ error: 'bad gateway' }));
  }
});

server.listen(PORT, () => console.log(`gateway-api listening on ${PORT}`));
