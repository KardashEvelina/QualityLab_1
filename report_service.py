class ReportService:
    def generate_task_report(self, tasks):
        total = len(tasks)
        completed = 0
        high_priority = 0

        for task in tasks:
            if task["completed"]:
                completed += 1

            if task["priority"] == "high":
                high_priority += 1

        return {
            "total": total,
            "completed": completed,
            "high_priority": high_priority
        }

    def get_completion_rate(self, tasks):
        if not tasks:
            return 0

        completed = 0

        for task in tasks:
            if task["completed"]:
                completed += 1

        return completed / len(tasks) * 100