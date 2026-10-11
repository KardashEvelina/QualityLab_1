from app import app


def test_export_own_personal_data():
    client = app.test_client()

    response = client.get(
        "/api/users/1/personal-data",
        headers={
            "X-User-Id": "1"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["subject_id"] == 1
    assert data["schema_version"] == "1.0"

    assert "profile" in data
    assert "settings" in data
    assert "activity" in data
    assert "consents" in data

    assert data["profile"]["name"] == "Olena Test"
    assert data["profile"]["email"] == "olena.test@example.com"

    assert data["settings"]["language"] == "uk"

    assert len(data["activity"]) >= 1
    assert len(data["consents"]) >= 1


def test_export_excludes_security_sensitive_fields():
    client = app.test_client()

    response = client.get(
        "/api/users/1/personal-data",
        headers={
            "X-User-Id": "1"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    response_text = response.get_data(
        as_text=True
    )

    assert "password_hash" not in data["profile"]
    assert "reset_token" not in data["profile"]
    assert "internal_security_flag" not in data["profile"]

    assert "password_hash" not in response_text
    assert "reset_token" not in response_text
    assert "internal_security_flag" not in response_text


def test_export_other_user_is_denied():
    client = app.test_client()

    response = client.get(
        "/api/users/1/personal-data",
        headers={
            "X-User-Id": "2"
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data == {
        "error": "not_found"
    }

    response_text = response.get_data(
        as_text=True
    )

    assert "Olena Test" not in response_text
    assert "olena.test@example.com" not in response_text


def test_export_nonexistent_user_returns_not_found():
    client = app.test_client()

    response = client.get(
        "/api/users/999/personal-data",
        headers={
            "X-User-Id": "999"
        }
    )

    assert response.status_code == 404

    assert response.get_json() == {
        "error": "not_found"
    }
