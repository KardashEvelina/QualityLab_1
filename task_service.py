class TaskService:
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
        for task in self.tasks:
            if task["title"] == title:
                task["completed"] = True
                return True

        return False

    def get_tasks_by_priority(self, priority):
        result = []

        for task in self.tasks:
            if task["priority"] == priority:
                result.append(task)

        return result

    def count_completed(self):
        count = 0

        for task in self.tasks:
            if task["completed"]:
                count += 1

        return count