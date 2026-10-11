import logging

from flask import Flask, jsonify, request

from consent_service import ConsentService
from external_service import get_external_status
from privacy_data_service import PrivacyDataService
from privacy_logging import configure_privacy_logging
from task_service import TaskService


app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


logger = logging.getLogger("privacy-demo")
configure_privacy_logging(logger)


task_service = TaskService()
privacy_data_service = PrivacyDataService()
consent_service = ConsentService()


task_service.add_task(
    "Prepare laboratory report",
    "high"
)

task_service.add_task(
    "Run performance test",
    "medium"
)

task_service.add_task(
    "Check resilience scenario",
    "high"
)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    }), 200


@app.route("/tasks/summary", methods=["GET"])
def tasks_summary():
    mode = request.args.get(
        "mode",
        "normal"
    )

    external_status = get_external_status(
        mode
    )

    return jsonify({
        "total_tasks": len(
            task_service.tasks
        ),
        "completed_tasks":
            task_service.count_completed(),
        "high_priority_tasks": len(
            task_service.get_tasks_by_priority(
                "high"
            )
        ),
        "external_status":
            external_status
    }), 200


@app.route(
    "/privacy/log-demo",
    methods=["GET"]
)
def privacy_log_demo():
    demo_data = {
        "operation": "profile_update",
        "email": "olena.test@example.com",
        "phone": "+380501234567",
        "password": "DemoPassword123!",
        "access_token":
            "synthetic-access-token",
        "correlation_id":
            "privacy-demo-001",
        "profile": {
            "email":
                "nested.user@example.com",
            "phone":
                "+380671112233",
            "reset_token":
                "synthetic-reset-token"
        }
    }

    logger.info(demo_data)

    try:
        raise ValueError(
            "Failed request for "
            "email=exception.user@example.com "
            "phone=+380931234567 "
            "password=ExceptionPassword123!"
        )

    except ValueError as error:
        logger.error(
            "Operation failed: %s",
            error
        )

    return jsonify({
        "status": "logged",
        "correlation_id":
            "privacy-demo-001"
    }), 200


@app.route(
    "/api/users/<int:subject_id>/personal-data",
    methods=["GET"]
)
def export_personal_data(subject_id):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    if actor_id is None:
        return jsonify({
            "error": "not_found"
        }), 404

    export, status_code = (
        privacy_data_service.export_personal_data(
            actor_id=actor_id,
            subject_id=subject_id
        )
    )

    if export is None:
        return jsonify({
            "error": "not_found"
        }), status_code

    logger.info({
        "operation": "personal_data_export",
        "actor_id": actor_id,
        "subject_id": subject_id,
        "result": "success",
        "correlation_id": "privacy-export-001"
    })

    return jsonify(export), status_code


@app.route(
    "/api/users/<int:subject_id>/privacy-state",
    methods=["GET"]
)
def get_privacy_state(subject_id):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    if actor_id != subject_id:
        return jsonify({
            "error": "not_found"
        }), 404

    state = privacy_data_service.get_privacy_state(
        subject_id
    )

    if state is None:
        return jsonify({
            "error": "not_found"
        }), 404

    return jsonify(state), 200


@app.route(
    "/api/users/<int:subject_id>/anonymize",
    methods=["POST"]
)
def anonymize_user(subject_id):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    correlation_id = request.headers.get(
        "X-Correlation-Id",
        "privacy-anonymize-001"
    )

    if actor_id is None:
        return jsonify({
            "error": "not_found"
        }), 404

    result, status_code = (
        privacy_data_service.anonymize_user(
            actor_id=actor_id,
            subject_id=subject_id,
            correlation_id=correlation_id
        )
    )

    if result is None:
        return jsonify({
            "error": "not_found"
        }), status_code

    logger.info({
        "operation": "user_anonymization",
        "actor_id": actor_id,
        "subject_id": subject_id,
        "result": result["status"],
        "correlation_id": correlation_id
    })

    return jsonify(result), status_code


@app.route(
    "/api/users/<int:user_id>/consents/<purpose>/grant",
    methods=["POST"]
)
def grant_consent(user_id, purpose):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    body = request.get_json(
        silent=True
    ) or {}

    policy_version = body.get(
        "policy_version",
        "1.0"
    )

    source = body.get(
        "source",
        "web"
    )

    result, status_code = (
        consent_service.grant_consent(
            actor_id=actor_id,
            user_id=user_id,
            purpose=purpose,
            policy_version=policy_version,
            source=source
        )
    )

    if result is None:
        return jsonify({
            "error": "not_found"
        }), status_code

    return jsonify(result), status_code


@app.route(
    "/api/users/<int:user_id>/consents/<purpose>/revoke",
    methods=["POST"]
)
def revoke_consent(user_id, purpose):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    result, status_code = (
        consent_service.revoke_consent(
            actor_id=actor_id,
            user_id=user_id,
            purpose=purpose
        )
    )

    if result is None:
        return jsonify({
            "error": "not_found"
        }), status_code

    return jsonify(result), status_code


@app.route(
    "/api/users/<int:user_id>/consents/history",
    methods=["GET"]
)
def consent_history(user_id):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    if actor_id != user_id:
        return jsonify({
            "error": "not_found"
        }), 404

    return jsonify({
        "user_id": user_id,
        "history":
            consent_service.get_history(
                user_id
            )
    }), 200


@app.route(
    "/api/users/<int:user_id>/optional-action/<purpose>",
    methods=["POST"]
)
def optional_action(user_id, purpose):
    actor_id = request.headers.get(
        "X-User-Id",
        type=int
    )

    if actor_id != user_id:
        return jsonify({
            "error": "not_found"
        }), 404

    body = request.get_json(
        silent=True
    ) or {}

    required_policy_version = (
        body.get(
            "policy_version",
            "1.0"
        )
    )

    result, status_code = (
        consent_service.perform_optional_action(
            user_id=user_id,
            purpose=purpose,
            required_policy_version=
                required_policy_version
        )
    )

    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
