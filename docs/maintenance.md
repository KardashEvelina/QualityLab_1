---
owner: Documentation Owner
status: published
review_date: 2027-02-19
---

# Documentation Maintenance Regime

## 1. Головне правило супроводу

Зміна коду = зміна документації.

Жодна зміна, яка впливає на поведінку, архітектуру, API або розгортання системи, не повинна потрапляти до основної гілки без оновлення відповідної документації.

## 2. Ownership and Review Cycle

| Document | Owner | Review cycle | Last review date |
|---|---|---|---|
| README.md | Project Owner | 90 days | 2026-11-21 |
| docs/sdd.md | System Architect | 180 days | 2026-11-21 |
| docs/isd.md | DevOps Owner | 90 days | 2026-11-21 |
| docs/architecture/adr/ADR-001-python-flask.md | System Architect | 180 days | 2026-11-21 |
| docs/architecture/adr/ADR-002-in-memory-storage.md | System Architect | 180 days | 2026-11-21 |
| docs/audience_coverage.md | Documentation Owner | 90 days | 2026-11-21 |

## 3. Review Policy

- Operational documentation: review at least every 90 days.
- Architectural documentation: review at least every 180 days.
- README must be reviewed after changes to startup, API behaviour or onboarding.
- SDD must be reviewed after architecture or API contract changes.
- ISD must be reviewed after deployment, CI/CD, monitoring or recovery changes.
- ADR records are never rewritten retrospectively; obsolete decisions receive superseded status.

## 4. Pull Request Rule

Перед merge необхідно перевірити:
1. Чи змінено поведінку системи?
2. Чи змінено API?
3. Чи змінено архітектуру?
4. Чи змінено deployment або CI/CD?
5. Якщо так — чи оновлена відповідна документація?

Last documentation restoration: 2026-11-21

STATUS: DOCUMENTATION MAINTENANCE REGIME ACTIVE
