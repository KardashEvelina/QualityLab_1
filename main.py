from task_service import TaskService
from user_service import UserService
from report_service import ReportService


def main():
    task_service = TaskService()
    user_service = UserService()
    report_service = ReportService()

    user_service.add_user("Anna", "anna@example.com")
    user_service.add_user("John", "john@example.com")

    task_service.add_task("Prepare report", "high")
    task_service.add_task("Read documentation", "medium")
    task_service.add_task("Complete laboratory", "high")

    task_service.complete_task("Prepare report")

    report = report_service.generate_task_report(task_service.tasks)

    print("Users:", len(user_service.get_active_users()))
    print("Tasks:", report["total"])
    print("Completed:", report["completed"])
    print("High priority:", report["high_priority"])
    print("Completion rate:",
          report_service.get_completion_rate(task_service.tasks))


if __name__ == "__main__":
    main()