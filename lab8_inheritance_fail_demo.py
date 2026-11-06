from lab8_inheritance_baseline import (
    AdaptivePlanningService,
    BasePlanningService,
    ManagedPlanningService,
)


services = [
    BasePlanningService(),
    ManagedPlanningService(),
    AdaptivePlanningService(),
]

print("===== INHERITANCE FRAGILITY CRASH =====")

failures = 0

for service in services:
    class_name = type(service).__name__

    try:
        service.create_plan()

        print(
            f"{class_name}: UNEXPECTED PASS"
        )

    except TypeError as error:
        failures += 1

        print(
            f"{class_name}: FAIL"
        )

        print(
            f"  {error}"
        )


print()
print(
    f"Broken hierarchy levels: {failures}/3"
)

if failures == 3:
    print(
        "STATUS: INHERITANCE FRAGILITY FAIL"
    )
else:
    print(
        "STATUS: CRASH TEST INCOMPLETE"
    )
