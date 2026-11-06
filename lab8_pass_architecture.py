from lab8_contracts import (
    AuditPort,
    ConsentPort,
    ExternalStatusPort,
    PrivacyPort,
    ReportPort,
    TaskPort,
    UserPort,
)


class RegistrationCoordinator:
    def __init__(
        self,
        user_port: UserPort,
        task_port: TaskPort,
        audit_port: AuditPort,
    ):
        self.user_port = user_port
        self.task_port = task_port
        self.audit_port = audit_port

    def register(
        self,
        name,
        email,
        title,
        priority="medium",
    ):
        user_created = (
            self.user_port.add_user(
                name,
                email,
            )
        )

        task_created = (
            self.task_port.add_task(
                title,
                priority,
            )
        )

        result = {
            "user_created":
                user_created,
            "task_created":
                task_created,
        }

        self.audit_port.record(
            "registration",
            result,
        )

        return result


class ReportingCoordinator:
    def __init__(
        self,
        task_port: TaskPort,
        report_port: ReportPort,
        audit_port: AuditPort,
    ):
        self.task_port = task_port
        self.report_port = report_port
        self.audit_port = audit_port

    def build_report(self):
        tasks = (
            self.task_port.list_tasks()
        )

        report = (
            self.report_port.generate(
                tasks
            )
        )

        self.audit_port.record(
            "task_report",
            report,
        )

        return report


class PrivacyCoordinator:
    def __init__(
        self,
        consent_port: ConsentPort,
        privacy_port: PrivacyPort,
        audit_port: AuditPort,
    ):
        self.consent_port = consent_port
        self.privacy_port = privacy_port
        self.audit_port = audit_port

    def process_user_privacy(
        self,
        user_id,
    ):
        consent, consent_status = (
            self.consent_port
            .grant_marketing(
                user_id
            )
        )

        exported, export_status = (
            self.privacy_port.export(
                user_id
            )
        )

        result = {
            "consent_status":
                consent_status,
            "export_status":
                export_status,
            "consent":
                consent,
            "export":
                exported,
        }

        self.audit_port.record(
            "privacy_operation",
            {
                "consent_status":
                    consent_status,
                "export_status":
                    export_status,
            },
        )

        return result


class AuditCoordinator:
    def __init__(
        self,
        external_port:
            ExternalStatusPort,
        audit_port:
            AuditPort,
    ):
        self.external_port = (
            external_port
        )
        self.audit_port = (
            audit_port
        )

    def check_external_status(self):
        status = (
            self.external_port
            .get_status()
        )

        self.audit_port.record(
            "external_status",
            status,
        )

        return status
