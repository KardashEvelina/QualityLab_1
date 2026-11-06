class PlanningCore:
    def create_plan(
        self,
        plan_mode,
    ):
        return f"core:create:{plan_mode}"

    def validate_plan(self):
        return "core:validate"

    def load_tasks(self):
        return "core:load"

    def calculate_capacity(self):
        return "core:capacity"

    def prioritize_tasks(self):
        return "core:prioritize"

    def schedule_tasks(self):
        return "core:schedule"

    def save_plan(self):
        return "core:save"

    def notify_user(self):
        return "core:notify"


class ManagedPlanningService:
    def __init__(
        self,
        core: PlanningCore,
    ):
        self._core = core

    def create_plan(self):
        return self._core.create_plan(
            "managed"
        )

    def validate_plan(self):
        return self._core.validate_plan()

    def calculate_capacity(self):
        return (
            self._core
            .calculate_capacity()
        )

    def assign_owner(self):
        return "managed:owner"

    def estimate_effort(self):
        return "managed:effort"

    def detect_conflicts(self):
        return "managed:conflicts"

    def calculate_risk(self):
        return "managed:risk"

    def generate_summary(self):
        return "managed:summary"

    def export_calendar(self):
        return "managed:calendar"

    def track_progress(self):
        return "managed:progress"

    def update_deadlines(self):
        return "managed:deadlines"


class AdaptivePlanningService:
    def __init__(
        self,
        core: PlanningCore,
        managed:
            ManagedPlanningService,
    ):
        self._core = core
        self._managed = managed

    def create_plan(self):
        return self._core.create_plan(
            "adaptive"
        )

    def validate_plan(self):
        return self._core.validate_plan()

    def calculate_capacity(self):
        return (
            self._core
            .calculate_capacity()
        )

    def prioritize_tasks(self):
        return (
            self._core
            .prioritize_tasks()
        )

    def schedule_tasks(self):
        return (
            self._core
            .schedule_tasks()
        )

    def detect_conflicts(self):
        return (
            self._managed
            .detect_conflicts()
        )

    def update_deadlines(self):
        return (
            self._managed
            .update_deadlines()
        )

    def rebalance_load(self):
        return "adaptive:rebalance"

    def reschedule_overdue(self):
        return "adaptive:overdue"

    def predict_overload(self):
        return "adaptive:predict"

    def suggest_breaks(self):
        return "adaptive:breaks"

    def calculate_focus_score(self):
        return "adaptive:focus"

    def generate_weekly_plan(self):
        return "adaptive:weekly"

    def adapt_to_capacity(self):
        return "adaptive:adapt"

    def recover_failed_plan(self):
        return "adaptive:recover"
