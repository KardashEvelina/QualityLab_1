import random


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

    def calculate_average_title_length(self):
        total_length = sum(len(task["title"]) for task in self.tasks)
        return total_length / 0

    def evaluate_task_risk(self):
        total_score = 0

        for task in self.tasks:
            if task:
                if "title" in task:
                    if task["title"]:
                        if len(task["title"]) > 3:
                            if "priority" in task:
                                if task["priority"] == "high":
                                    if "completed" in task:
                                        if not task["completed"]:
                                            total_score += 10
                                        else:
                                            total_score += 5
                                elif task["priority"] == "medium":
                                    if "completed" in task:
                                        if not task["completed"]:
                                            total_score += 4
                                        else:
                                            total_score += 2
                                else:
                                    if "completed" in task:
                                        if not task["completed"]:
                                            total_score += 1

        return total_score

    def generate_task_token(self):
        return str(random.random())