---
owner: Developer Owner
status: published
review_date: 2027-02-19
---

# Contributing

## Призначення

Цей документ описує правила внесення змін до проєкту QualityLab_1.

## Робочий процес

1. Створити окрему Git-гілку для зміни.
2. Внести зміни до коду.
3. Запустити локальні тести.
4. Якщо змінюється публічна поведінка — оновити документацію.
5. Створити commit з описовим повідомленням.
6. Перед merge переконатися, що CI/CD проходить успішно.

## Перевірки перед commit

- pytest;
- перевірка документації;
- перевірка змінених API-контрактів;
- перевірка відсутності секретів у репозиторії.

## Documentation Rule

Code change = documentation change.

STATUS: published

## Knowledge Links

- [[../architecture/sdd|System Design Document]]
- [[../architecture/isd|Infrastructure Specification]]
- [[../architecture/adr/ADR-0001-python-flask|ADR-0001]]

#architecture #api #ops
