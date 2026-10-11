from app import app, consent_service


def reset_consent_service():
    consent_service.__init__()


def test_consent_flow_deny_grant_allow_revoke_deny():
    reset_consent_service()

    client = app.test_client()

    # Початковий стан: DENY
    initial = client.post(
        "/api/users/1/optional-action/MARKETING_EMAIL",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0"
        }
    )

    assert initial.status_code == 403
    assert initial.get_json() == {
        "status": "DENY",
        "side_effect_created": False
    }

    # GRANT
    grant = client.post(
        "/api/users/1/consents/MARKETING_EMAIL/grant",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0",
            "source": "web"
        }
    )

    assert grant.status_code == 200

    grant_data = grant.get_json()

    assert grant_data["status"] == "GRANTED"
    assert grant_data["purpose"] == "MARKETING_EMAIL"
    assert grant_data["policy_version"] == "1.0"
    assert grant_data["source"] == "web"
    assert grant_data["granted_at"] is not None
    assert grant_data["withdrawn_at"] is None

    # ALLOW
    allowed = client.post(
        "/api/users/1/optional-action/MARKETING_EMAIL",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0"
        }
    )

    assert allowed.status_code == 200
    assert allowed.get_json() == {
        "status": "ALLOW",
        "side_effect_created": True
    }

    assert len(consent_service.side_effects) == 1

    # REVOKE
    revoke = client.post(
        "/api/users/1/consents/MARKETING_EMAIL/revoke",
        headers={
            "X-User-Id": "1"
        }
    )

    assert revoke.status_code == 200

    revoke_data = revoke.get_json()

    assert revoke_data["status"] == "REVOKED"
    assert revoke_data["withdrawn_at"] is not None

    # Після REVOKE знову DENY
    denied = client.post(
        "/api/users/1/optional-action/MARKETING_EMAIL",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0"
        }
    )

    assert denied.status_code == 403
    assert denied.get_json() == {
        "status": "DENY",
        "side_effect_created": False
    }

    # Новий side effect після REVOKE не створено
    assert len(consent_service.side_effects) == 1


def test_consent_is_purpose_specific():
    reset_consent_service()

    client = app.test_client()

    # Даємо згоду лише на MARKETING_EMAIL
    grant = client.post(
        "/api/users/1/consents/MARKETING_EMAIL/grant",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0",
            "source": "web"
        }
    )

    assert grant.status_code == 200

    # MARKETING_EMAIL дозволено
    marketing = client.post(
        "/api/users/1/optional-action/MARKETING_EMAIL",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0"
        }
    )

    assert marketing.status_code == 200
    assert marketing.get_json()["status"] == "ALLOW"

    # OPTIONAL_ANALYTICS все одно заборонено
    analytics = client.post(
        "/api/users/1/optional-action/OPTIONAL_ANALYTICS",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0"
        }
    )

    assert analytics.status_code == 403
    assert analytics.get_json() == {
        "status": "DENY",
        "side_effect_created": False
    }


def test_consent_history_contains_grant_and_revoke():
    reset_consent_service()

    client = app.test_client()

    client.post(
        "/api/users/1/consents/MARKETING_EMAIL/grant",
        headers={
            "X-User-Id": "1"
        },
        json={
            "policy_version": "1.0",
            "source": "web"
        }
    )

    client.post(
        "/api/users/1/consents/MARKETING_EMAIL/revoke",
        headers={
            "X-User-Id": "1"
        }
    )

    response = client.get(
        "/api/users/1/consents/history",
        headers={
            "X-User-Id": "1"
        }
    )

    assert response.status_code == 200

    history = response.get_json()["history"]

    assert len(history) == 2
    assert history[0]["action"] == "GRANT"
    assert history[1]["action"] == "REVOKE"

    assert history[0]["policy_version"] == "1.0"
    assert history[0]["source"] == "web"
