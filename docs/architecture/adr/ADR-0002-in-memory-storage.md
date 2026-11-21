---
owner: System Architect
status: published
review_date: 2027-05-20
---

# ADR-002: Використання In-Memory Storage у навчальному контурі

## Status

Accepted

## Context

Поточна версія QualityLab_1 використовується для лабораторних експериментів і не потребує довготривалого зберігання production-даних.

TaskService, PrivacyDataService та інші компоненти зберігають дані у Python lists та dictionaries.

## Alternatives Considered

### In-Memory Storage
- не потребує окремої бази даних;
- швидкий запуск;
- мінімальна конфігурація;
- зручно для контрольованих тестових сценаріїв.

### SQLite
- забезпечує persistence;
- проста локальна база;
- додає шар роботи з БД та міграціями.

### PostgreSQL
- придатний для production;
- забезпечує транзакції та масштабування;
- потребує окремої інфраструктури та конфігурації.

## Decision

Для поточного навчального контуру використовувати in-memory storage.

Для реального production deployment рішення повинно бути переглянуте на користь persistent database.

## Consequences

Позитивні наслідки:
- простота системи;
- швидкий запуск тестів;
- відсутність зовнішньої database dependency.

Негативні наслідки:
- дані втрачаються після завершення процесу;
- неможливо гарантувати RPO для runtime state;
- рішення не підходить для production.

## Future Decision Trigger

Перехід на persistent storage необхідний, якщо система почне зберігати реальні користувацькі дані або буде розгорнута як production service.

## Related Documents

- docs/sdd.md
- docs/isd.md

STATUS: ADR ACCEPTED

## Knowledge Links

- [[../sdd|SDD]]
- [[../isd|ISD]]
- [[../../developer/CONTRIBUTING|Contributing]]

#architecture #ops
