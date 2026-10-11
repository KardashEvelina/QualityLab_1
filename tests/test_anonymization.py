from app import app, privacy_data_service


def reset_privacy_data():
    privacy_data_service.__init__()


def test_anonymization_workflow():
    reset_privacy_data()

    client = app.test_client()

    before = client.get(
        "/api/users/1/privacy-state",
        headers={
            "X-User-Id": "1"
        }
    )

    assert before.status_code == 200

    before_data = before.get_json()

    assert before_data["user"]["name"] == "Olena Test"
    assert before_data["user"]["email"] == "olena.test@example.com"
    assert before_data["user"]["phone"] == "+380501234567"

    response = client.post(
        "/api/users/1/anonymize",
        headers={
            "X-User-Id": "1",
            "X-Correlation-Id": "test-anonymize-001"
        }
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "status": "anonymized",
        "subject_id": 1
    }

    after = client.get(
        "/api/users/1/privacy-state",
        headers={
            "X-User-Id": "1"
        }
    )

    assert after.status_code == 200

    after_data = after.get_json()

    assert after_data["user"]["name"] == "ANONYMIZED"
    assert after_data["user"]["email"] == "deleted-1@anon.local"
    assert after_data["user"]["phone"] is None
    assert after_data["user"]["password_hash"] is None
    assert after_data["user"]["reset_token"] is None
    assert after_data["user"]["anonymized"] is True

    assert after_data["settings"] == {}
    assert after_data["consents"] == []

    assert len(after_data["business_records"]) == 1

    assert (
        after_data["business_records"][0]["record_id"]
        == "order-1001"
    )

    after_text = after.get_data(
        as_text=True
    )

    assert "Olena Test" not in after_text
    assert "olena.test@example.com" not in after_text
    assert "+380501234567" not in after_text

    assert len(privacy_data_service.audit_events) == 1

    audit_text = str(
        privacy_data_service.audit_events
    )

    assert "Olena Test" not in audit_text
    assert "olena.test@example.com" not in audit_text
    assert "+380501234567" not in audit_text


def test_anonymization_is_idempotent():
    reset_privacy_data()

    client = app.test_client()

    first = client.post(
        "/api/users/1/anonymize",
        headers={
            "X-User-Id": "1"
        }
    )

    assert first.status_code == 200
    assert first.get_json()["status"] == "anonymized"

    first_state = (
        privacy_data_service.get_privacy_state(1)
    )

    second = client.post(
        "/api/users/1/anonymize",
        headers={
            "X-User-Id": "1"
        }
    )

    assert second.status_code == 200

    assert (
        second.get_json()["status"]
        == "already_anonymized"
    )

    second_state = (
        privacy_data_service.get_privacy_state(1)
    )

    assert first_state == second_state


def test_other_user_cannot_anonymize_subject():
    reset_privacy_data()

    client = app.test_client()

    response = client.post(
        "/api/users/1/anonymize",
        headers={
            "X-User-Id": "2"
        }
    )

    assert response.status_code == 404

    assert response.get_json() == {
        "error": "not_found"
    }

    state = client.get(
        "/api/users/1/privacy-state",
        headers={
            "X-User-Id": "1"
        }
    )

    state_data = state.get_json()

    assert state_data["user"]["name"] == "Olena Test"

    assert (
        state_data["user"]["email"]
        == "olena.test@example.com"
    )


def test_anonymization_rolls_back_on_failure():
    reset_privacy_data()

    before = (
        privacy_data_service.get_privacy_state(1)
    )

    result, status_code = (
        privacy_data_service.anonymize_user(
            actor_id=1,
            subject_id=1,
            correlation_id="rollback-test-001",
            simulate_failure=True
        )
    )

    assert status_code == 500

    assert result == {
        "status": "failed",
        "subject_id": 1
    }

    after = (
        privacy_data_service.get_privacy_state(1)
    )

    assert after == before

    assert (
        privacy_data_service.audit_events
        == []
    )

    assert (
        after["user"]["name"]
        == "Olena Test"
    )

    assert (
        after["user"]["email"]
        == "olena.test@example.com"
    )

    assert (
        after["user"]["phone"]
        == "+380501234567"
    )

    assert (
        after["settings"]
        == {
            "language": "uk",
            "theme": "dark"
        }
    )

    assert len(
        after["business_records"]
    ) == 1
