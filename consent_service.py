from copy import deepcopy
from datetime import datetime, timezone


class ConsentService:
    VALID_PURPOSES = {
        "MARKETING_EMAIL",
        "OPTIONAL_ANALYTICS",
    }

    def __init__(self):
        self.consents = {}
        self.history = []
        self.side_effects = []

    def _now(self):
        return datetime.now(
            timezone.utc
        ).isoformat()

    def _key(self, user_id, purpose):
        return user_id, purpose

    def _validate_purpose(self, purpose):
        return purpose in self.VALID_PURPOSES

    def grant_consent(
        self,
        actor_id,
        user_id,
        purpose,
        policy_version,
        source
    ):
        if actor_id != user_id:
            return None, 404

        if not self._validate_purpose(purpose):
            return {
                "error": "invalid_purpose"
            }, 400

        key = self._key(
            user_id,
            purpose
        )

        now = self._now()

        current = self.consents.get(key)

        if (
            current is not None
            and current["status"] == "GRANTED"
            and current["policy_version"]
            == policy_version
        ):
            return deepcopy(current), 200

        consent = {
            "user_id": user_id,
            "purpose": purpose,
            "status": "GRANTED",
            "policy_version": policy_version,
            "granted_at": now,
            "withdrawn_at": None,
            "updated_at": now,
            "source": source,
        }

        self.consents[key] = consent

        self.history.append({
            "user_id": user_id,
            "purpose": purpose,
            "action": "GRANT",
            "policy_version": policy_version,
            "timestamp": now,
            "source": source,
        })

        return deepcopy(consent), 200

    def revoke_consent(
        self,
        actor_id,
        user_id,
        purpose
    ):
        if actor_id != user_id:
            return None, 404

        if not self._validate_purpose(purpose):
            return {
                "error": "invalid_purpose"
            }, 400

        key = self._key(
            user_id,
            purpose
        )

        current = self.consents.get(key)

        if current is None:
            return {
                "status": "REVOKED",
                "user_id": user_id,
                "purpose": purpose,
            }, 200

        if current["status"] == "REVOKED":
            return deepcopy(current), 200

        now = self._now()

        current["status"] = "REVOKED"
        current["withdrawn_at"] = now
        current["updated_at"] = now

        self.history.append({
            "user_id": user_id,
            "purpose": purpose,
            "action": "REVOKE",
            "policy_version":
                current["policy_version"],
            "timestamp": now,
            "source": current["source"],
        })

        return deepcopy(current), 200

    def get_consent(
        self,
        user_id,
        purpose
    ):
        key = self._key(
            user_id,
            purpose
        )

        consent = self.consents.get(key)

        if consent is None:
            return None

        return deepcopy(consent)

    def is_allowed(
        self,
        user_id,
        purpose,
        required_policy_version
    ):
        consent = self.get_consent(
            user_id,
            purpose
        )

        if consent is None:
            return False

        if consent["status"] != "GRANTED":
            return False

        if (
            consent["policy_version"]
            != required_policy_version
        ):
            return False

        return True

    def perform_optional_action(
        self,
        user_id,
        purpose,
        required_policy_version
    ):
        allowed = self.is_allowed(
            user_id=user_id,
            purpose=purpose,
            required_policy_version=
                required_policy_version
        )

        if not allowed:
            return {
                "status": "DENY",
                "side_effect_created": False,
            }, 403

        side_effect = {
            "user_id": user_id,
            "purpose": purpose,
            "action": "optional_operation_executed",
            "timestamp": self._now(),
        }

        self.side_effects.append(
            side_effect
        )

        return {
            "status": "ALLOW",
            "side_effect_created": True,
        }, 200

    def get_history(self, user_id):
        return [
            deepcopy(item)
            for item in self.history
            if item["user_id"] == user_id
        ]
