import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,
  duration: '5s',
};

export default function () {
  const res = http.get('http://api:3000/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'body has status ok': (r) => typeof r.body === 'string' && r.body.includes('"status":"ok"'),
  });
}
