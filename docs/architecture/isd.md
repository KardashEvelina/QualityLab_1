---
owner: DevOps Owner
status: published
review_date: 2027-02-19
---

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

## Knowledge Links

- [[sdd|SDD]]
- [[adr/ADR-0001-python-flask|ADR-0001 — Python + Flask]]
- [[adr/ADR-0002-in-memory-storage|ADR-0002 — In-Memory Storage]]
- [[../developer/local-environment|Local Development Environment]]

#architecture #ops

## 10. Експлуатаційна документація

### 10.1. Процедура розгортання версії

Поточний навчальний контур QualityLab_1 розгортається локально як Flask-застосунок.

Перед розгортанням необхідно перейти до каталогу проєкту:

cd ~/PycharmProjects/QualityLab_1

Активувати віртуальне середовище:

source .venv/bin/activate

Перевірити поточну Git-гілку:

git branch --show-current

Перевірити стан робочого дерева:

git status --short

Оновити локальну копію репозиторію:

git pull

Встановити або оновити залежності:

pip install -r requirements.txt

Запустити Flask API:

python3 app.py

Після запуску виконати health-перевірку:

curl -i http://127.0.0.1:5000/health

Очікуваний результат:

HTTP 200

{"status":"ok"}

Розгортання вважається успішним, якщо Flask API запускається без критичних помилок, порт 5000 доступний, а GET /health повертає HTTP 200.

### 10.2. Процедура оновлення версії

Перед оновленням необхідно:

1. Перевірити Git status.
2. Перевірити CHANGELOG.
3. Переконатися, що документація відповідає новій версії.
4. Виконати тести.
5. Перевірити OpenAPI-контракт, якщо змінився API.
6. Виконати strict-збірку документації.

Перевірка тестів:

pytest

Перевірка OpenAPI:

spectral lint docs/api/openapi.yaml

Перевірка документації:

mkdocs build --strict

Після успішних перевірок виконується оновлення робочої версії.

Якщо у майбутньому буде додано постійне сховище даних, міграції схеми повинні виконуватися перед запуском нової версії застосунку.

Порядок для версії з базою даних:

1. створити резервну копію;
2. зупинити застосунок;
3. виконати міграцію бази даних;
4. перевірити результат міграції;
5. запустити застосунок;
6. виконати health check;
7. у разі помилки виконати rollback.

Для поточної версії QualityLab_1 постійна база даних не використовується, тому окремі міграції схеми не виконуються.

### 10.3. Процедура відновлення після відмови

Відновлення виконується з урахуванням залежностей системи.

Для поточної версії порядок запуску:

1. перевірити локальне середовище Python;
2. перевірити доступність залежностей;
3. за потреби запустити зовнішній mock-сервіс;
4. запустити Flask API;
5. виконати GET /health;
6. виконати GET /api/system/info;
7. перевірити основний функціональний endpoint.

Якщо в майбутньому буде використано постійну базу даних, порядок відновлення має бути таким:

1. відновити та перевірити базу даних;
2. виконати перевірку доступності сховища;
3. запустити застосунок;
4. виконати health check;
5. відновити зовнішні інтеграції.

Це відповідає правилу: спочатку відновлюються залежності та сховища, після цього запускається застосунок.

### 10.4. RTO та RPO

RTO — максимально допустимий час від моменту відмови до відновлення працездатності системи.

Для QualityLab_1 встановлено цільове значення:

RTO = 10 хвилин.

Обґрунтування:

1 хвилина — виявлення проблеми;
до 4 хвилин — первинна діагностика;
до 3 хвилин — перезапуск сервісу;
до 2 хвилин — health check та функціональна перевірка.

Сумарно:

1 + 4 + 3 + 2 = 10 хвилин.

RPO — максимально допустимий обсяг втрати даних після відновлення.

Для вихідного коду, конфігурації та документації, що зберігаються у Git і відправлені на GitHub:

RPO = 0 хвилин для зафіксованих та запушених змін.

Для runtime-даних поточної версії QualityLab_1 гарантувати RPO неможливо, оскільки дані зберігаються in-memory та можуть бути втрачені після завершення процесу.

Це є відомим експлуатаційним обмеженням системи.

Для майбутньої production-версії з постійним сховищем встановлюється цільовий RPO не більше 15 хвилин.

## 11. Політика резервного копіювання

### 11.1. Обсяг резервного копіювання

До резервного копіювання входять:

- вихідний код;
- Markdown-документація;
- OpenAPI Specification;
- MkDocs configuration;
- CI/CD workflow;
- runbook-и;
- конфігураційні файли без секретів;
- Git history;
- release tags.

Runtime in-memory дані поточної версії не входять до гарантованого backup-контуру.

### 11.2. Розклад резервного копіювання

Основний механізм резервного копіювання — Git та віддалений GitHub repository.

Інкрементна копія створюється при кожному commit і push.

Додаткова повна резервна копія репозиторію повинна створюватися один раз на тиждень.

### 11.3. Типи копій

Використовуються:

- інкрементні копії — Git commits;
- повна копія — повний clone або archive репозиторію.

### 11.4. Retention

Git history зберігається без обмеження для актуального репозиторію.

Щотижневі архівні копії зберігаються не менше 30 днів.

Критичні release-версії додатково фіксуються Git tags.

### 11.5. Шифрування

Секрети не повинні зберігатися у відкритому вигляді в Git.

Файли резервних копій, що можуть містити службову інформацію, повинні зберігатися у захищеному сховищі.

Секретні значення передаються через environment variables або окреме secret storage.

### 11.6. Правило 3-2-1

Для QualityLab_1 застосовується правило 3-2-1:

3 копії:

1. локальна робоча копія репозиторію;
2. віддалена копія GitHub;
3. окремий архівний backup.

2 типи носіїв:

1. локальний SSD;
2. віддалене або хмарне сховище.

1 копія поза основним середовищем:

віддалений GitHub repository або окреме хмарне сховище.

Таким чином одна локальна відмова не повинна призвести до втрати всіх копій системи.

## 12. Restore Drill

Restore Drill — контрольоване тестове відновлення системи з резервної копії.

Процедура повинна виконуватися регулярно та після суттєвих змін backup-політики.

### Крок 1. Створити тимчасовий каталог

mkdir -p ~/QualityLab_1_restore_test

### Крок 2. Перейти до каталогу

cd ~/QualityLab_1_restore_test

### Крок 3. Відновити репозиторій із віддаленої копії

git clone https://github.com/KardashEvelina/QualityLab_1.git

### Крок 4. Перейти до репозиторію

cd QualityLab_1

### Крок 5. Створити virtual environment

python3 -m venv .venv

### Крок 6. Активувати середовище

source .venv/bin/activate

### Крок 7. Встановити залежності

pip install -r requirements.txt

### Крок 8. Запустити тести

pytest

### Крок 9. Запустити застосунок

python3 app.py

### Крок 10. Виконати health check

curl -i http://127.0.0.1:5000/health

Restore Drill вважається успішним, якщо:

- репозиторій відновлено;
- залежності встановлено;
- тести проходять;
- Flask API запускається;
- GET /health повертає HTTP 200;
- документація доступна;
- Git history та release tags збережені.

Результат кожного Restore Drill повинен бути задокументований із датою, результатом PASS / FAIL та виявленими проблемами.

Правило експлуатації:

резервна копія, відновлення з якої ніколи не перевірялося, не вважається перевіреною резервною копією.

STATUS: OPERATIONAL RECOVERY AND BACKUP POLICY DEFINED
