from datetime import datetime, timezone

from consent_service import ConsentService
from external_service import get_external_status
from privacy_data_service import PrivacyDataService
from privacy_logging import (
    sanitize_mapping,
    sanitize_text,
)
from report_service import ReportService
from task_service import TaskService
from user_service import UserService


class UserServiceAdapter:
    def __init__(self, service: UserService):
        self.service = service

    def add_user(self, name, email):
        return self.service.add_user(
            name,
            email,
        )


class TaskServiceAdapter:
    def __init__(self, service: TaskService):
        self.service = service

    def add_task(
        self,
        title,
        priority="medium",
    ):
        return self.service.add_task(
            title,
            priority,
        )

    def list_tasks(self):
        return list(
            self.service.tasks
        )


class ReportServiceAdapter:
    def __init__(self, service: ReportService):
        self.service = service

    def generate(self, tasks):
        return (
            self.service
            .generate_task_report(
                tasks,
                report_format="summary",
            )
        )


class ConsentServiceAdapter:
    def __init__(
        self,
        service: ConsentService,
    ):
        self.service = service

    def grant_marketing(self, user_id):
        return self.service.grant_consent(
            actor_id=user_id,
            user_id=user_id,
            purpose="MARKETING_EMAIL",
            policy_version="1.0",
            source="lab8",
        )


class PrivacyDataAdapter:
    def __init__(
        self,
        service: PrivacyDataService,
    ):
        self.service = service

    def export(self, user_id):
        return (
            self.service
            .export_personal_data(
                actor_id=user_id,
                subject_id=user_id,
            )
        )


class AuditLogAdapter:
    def __init__(self):
        self.events = []

    def record(
        self,
        action,
        payload,
    ):
        event = {
            "action":
                sanitize_text(action),
            "payload":
                sanitize_mapping(payload),
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        self.events.append(event)
        return event


class ExternalStatusAdapter:
    def get_status(self):
        return get_external_status(
            mode="normal"
        )
