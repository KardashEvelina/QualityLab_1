---
owner: SRE Owner
status: documented
review_date: 2027-02-19
---

# Legacy Component — external_service.py

## 1. Компонент

Назва: external_service.py

Тип: інтеграційний / legacy-компонент.

Призначення: взаємодія QualityLab_1 із зовнішнім HTTP-сервісом та забезпечення retry/fallback поведінки при його недоступності.

Рівень довіри: verified.

## 2. Причина вибору

Компонент external_service.py був визначений під час аудиту документації ЛР10 як один із найбільш змінюваних компонентів проєкту та мав documentation gap.

Рівень довіри: verified.

## 3. Зовнішня залежність

Компонент звертається до:

http://127.0.0.1:5001/external/status

Тип взаємодії:

HTTP GET.

Параметр запиту:

mode.

Рівень довіри: verified.

## 4. Граф залежностей

Основний ланцюг:

Користувач / API client

↓

Flask app.py

↓

GET /tasks/summary

↓

get_external_status()

↓

external_service.py

↓

requests.get()

↓

External Service :5001

У випадку успіху:

External Service → HTTP response → ExternalStatus → /tasks/summary

У випадку помилки:

External Service unavailable → retry → fallback → degraded response → /tasks/summary

Рівень довіри: verified.

## 5. Конфігурація

Компонент використовує такі параметри:

EXTERNAL_SERVICE_URL = http://127.0.0.1:5001/external/status

MAX_ATTEMPTS = 3

REQUEST_TIMEOUT = 2 секунди

BACKOFF_SECONDS = 0.2 секунди

Рівень довіри: verified.

## 6. Модель даних

### ExternalRequest

Поля:

mode — режим зовнішнього запиту.

attempt — номер поточної спроби.

url — URL зовнішнього сервісу.

timeout — timeout HTTP-запиту.

max_attempts — максимальна кількість спроб.

Компонент реалізований як immutable Value Object.

Рівень довіри: verified.

### ExternalStatus

Поля:

status — статус зовнішнього сервісу.

source — джерело відповіді.

attempts — кількість виконаних спроб.

degraded — ознака деградованого режиму.

Рівень довіри: verified.

## 7. Ключові функції

### get_external_status(mode="normal")

Головна функція компонента.

Виконує до трьох спроб отримати відповідь зовнішнього сервісу.

Якщо запит успішний — повертає результат зовнішнього сервісу.

Якщо всі спроби завершилися помилкою — повертає fallback response.

Рівень довіри: verified.

### _request_external_status()

Виконує один HTTP-запит до зовнішнього сервісу.

Обробляє requests.RequestException.

У разі помилки повертає None.

Рівень довіри: verified.

### _wait_before_retry()

Реалізує затримку між повторними спробами.

Затримка залежить від номера спроби.

Рівень довіри: verified.

### _fallback_response()

Формує відповідь degraded mode, якщо зовнішній сервіс недоступний.

Очікувана fallback-відповідь містить:

status = degraded

source = fallback

attempts = 3

degraded = true

Рівень довіри: verified.

## 8. Поведінка при відмові

Якщо зовнішній сервіс на порту 5001 недоступний:

1. HTTP-запит завершується помилкою.
2. Компонент фіксує warning у логах.
3. Виконується повторна спроба.
4. Максимальна кількість спроб — 3.
5. Після невдалих спроб використовується fallback.
6. Система переходить у degraded mode замість повної відмови.

Рівень довіри: verified.

## 9. Відомі тести

Для компонента існують resilience tests.

Перевіряються:

- успішна відповідь зовнішнього сервісу;
- повторні спроби;
- fallback після трьох невдалих спроб;
- кількість retry;
- immutable поведінка ExternalRequest;
- immutable поведінка ExternalStatus.

Рівень довіри: verified.

## 10. Реєстр технічного боргу

| ID | Тип боргу | Проблема | Наслідок | Рівень |
|---|---|---|---|---|
| TD-01 | Architecture debt | Жорстко заданий URL зовнішнього сервісу | Складніше змінювати середовище deployment | Medium |
| TD-02 | Code debt | Retry та fallback знаходяться в одному integration module | Подальше розширення може збільшити відповідальність модуля | Medium |
| TD-03 | Test debt | Частина mutation-тестів для external_service виживала | Можливі неперевірені граничні сценарії | High |
| TD-04 | Documentation debt | До ЛР12 компонент не мав окремої документації | Черговому спеціалісту складно швидко зрозуміти залежності | High |
| TD-05 | Operations debt | Немає окремого автоматичного алерту саме на недоступність :5001 | Збій може бути виявлений із затримкою | Medium |

## 11. Відомі ризики

### RISK-01

Недоступність зовнішнього сервісу.

Наслідок:

система переходить у degraded mode.

Рівень: High.

Рівень довіри: verified.

### RISK-02

Збільшення latency через повторні спроби.

Наслідок:

користувач може отримати повільнішу відповідь.

Рівень: Medium.

Рівень довіри: verified.

### RISK-03

Зміна контракту зовнішнього сервісу.

Наслідок:

ExternalStatus може не змогти коректно побудувати результат.

Рівень: High.

Рівень довіри: assumed.

## 12. Підсумок

external_service.py є критичним інтеграційним компонентом QualityLab_1.

Він забезпечує взаємодію із зовнішнім сервісом, retry-механізм та fallback-поведінку.

Основним операційним ризиком є недоступність зовнішньої залежності.

STATUS: LEGACY COMPONENT DOCUMENTED