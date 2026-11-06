from typing import Protocol


class UserPort(Protocol):
    def add_user(
        self,
        name: str,
        email: str,
    ) -> bool:
        ...


class TaskPort(Protocol):
    def add_task(
        self,
        title: str,
        priority: str = "medium",
    ) -> bool:
        ...

    def list_tasks(self) -> list[dict]:
        ...


class ReportPort(Protocol):
    def generate(
        self,
        tasks: list[dict],
    ) -> dict:
        ...


class ConsentPort(Protocol):
    def grant_marketing(
        self,
        user_id: int,
    ) -> tuple:
        ...


class PrivacyPort(Protocol):
    def export(
        self,
        user_id: int,
    ) -> tuple:
        ...


class AuditPort(Protocol):
    def record(
        self,
        action: str,
        payload: dict,
    ) -> dict:
        ...


class ExternalStatusPort(Protocol):
    def get_status(self) -> dict:
        ...
