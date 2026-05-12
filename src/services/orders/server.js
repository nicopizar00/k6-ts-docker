const http = require('http');
const { Pool } = require('pg');

const PORT = Number(process.env.PORT) || 3002;

const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'postgres',
  database: process.env.POSTGRES_DB || 'gateway',
  user: process.env.POSTGRES_USER || 'app',
  password: process.env.POSTGRES_PASSWORD || 'app',
  port: 5432,
});

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
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
      await pool.query('SELECT 1');
      res.writeHead(200);
      res.end(JSON.stringify({ status: 'ok', service: 'orders-api' }));
      return;
    }

    if (req.method === 'POST' && req.url === '/orders') {
      const body = await readBody(req);
      const { product_id, quantity = 1 } = body;
      if (!product_id) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'product_id required' }));
        return;
      }
      const result = await pool.query(
        'INSERT INTO orders (product_id, quantity) VALUES ($1, $2) RETURNING *',
        [product_id, Number(quantity)],
      );
      res.writeHead(201);
      res.end(JSON.stringify(result.rows[0]));
      return;
    }

    const match = req.url && req.url.match(/^\/orders\/(\d+)$/);
    if (req.method === 'GET' && match) {
      const result = await pool.query('SELECT * FROM orders WHERE id = $1', [match[1]]);
      if (result.rows.length === 0) {
        res.writeHead(404);
        res.end(JSON.stringify({ error: 'not found' }));
      } else {
        res.writeHead(200);
        res.end(JSON.stringify(result.rows[0]));
      }
      return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'not found' }));
  } catch (err) {
    console.error(err);
    res.writeHead(500);
    res.end(JSON.stringify({ error: 'internal server error' }));
  }
});

server.listen(PORT, () => console.log(`orders-api listening on ${PORT}`));
