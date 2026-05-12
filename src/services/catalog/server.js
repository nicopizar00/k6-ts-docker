const http = require('http');

const PORT = Number(process.env.PORT) || 3001;

const products = [
  { id: 'prod-001', name: 'Widget A', price: 9.99, stock: 100 },
  { id: 'prod-002', name: 'Widget B', price: 19.99, stock: 50 },
  { id: 'prod-003', name: 'Gadget X', price: 49.99, stock: 25 },
];

const productMap = new Map(products.map((p) => [p.id, p]));

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({ status: 'ok', service: 'catalog-api' }));
    return;
  }

  if (req.method === 'GET' && req.url === '/products') {
    res.writeHead(200);
    res.end(JSON.stringify({ products }));
    return;
  }

  const match = req.url && req.url.match(/^\/products\/([\w-]+)$/);
  if (req.method === 'GET' && match) {
    const product = productMap.get(match[1]);
    if (product) {
      res.writeHead(200);
      res.end(JSON.stringify(product));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'not found' }));
    }
    return;
  }

  res.writeHead(404);
  res.end(JSON.stringify({ error: 'not found' }));
});

server.listen(PORT, () => console.log(`catalog-api listening on ${PORT}`));
