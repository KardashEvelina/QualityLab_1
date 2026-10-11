from copy import deepcopy
from datetime import datetime, timezone


class PrivacyDataService:
    def __init__(self):
        self.users = {
            1: {
                "id": 1,
                "name": "Olena Test",
                "email": "olena.test@example.com",
                "phone": "+380501234567",
                "password_hash": "synthetic-password-hash",
                "reset_token": "synthetic-reset-token",
                "internal_security_flag": True,
                "anonymized": False,
            },
            2: {
                "id": 2,
                "name": "Taras Demo",
                "email": "taras.demo@example.com",
                "phone": "+380671112233",
                "password_hash": "another-synthetic-hash",
                "reset_token": "another-synthetic-token",
                "internal_security_flag": False,
                "anonymized": False,
            },
        }

        self.settings = {
            1: {
                "language": "uk",
                "theme": "dark"
            },
            2: {
                "language": "en",
                "theme": "light"
            },
        }

        self.activity = {
            1: [
                {
                    "action": "login",
                    "timestamp":
                        "2026-10-11T10:00:00Z"
                },
                {
                    "action": "profile_update",
                    "timestamp":
                        "2026-10-11T11:00:00Z"
                },
            ],
            2: [
                {
                    "action": "login",
                    "timestamp":
                        "2026-10-11T09:30:00Z"
                }
            ],
        }

        self.consents = {
            1: [
                {
                    "purpose":
                        "MARKETING_EMAIL",
                    "status":
                        "GRANTED",
                    "policy_version":
                        "1.0",
                    "source":
                        "web",
                }
            ],
            2: [],
        }

        self.business_records = {
            1: [
                {
                    "record_id":
                        "order-1001",
                    "amount":
                        1200,
                    "status":
                        "completed",
                }
            ],
            2: [
                {
                    "record_id":
                        "order-2001",
                    "amount":
                        500,
                    "status":
                        "completed",
                }
            ],
        }

        self.audit_events = []

    def export_personal_data(
        self,
        actor_id,
        subject_id
    ):
        if actor_id != subject_id:
            return None, 404

        user = self.users.get(
            subject_id
        )

        if user is None:
            return None, 404

        profile = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
        }

        export = {
            "schema_version":
                "1.0",
            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "subject_id":
                subject_id,
            "profile":
                profile,
            "settings":
                deepcopy(
                    self.settings.get(
                        subject_id,
                        {}
                    )
                ),
            "activity":
                deepcopy(
                    self.activity.get(
                        subject_id,
                        []
                    )
                ),
            "consents":
                deepcopy(
                    self.consents.get(
                        subject_id,
                        []
                    )
                ),
        }

        return export, 200

    def get_privacy_state(
        self,
        subject_id
    ):
        user = self.users.get(
            subject_id
        )

        if user is None:
            return None

        return {
            "user":
                deepcopy(user),
            "settings":
                deepcopy(
                    self.settings.get(
                        subject_id,
                        {}
                    )
                ),
            "activity":
                deepcopy(
                    self.activity.get(
                        subject_id,
                        []
                    )
                ),
            "consents":
                deepcopy(
                    self.consents.get(
                        subject_id,
                        []
                    )
                ),
            "business_records":
                deepcopy(
                    self.business_records.get(
                        subject_id,
                        []
                    )
                ),
        }

    def anonymize_user(
        self,
        actor_id,
        subject_id,
        correlation_id,
        simulate_failure=False
    ):
        if actor_id != subject_id:
            return None, 404

        user = self.users.get(
            subject_id
        )

        if user is None:
            return None, 404

        if user["anonymized"]:
            return {
                "status":
                    "already_anonymized",
                "subject_id":
                    subject_id,
            }, 200

        snapshot = {
            "user":
                deepcopy(
                    self.users[
                        subject_id
                    ]
                ),
            "settings":
                deepcopy(
                    self.settings.get(
                        subject_id,
                        {}
                    )
                ),
            "activity":
                deepcopy(
                    self.activity.get(
                        subject_id,
                        []
                    )
                ),
            "consents":
                deepcopy(
                    self.consents.get(
                        subject_id,
                        []
                    )
                ),
            "business_records":
                deepcopy(
                    self.business_records.get(
                        subject_id,
                        []
                    )
                ),
            "audit_events":
                deepcopy(
                    self.audit_events
                ),
        }

        try:
            anonymous_email = (
                f"deleted-{subject_id}"
                "@anon.local"
            )

            user["name"] = (
                "ANONYMIZED"
            )

            user["email"] = (
                anonymous_email
            )

            user["phone"] = None

            user["password_hash"] = None

            user["reset_token"] = None

            user[
                "internal_security_flag"
            ] = False

            user["anonymized"] = True

            self.settings[
                subject_id
            ] = {}

            self.consents[
                subject_id
            ] = []

            self.activity[
                subject_id
            ] = [
                {
                    "action":
                        item["action"],
                    "timestamp":
                        item["timestamp"]
                }
                for item
                in self.activity.get(
                    subject_id,
                    []
                )
            ]

            if simulate_failure:
                raise RuntimeError(
                    "Synthetic transaction failure"
                )

            self.audit_events.append({
                "event":
                    "user_anonymized",
                "subject_id":
                    subject_id,
                "actor_id":
                    actor_id,
                "correlation_id":
                    correlation_id,
                "timestamp":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                "result":
                    "success",
            })

            return {
                "status":
                    "anonymized",
                "subject_id":
                    subject_id,
            }, 200

        except Exception:
            self.users[
                subject_id
            ] = snapshot["user"]

            self.settings[
                subject_id
            ] = snapshot[
                "settings"
            ]

            self.activity[
                subject_id
            ] = snapshot[
                "activity"
            ]

            self.consents[
                subject_id
            ] = snapshot[
                "consents"
            ]

            self.business_records[
                subject_id
            ] = snapshot[
                "business_records"
            ]

            self.audit_events = snapshot[
                "audit_events"
            ]

            return {
                "status":
                    "failed",
                "subject_id":
                    subject_id,
            }, 500
