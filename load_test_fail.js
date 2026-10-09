import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '5s', target: 20 },
        { duration: '10s', target: 20 },
        { duration: '5s', target: 0 },
    ],

    thresholds: {
        http_req_duration: ['p(95)<5'],
        http_req_failed: ['rate<0.01'],
    },

    summaryTrendStats: [
        'avg',
        'min',
        'med',
        'max',
        'p(90)',
        'p(95)',
        'p(99)',
    ],
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
