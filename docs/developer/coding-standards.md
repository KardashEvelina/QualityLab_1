---
owner: Developer Owner
status: published
review_date: 2027-02-19
---

# Coding Standards

## Python conventions

- використовувати зрозумілі назви функцій і змінних;
- функції та змінні оформлювати у snake_case;
- класи оформлювати у PascalCase;
- уникати дублювання логіки;
- не зберігати secrets безпосередньо у вихідному коді;
- нову поведінку покривати тестами;
- складні операції декомпозувати на окремі функції або сервіси;

## Quality checks

- pytest — автоматичні тести;
- Radon — Cyclomatic Complexity та Halstead metrics;
- SonarCloud — статичний аналіз якості;
- GitHub Actions — автоматизована перевірка.

## Documentation

Зміна API, архітектури, конфігурації або поведінки повинна супроводжуватися зміною відповідної документації.

STATUS: published
