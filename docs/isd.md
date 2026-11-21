# Infrastructure Specification Document (ISD)

## 1. Призначення документа

ISD описує середовище виконання, CI/CD, моніторинг, резервне копіювання та параметри відновлення системи QualityLab_1.

## 2. Поточна топологія розгортання

Поточна система є навчальним Python/Flask застосунком.

Основна топологія:
- локальний запуск на macOS;
- Flask Web API запускається як Python-процес;
- зовнішній тестовий HTTP-сервіс запускається окремим Python-процесом;
- CI виконується у GitHub Actions;
- CI runner: ubuntu-latest;
- CI container: python:3.12-slim;
- постійна база даних відсутня;
- дані застосунку зберігаються in-memory.

## 3. Середовища

### Development

Призначення: локальна розробка та ручне тестування.

Конфігурація:
- Python 3.12;
- Flask 3.1.3;
- pytest;
- requests;
- Radon;
- локальні Flask та mock HTTP services.

Запуск основного API:
python3 app.py

### Test

Призначення: автоматизована перевірка якості та тестів.

Середовище:
- GitHub Actions;
- ubuntu-latest;
- container python:3.12-slim;
- pytest для тестування;
- Radon 6.0.1 для метрик складності.

CI запускається при:
- push;
- pull_request.

### Production

Окреме production-середовище на поточному етапі не розгорнуте.

Для лабораторного проєкту production розглядається як цільове середовище. Перед реальним production deployment необхідно:
- використовувати production WSGI server;
- винести конфігурацію у environment variables;
- додати постійне сховище даних;
- налаштувати централізовані логи;
- додати automated deployment та rollback.

## 4. Environment Variables

У репозиторії присутній файл .env.example.

Приклад змінної:
- LAB_SECRET — демонстраційна конфігураційна змінна.

Секретні значення не повинні зберігатися у Git.
У документації та .env.example дозволені тільки назви змінних і безпечні placeholder values.

## 5. Сховища даних

Поточна версія не використовує постійну базу даних.

Дані зберігаються:
- у Python lists;
- у Python dictionaries;
- тільки протягом життя процесу.

Наслідок: після рестарту застосунку runtime state втрачається.

GitHub використовується як постійне сховище вихідного коду та документації.

## 6. CI/CD Pipeline

Workflow:
.github/workflows/lab7-quality-metrics.yml

Triggers:
- push;
- pull_request.

Основні стадії:
1. Checkout repository.
2. Install Radon 6.0.1.
3. Run repository complexity scan.
4. Generate Cyclomatic Complexity JSON.
5. Generate Halstead JSON.
6. Build combined quality-metrics.json.
7. Validate JSON report.
8. Upload build artifact.

Quality Gate:
- JSON-звіт повинен бути валідним;
- complexity metrics повинні успішно сформуватися;
- локальний pre-commit gate додатково контролює Cyclomatic Complexity.

Artifact retention:
- quality-metrics.json зберігається GitHub Actions протягом 30 днів.

## 7. SonarCloud

У проєкті присутня конфігурація sonar-project.properties.

Project key:
KardashEvelina_QualityLab_1

Organization:
kardashevelina

Python version:
3.12

SonarCloud використовується для статичного аналізу та аудиту якості коду.

## 8. Monitoring

Поточні механізми контролю:
- GET /health для health check Flask API;
- GitHub Actions job status;
- Radon quality metrics;
- SonarCloud static analysis;
- application logging;
- privacy-safe logging.

Health endpoint:
GET /health

Очікувана відповідь:
HTTP 200, status = ok.

## 9. Backup and Recovery

### Source Code and Documentation

Основне резервне копіювання забезпечується Git та віддаленим GitHub repository.

Цільові показники для вихідного коду та документації:
- RTO <= 30 хвилин;
- RPO = 0 для вже запушених комітів.

### CI Artifacts

Quality reports зберігаються в GitHub Actions протягом 30 днів.

Повторне створення можливе повторним запуском pipeline.

Цільовий RTO для CI artifacts:
- RTO <= 30 хвилин.

### Runtime Data

Runtime-дані зараз зберігаються тільки in-memory.

Тому гарантувати RPO для runtime state неможливо: після аварійного завершення процесу дані можуть бути втрачені.

Це зафіксовано як поточне архітектурне обмеження.

Ціль для майбутнього production:
- persistent storage;
- автоматичний backup;
- RTO <= 30 хвилин;
- RPO <= 15 хвилин.

## 10. Deployment Recovery Procedure

У разі збою локального середовища:
1. Клонувати GitHub repository.
2. Створити Python virtual environment.
3. Встановити requirements.txt.
4. Відновити environment variables.
5. Запустити tests.
6. Запустити Flask API.
7. Перевірити GET /health.

## 11. Зв’язок із SDD

Flask Web API, Task Service, Privacy Data Service, Consent Service та External Service Adapter описані у docs/sdd.md.

ISD визначає, де та в якому середовищі ці компоненти виконуються.

STATUS: ISD CREATED

## 12. System Information Endpoint

GET /api/system/info використовується для перевірки поточної версії сервісу та його активного стану.

Поточна API version: 2.0.
