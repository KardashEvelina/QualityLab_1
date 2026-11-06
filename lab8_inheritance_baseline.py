class BasePlanningService:
    def create_plan(self):
        return "base:create"

    def validate_plan(self):
        return "base:validate"

    def load_tasks(self):
        return "base:load"

    def calculate_capacity(self):
        return "base:capacity"

    def prioritize_tasks(self):
        return "base:prioritize"

    def schedule_tasks(self):
        return "base:schedule"

    def save_plan(self):
        return "base:save"

    def notify_user(self):
        return "base:notify"


class ManagedPlanningService(
    BasePlanningService
):
    # Перевизначення логіки батьківського класу.
    def validate_plan(self):
        return "managed:validate"

    def calculate_capacity(self):
        return "managed:capacity"

    def prioritize_tasks(self):
        return "managed:prioritize"

    def schedule_tasks(self):
        return "managed:schedule"

    # Новий публічний інтерфейс.
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


class AdaptivePlanningService(
    ManagedPlanningService
):
    # Дочірній клас знову змушений
    # переписувати успадковану поведінку.
    def validate_plan(self):
        return "adaptive:validate"

    def calculate_capacity(self):
        return "adaptive:capacity"

    def prioritize_tasks(self):
        return "adaptive:prioritize"

    def schedule_tasks(self):
        return "adaptive:schedule"

    def detect_conflicts(self):
        return "adaptive:conflicts"

    def update_deadlines(self):
        return "adaptive:deadlines"

    # Ще більше публічних методів.
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
