---
owner: Project Owner
status: completed
review_date: 2027-02-19
---

# AI Tech Lead Validation Log — Lab 12

## 1. Scope

Перевірено виконання Лабораторної роботи №12 для проєкту QualityLab_1.

Перевірка охоплювала:

- SRE runbook;
- SLA / SLO / SLI;
- Error Budget;
- RFC та Impact Analysis;
- CCB;
- Release Checklist;
- legacy-компонент;
- контрольований інцидент;
- FAIL → PASS;
- Post-Mortem;
- CAPA;
- SWEBOK Maintenance Plan.

## 2. Incident Crash Test

Legacy-компонент:

`external_service.py`

Зовнішня залежність:

`127.0.0.1:5001`

Під час контрольованого тесту зовнішній сервіс був недоступний.

Результат:

- 5 контрольних запитів;
- 5 degraded responses;
- HTTP 200;
- fallback activated;
- 3 attempts;
- latency приблизно 616–622 ms.

FAIL evidence:

`lab12_results/incident_fail.log`

FAIL commit:

`4a8e6aa ops(incident): capture legacy module outage, FAIL`

Validation result:

PASS — контрольований інцидент відтворено та задокументовано.

## 3. CAPA Effectiveness Check

Для CAPA-01 реалізовано:

`scripts/check_external_dependency.py`

Перевірено два стани зовнішньої залежності.

### DOWN

Результат:

`EXTERNAL DEPENDENCY: UNAVAILABLE`

Exit code:

`1`

Evidence:

`lab12_results/capa01_down.log`

### UP

Результат:

`EXTERNAL DEPENDENCY: AVAILABLE`

HTTP:

`200`

Exit code:

`0`

Evidence:

`lab12_results/capa01_up.log`

CAPA-01 Effectiveness Check:

PASS.

## 4. Regression Validation

Після змін виконано автоматичні тести.

Результат:

`25 passed`

Regression status:

PASS.

## 5. FAIL → PASS Traceability

FAIL:

`4a8e6aa ops(incident): capture legacy module outage, FAIL`

PASS:

`c769b24 docs(maintenance): deliver capa actions and swebok plan, PASS`

Ланцюг FAIL → PASS зафіксовано у Git.

## 6. Maintenance Documentation

Перевірено наявність:

- `docs/incidents/INC-001.md`;
- `docs/incidents/POSTMORTEM-INC-001.md`;
- `docs/incidents/CAPA-INC-001.md`;
- `docs/legacy/external-service.md`;
- `docs/maintenance-plan.md`;
- `docs/runbooks/RB-001.md`;
- `docs/slo.yaml`.

SWEBOK Maintenance Plan містить:

- L1 / L2 / L3;
- правила ескалації;
- severity levels;
- Known Issues;
- runbook references;
- SLO references.

## 7. Final Validation

Incident simulation: PASS

FAIL evidence: PASS

CAPA effectiveness check: PASS

Regression tests: PASS

FAIL → PASS Git traceability: PASS

Maintenance Plan: PASS

Operational documentation: PASS

FINAL VALIDATION STATUS: PASS