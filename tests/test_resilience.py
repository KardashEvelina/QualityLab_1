from unittest.mock import Mock, patch

import requests

from external_service import get_external_status


def test_external_service_success():
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "status": "ok",
        "source": "mock_external_service"
    }

    with patch(
        "external_service.requests.get",
        return_value=response
    ) as mock_get:
        result = get_external_status("normal")

    assert result["status"] == "ok"
    assert result["degraded"] is False
    assert result["attempts"] == 1
    assert mock_get.call_count == 1


def test_external_service_fallback_after_retries():
    with patch(
        "external_service.requests.get",
        side_effect=requests.exceptions.HTTPError(
            "500 Server Error"
        )
    ) as mock_get, patch(
        "external_service.time.sleep"
    ) as mock_sleep:
        result = get_external_status("error")

    assert result["status"] == "degraded"
    assert result["source"] == "fallback"
    assert result["degraded"] is True
    assert result["attempts"] == 3

    assert mock_get.call_count == 3
    assert mock_sleep.call_count == 2
