import hashlib
import json
import logging
import uuid

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from consent_service import ConsentService
from external_service import (
    ExternalRequest,
    ExternalStatus,
    get_external_status,
)
from privacy_data_service import PrivacyDataService
from privacy_logging import (
    configure_privacy_logging,
    sanitize_mapping,
    sanitize_text,
)
from report_service import ReportService
from task_service import TaskService
from user_service import UserService


class Lab8GodObject:
    def __init__(self):
        self.consent_service = ConsentService()
        self.privacy_service = PrivacyDataService()
        self.report_service = ReportService()
        self.task_service = TaskService()
        self.user_service = UserService()

        self.logger = logging.getLogger(
            "lab8-god-object"
        )
        configure_privacy_logging(
            self.logger
        )

        self.audit_log = []

        self.snapshot_path = Path(
            "lab8_results/god_object_snapshot.json"
        )

        self.external_request = ExternalRequest(
            mode="normal",
            attempt=1,
        )

        self.external_status_type = ExternalStatus
        self.external_gateway = get_external_status

    def _record(self, action, payload):
        event = {
            "id": str(uuid.uuid4()),
            "action": sanitize_text(action),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "payload": sanitize_mapping(
                payload
            ),
        }

        self.audit_log.append(event)
        return event

    def register_user_and_task(
        self,
        name,
        email,
        title,
        priority="medium",
    ):
        user_created = self.user_service.add_user(
            name,
            email,
        )

        task_created = self.task_service.add_task(
            title,
            priority,
        )

        fingerprint = hashlib.sha256(
            email.encode("utf-8")
        ).hexdigest()

        result = {
            "user_created": user_created,
            "task_created": task_created,
            "fingerprint": fingerprint,
            "tasks": deepcopy(
                self.task_service.tasks
            ),
        }

        self._record(
            "register_user_and_task",
            result,
        )

        return result

    def build_task_report(self):
        report = (
            self.report_service
            .generate_task_report(
                self.task_service.tasks
            )
        )

        self._record(
            "build_task_report",
            report,
        )

        return report

    def grant_marketing_consent(
        self,
        user_id,
    ):
        result, status = (
            self.consent_service.grant_consent(
                actor_id=user_id,
                user_id=user_id,
                purpose="MARKETING_EMAIL",
                policy_version="1.0",
                source="lab8",
            )
        )

        self._record(
            "grant_marketing_consent",
            {
                "status": status,
                "result": result,
            },
        )

        return result, status

    def export_privacy_data(
        self,
        user_id,
    ):
        result, status = (
            self.privacy_service
            .export_personal_data(
                actor_id=user_id,
                subject_id=user_id,
            )
        )

        self._record(
            "export_privacy_data",
            {
                "status": status,
                "result": result,
            },
        )

        return result, status

    def describe_external_dependency(self):
        result = {
            "request": {
                "mode":
                    self.external_request.mode,
                "attempt":
                    self.external_request.attempt,
            },
            "status_type":
                self.external_status_type.__name__,
            "gateway":
                self.external_gateway.__name__,
        }

        self._record(
            "describe_external_dependency",
            result,
        )

        return result

    def persist_snapshot(self):
        snapshot = {
            "users":
                self.user_service.users,
            "tasks":
                self.task_service.tasks,
            "audit":
                self.audit_log,
        }

        self.snapshot_path.write_text(
            json.dumps(
                snapshot,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        self._record(
            "persist_snapshot",
            {
                "path":
                    str(self.snapshot_path)
            },
        )

        return self.snapshot_path
