from consent_service import ConsentService
from privacy_data_service import PrivacyDataService
from report_service import ReportService
from task_service import TaskService
from user_service import UserService

from lab8_adapters import (
    AuditLogAdapter,
    ConsentServiceAdapter,
    ExternalStatusAdapter,
    PrivacyDataAdapter,
    ReportServiceAdapter,
    TaskServiceAdapter,
    UserServiceAdapter,
)
from lab8_pass_architecture import (
    AuditCoordinator,
    PrivacyCoordinator,
    RegistrationCoordinator,
    ReportingCoordinator,
)


audit = AuditLogAdapter()

user_port = UserServiceAdapter(
    UserService()
)

task_port = TaskServiceAdapter(
    TaskService()
)

report_port = ReportServiceAdapter(
    ReportService()
)

consent_port = ConsentServiceAdapter(
    ConsentService()
)

privacy_port = PrivacyDataAdapter(
    PrivacyDataService()
)

external_port = ExternalStatusAdapter()


registration = RegistrationCoordinator(
    user_port,
    task_port,
    audit,
)

reporting = ReportingCoordinator(
    task_port,
    report_port,
    audit,
)

privacy = PrivacyCoordinator(
    consent_port,
    privacy_port,
    audit,
)

external = AuditCoordinator(
    external_port,
    audit,
)


print("===== INTERFACE DECOMPOSITION PASS =====")

print(
    registration.register(
        name="Evelina",
        email="evelina@example.com",
        title="Lab 8 audit",
        priority="high",
    )
)

print(
    reporting.build_report()
)

privacy_result = (
    privacy.process_user_privacy(1)
)

print({
    "consent_status":
        privacy_result[
            "consent_status"
        ],
    "export_status":
        privacy_result[
            "export_status"
        ],
})

print(
    external.check_external_status()
)

print(
    "Audit events:",
    len(audit.events),
)

print("STATUS: PASS")
