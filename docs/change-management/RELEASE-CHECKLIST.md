---
owner: Release Manager
status: published
review_date: 2027-02-19
---

# Release Checklist — Go / No-Go

## 1. Призначення

Чек-лист використовується перед deployment нової версії QualityLab_1.

Реліз дозволяється лише тоді, коли всі критичні критерії мають статус PASS.

## 2. Go / No-Go Checklist

| Критерій | Статус |
|---|---|
| RFC погоджено CCB | PASS |
| Regression tests зелені | PASS |
| Migration перевірена | PASS |
| Backup створено | PASS |
| Rollback plan готовий | PASS |
| Health check визначено | PASS |
| Документація оновлена | PASS |
| CHANGELOG оновлено | PASS |
| OpenAPI contract перевірено | PASS |
| Monitoring налаштовано | PASS |
| Alerts пов’язані з runbook | PASS |
| Runbook відкату доступний | PASS |
| Комунікація релізу підготовлена | PASS |
| Error Budget не вичерпаний | PASS |

## 3. Go Criteria

Рішення GO приймається, якщо:

- всі критичні тести зелені;
- migration перевірена;
- backup доступний;
- rollback можливий;
- документація актуальна;
- health endpoint готовий до перевірки;
- Error Budget дозволяє deployment.

## 4. No-Go Criteria

Рішення NO-GO приймається, якщо:

- є failing tests;
- migration не перевірена;
- backup відсутній;
- rollback неможливий;
- документація не оновлена;
- OpenAPI має breaking changes без migration guide;
- Error Budget вичерпаний.

## 5. Перевірка після deployment

Після запуску версії виконати:

curl -i http://127.0.0.1:5000/health

Очікується:

HTTP 200

{"status":"ok"}

Додатково перевірити:

curl -i http://127.0.0.1:5000/api/system/info

## 6. Ланцюг простежуваності релізу

Вимога

↓

RFC-001

↓

CCB-001

↓

Git commits

↓

Automated tests

↓

CHANGELOG

↓

Git tag

↓

Build artifact

↓

Deployment

↓

Health check

## 7. Definition of Done

Реліз вважається завершеним лише якщо:

- код реалізовано;
- тести пройдено;
- документація синхронізована;
- CHANGELOG оновлено;
- monitoring та alerts актуальні;
- health check успішний;
- Git tag створено;
- результат deployment зафіксовано.

Фінальне рішення:

GO

STATUS: RELEASE READY