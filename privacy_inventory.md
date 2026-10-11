# PII Inventory

| Категорія | Поля | Джерело / сховище | Експорт | Логи |
|---|---|---|---|---|
| Прямі ідентифікатори | id, name | users | Так | ID лише у безпечному вигляді |
| Контактні дані | email, phone | users | Так | Маскувати |
| Налаштування профілю | language, theme | user_settings | Так | Не логувати повністю |
| Історія дій | action, timestamp | user_activity | Так | Без відкритих PII |
| Дані про згоду | purpose, status, policy_version, granted_at, withdrawn_at, source | user_consents | Так | Без відкритих PII |
| Security-sensitive | password_hash, reset_token, internal_security_flag | users | Ні | Повністю REDACTED |

## Поля, заборонені для Personal Data Export

- password_hash
- reset_token
- internal_security_flag
- access_token
- refresh_token
- api_key
- session_secret

## Політика логування

- email: часткове маскування
- phone: часткове маскування
- password/token/api_key/session_secret: [REDACTED]
- correlation_id та тип операції: дозволено
