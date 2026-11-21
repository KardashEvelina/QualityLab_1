---
owner: Documentation Owner
status: published
review_date: 2027-02-19
---

# Handover Package

## 1. Мета

Цей пакет призначений для передачі системи QualityLab_1 новому розробнику або команді супроводу без необхідності отримувати критичні знання лише усно.

## 2. Реєстр документації

| Document | Owner | Status | Purpose |
|---|---|---|---|
| README.md | Project Owner | Current | Quick Start, призначення системи та onboarding |
| docs/sdd.md | System Architect | Current | Архітектура, компоненти, модель даних та API |
| docs/isd.md | DevOps Owner | Current | Середовища, CI/CD, monitoring, recovery |
| docs/architecture/adr/ADR-001-python-flask.md | System Architect | Accepted | Рішення щодо Python та Flask |
| docs/architecture/adr/ADR-002-in-memory-storage.md | System Architect | Accepted | Рішення щодо in-memory storage |
| docs/audience_coverage.md | Documentation Owner | Current | Покриття потреб Developer, QA, DevOps, Business |
| docs/maintenance.md | Documentation Owner | Current | Регламент підтримки документації |

## 3. Onboarding нового розробника

Новий розробник проходить такий шлях:

1. Прочитати README.md та зрозуміти призначення системи.
2. Клонувати репозиторій, створити .venv та встановити requirements.txt.
3. Запустити pytest і перевірити, що тести проходять.
4. Ознайомитися з docs/sdd.md, docs/isd.md та ADR.
5. Запустити Flask API і перевірити GET /health та GET /api/system/info.

## 4. Bus Factor Declaration

Bus Factor показує ризик втрати критичних знань, якщо ключова людина перестає бути доступною для проєкту.

Поточний Bus Factor для QualityLab_1 оцінено як 1, оскільки основні архітектурні, експлуатаційні та історичні знання створювалися одним власником проєкту.

## 5. Single Points of Knowledge

| Knowledge Area | Current Risk | Mitigation |
|---|---|---|
| Архітектура системи | High | SDD + C4 + ADR |
| Локальний запуск | Medium | README Quick Start |
| CI/CD | Medium | ISD + GitHub Actions workflow |
| API contracts | Medium | SDD API section |
| Privacy mechanisms | Medium | SDD + privacy_inventory.md |
| Documentation maintenance | Medium | docs/maintenance.md |

## 6. План збільшення Bus Factor

- підтримувати документацію актуальною;
- використовувати правило "code change = documentation change";
- проводити регулярні architecture reviews;
- уникати недокументованих ручних операцій;
- зберігати архітектурні рішення в ADR;
- передавати ownership критичних компонентів щонайменше двом людям у командному проєкті.

## 7. Handover Readiness Checklist

- [x] README існує.
- [x] Quick Start існує.
- [x] SDD існує.
- [x] ISD існує.
- [x] Два ADR існують.
- [x] API contracts задокументовані.
- [x] CI/CD задокументовано.
- [x] RTO/RPO визначені.
- [x] Documentation Maintenance Regime існує.
- [x] Documentation Decay FAIL → PASS перевірено.
- [x] Bus Factor задекларовано.

## 8. Final Verdict

Система перебуває у стані ALWAYS READY TO HANDOVER.

Основні знання про архітектуру, запуск, інфраструктуру, API, CI/CD та супровід документації зафіксовані у репозиторії та можуть бути передані новому розробнику без залежності від усного пояснення.

STATUS: ALWAYS READY TO HANDOVER
