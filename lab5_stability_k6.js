import http from 'k6/http';
import { check, sleep } from 'k6';

const p95Limit = Number(__ENV.P95_LIMIT_MS || '500');

export const options = {
  stages: [
    { duration: '5s', target: 5 },
    { duration: '10s', target: 5 },
    { duration: '5s', target: 0 },
  ],

  thresholds: {
    http_req_duration: [`p(95)<${p95Limit}`],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const response = http.get(
    'http://127.0.0.1:5000/tasks/summary'
  );

  check(response, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(0.1);
}