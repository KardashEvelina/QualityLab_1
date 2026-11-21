---
owner: System Architect
status: published
review_date: 2027-05-20
---

# ADR-001: Використання Python та Flask для Web API

## Status

Accepted

## Context

QualityLab_1 є навчальним проєктом для лабораторного дослідження якості, надійності, приватності та супроводу програмних систем.

Для проєкту потрібен простий HTTP API, який легко запускати локально, тестувати через pytest та інтегрувати з інструментами аналізу якості.

## Alternatives Considered

### Python + Flask
- мінімальна конфігурація;
- простий REST API;
- легка інтеграція з pytest;
- підтримка Radon, pip-audit та інших Python quality tools.

### Python + Django
- більше вбудованих можливостей;
- складніша структура для невеликого навчального проєкту;
- надлишкова функціональність для поточного обсягу системи.

### Node.js + Express
- підходить для REST API;
- потребує переходу на інший технологічний стек;
- не сумісний з уже створеним Python-кодом лабораторних робіт.

## Decision

Використовувати Python 3.12 та Flask як основний стек Web API.

## Consequences

Позитивні наслідки:
- швидкий локальний запуск;
- просте тестування;
- сумісність із поточним кодом;
- інтеграція з GitHub Actions, Radon та SonarCloud.

Негативні наслідки:
- Flask не надає production infrastructure з коробки;
- для production потрібен окремий WSGI server;
- частину архітектурних механізмів потрібно реалізовувати вручну.

## Related Documents

- docs/sdd.md
- docs/isd.md

STATUS: ADR ACCEPTED

## Knowledge Links

- [[../sdd|SDD]]
- [[../isd|ISD]]
- [[../../developer/coding-standards|Coding Standards]]

#architecture
