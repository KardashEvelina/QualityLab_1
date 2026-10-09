from flask import Flask, jsonify, request

from external_service import get_external_status
from task_service import TaskService

app = Flask(__name__)

task_service = TaskService()

task_service.add_task("Prepare laboratory report", "high")
task_service.add_task("Run performance test", "medium")
task_service.add_task("Check resilience scenario", "high")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200


@app.route("/tasks/summary", methods=["GET"])
def tasks_summary():
    mode = request.args.get("mode", "normal")

    external_status = get_external_status(mode)

    return jsonify({
        "total_tasks": len(task_service.tasks),
        "completed_tasks": task_service.count_completed(),
        "high_priority_tasks": len(
            task_service.get_tasks_by_priority("high")
        ),
        "external_status": external_status
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
