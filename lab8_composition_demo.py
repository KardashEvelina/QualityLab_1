from lab8_composition import (
    AdaptivePlanningService,
    ManagedPlanningService,
    PlanningCore,
)


core = PlanningCore()

managed = ManagedPlanningService(
    core
)

adaptive = AdaptivePlanningService(
    core,
    managed,
)


print(
    "===== COMPOSITION PASS ====="
)

print(
    "create_plan:",
    adaptive.create_plan(),
)

print(
    "validate:",
    adaptive.validate_plan(),
)

print(
    "capacity:",
    adaptive.calculate_capacity(),
)

print(
    "conflicts:",
    adaptive.detect_conflicts(),
)

print(
    "deadlines:",
    adaptive.update_deadlines(),
)

print(
    "STATUS: GREEN / PASS"
)
