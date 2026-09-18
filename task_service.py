import secrets


class TaskService:
    PRIORITY_SCORES = {
        "high": {
            False: 10,
            True: 5
        },
        "medium": {
            False: 4,
            True: 2
        },
        "low": {
            False: 1,
            True: 0
        }
    }

    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority="medium"):
        if not title:
            return False

        task = {
            "title": title,
            "priority": priority,
            "completed": False
        }

        self.tasks.append(task)
        return True

    def complete_task(self, title):
        task = next(
            (task for task in self.tasks if task["title"] == title),
            None
        )

        if task is None:
            return False

        task["completed"] = True
        return True

    def get_tasks_by_priority(self, priority):
        return [
            task
            for task in self.tasks
            if task["priority"] == priority
        ]

    def count_completed(self):
        return sum(
            1
            for task in self.tasks
            if task["completed"]
        )

    def calculate_average_title_length(self):
        if not self.tasks:
            return 0

        total_length = sum(
            len(task["title"])
            for task in self.tasks
        )

        return total_length / len(self.tasks)

    def evaluate_task_risk(self):
        return sum(
            self._calculate_task_risk(task)
            for task in self.tasks
        )

    def _calculate_task_risk(self, task):
        title = task.get("title", "")

        if len(title) <= 3:
            return 0

        priority = task.get("priority", "low")
        completed = bool(task.get("completed", False))

        scores = self.PRIORITY_SCORES.get(
            priority,
            self.PRIORITY_SCORES["low"]
        )

        return scores[completed]

    def generate_task_token(self):
        return secrets.token_hex(16)