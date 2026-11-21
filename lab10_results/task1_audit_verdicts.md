# Task 1 — Documentation Audit Verdicts

## 1. Documentation Decay Audit

За результатами Git-аудиту всі наявні відстежувані документи були оновлені менше ніж 90 днів тому.

Відповідно до порогів лабораторної роботи:

- до 90 днів — документ вважається актуальним за віком;
- понад 90 днів — підозра на Documentation Decay;
- понад 180 днів — документ імовірно застарілий.

На момент аудиту документів старших за 90 днів не виявлено.

При цьому в репозиторії повністю відсутній README.md. Це є критичною прогалиною документації, оскільки новий розробник, QA, DevOps або бізнес-користувач не має єдиної стартової точки для розуміння системи.

## 2. Dead Documentation Audit

Частина артефактів лабораторних робіт є історичною документацією процесу.

Такі файли не повинні використовуватися як актуальне джерело архітектури або інструкція запуску системи.

Вони зберігаються як історичні докази виконаних аудитів, але повинні бути позначені як deprecated / archive.

## 3. Final Verdict Matrix

| Artifact | Diagnosis | Verdict | Engineering justification |
|---|---|---|---|
| README.md | Missing documentation | UPDATE | Створити єдину точку входу, quick start, опис системи та onboarding |
| .github/workflows/lab7-quality-metrics.yml | Current operational documentation | UPDATE | Підтримувати разом зі змінами CI/CD |
| requirements.txt | Current operational documentation | UPDATE | Підтримувати синхронно із залежностями проєкту |
| privacy_inventory.md | Current product documentation | UPDATE | Повинен відповідати фактичним даним та privacy controls |
| FINANCIAL_LEDGER.md | Historical process artifact | DEPRECATED | Зберегти як результат Lab 9, але не використовувати як поточну документацію системи |
| lab5_goodhart.md | Historical process artifact | DEPRECATED | Архівний результат попередньої лабораторної |
| lab5_gqm.md | Historical process artifact | DEPRECATED | Архівний результат попередньої лабораторної |
| lab6_cfg_baseline.md | Historical process artifact | DEPRECATED | Фіксує попередній baseline |
| lab6_cfg_extended.md | Historical process artifact | DEPRECATED | Фіксує історичний стан аналізу |
| lab8_results/god_object_baseline_metrics.txt | Historical generated evidence | DEPRECATED | Не є живою документацією архітектури |
| lab8_results/mood_sonar_support.txt | Historical generated evidence | DEPRECATED | Зберігається як доказ Lab 8 |
| lab8_results/pass_wmc.txt | Historical generated evidence | DEPRECATED | Зберігається як доказ PASS |
| lab9_results/FPA_UCP_WORKSHEET.md | Historical analysis artifact | DEPRECATED | Фіксує функціональну оцінку Lab 9 |
| lab9_results/SQALE_AUDIT_LEDGER.md | Historical analysis artifact | DEPRECATED | Фіксує SQALE-аудит на конкретний момент часу |
| lab9_results/task3_git_history.txt | Reproducible generated evidence | DEPRECATED | Дані можуть бути повторно отримані через git log |
| requirements_lab5.txt | Historical dependency snapshot | DEPRECATED | Не використовувати замість актуального requirements.txt |

## 4. Main Findings

1. README.md відсутній — критична прогалина для всіх цільових аудиторій.
2. За Last Updated Age жоден існуючий документ ще не перевищив поріг 90 днів.
3. Репозиторій містить багато історичних артефактів лабораторних робіт, які не слід сприймати як живу документацію продукту.
4. Актуальними живими артефактами залишаються CI/CD-конфігурація, requirements.txt та privacy_inventory.md.
5. Для усунення ризику Documentation Decay необхідно створити формальний архітектурний паспорт і запровадити правило «зміна коду = зміна документації».

STATUS: TASK 1 AUDIT COMPLETED
