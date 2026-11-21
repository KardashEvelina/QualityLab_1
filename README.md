# QualityLab_1

QualityLab_1 — навчальний Python-проєкт для дослідження якості, надійності, приватності, архітектури та супроводу програмних систем.

## Основні можливості

- Flask Web API;
- робота із задачами;
- privacy data export;
- anonymization;
- consent management;
- privacy-safe logging;
- external service retry/fallback;
- автоматизовані quality metrics;
- SonarCloud analysis;
- GitHub Actions CI.

## Технології

- Python 3.12
- Flask 3.1.3
- pytest
- requests
- Radon
- SonarCloud
- GitHub Actions

## Quick Start

### 1. Клонування репозиторію

git clone https://github.com/KardashEvelina/QualityLab_1.git
cd QualityLab_1

### 2. Створення virtual environment

python3 -m venv .venv
source .venv/bin/activate

### 3. Встановлення залежностей

pip install -r requirements.txt

### 4. Запуск Flask API

python3 app.py

### 5. Перевірка роботи

curl http://127.0.0.1:5000/health

Очікувана відповідь:

{"status":"ok"}

## Tests

Запуск тестів:

pytest -q

## Quality Checks

Перевірка Cyclomatic Complexity:

radon cc . -s

Проєкт також використовує SonarCloud та GitHub Actions.

## Основні API endpoints

- GET /health
- GET /tasks/summary
- GET /privacy/log-demo
- GET /api/users/{subject_id}/personal-data
- GET /api/users/{subject_id}/privacy-state
- POST /api/users/{subject_id}/anonymize
- POST /api/users/{user_id}/consents/{purpose}/grant
- POST /api/users/{user_id}/consents/{purpose}/revoke
- GET /api/users/{user_id}/consents/history
- POST /api/users/{user_id}/optional-action/{purpose}

## Documentation

- System Design Document: docs/sdd.md
- Infrastructure Specification: docs/isd.md
- Architecture Decision Records: docs/architecture/adr/
- Audience Coverage Matrix: docs/audience_coverage.md

## Architecture Limitations

- дані зберігаються in-memory;
- production deployment поки не налаштований;
- після перезапуску процесу runtime data втрачаються.

## Onboarding Path

Новому розробнику рекомендується:
1. Прочитати README.md.
2. Ознайомитися з docs/sdd.md.
3. Переглянути docs/isd.md.
4. Переглянути ADR у docs/architecture/adr/.
5. Запустити проєкт та тести локально.

STATUS: PROJECT DOCUMENTATION ENTRY POINT

### GET /api/system/info

Повертає службову інформацію про систему.

Приклад відповіді:
{"service":"QualityLab_1","api_version":"2.0","status":"active"}
