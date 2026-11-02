from unittest.mock import Mock, call, patch

import requests

from external_service import (
    BACKOFF_SECONDS,
    EXTERNAL_SERVICE_URL,
    MAX_ATTEMPTS,
    REQUEST_TIMEOUT,
    _fallback_response,
    _request_external_status,
    _wait_before_retry,
    get_external_status,
)


def test_request_external_status_success():
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "status": "ok",
        "source": "mock_external_service",
    }

    with patch(
        "external_service.requests.get",
        return_value=response,
    ) as mock_get:
        result = _request_external_status("normal", 2)

    mock_get.assert_called_once_with(
        EXTERNAL_SERVICE_URL,
        params={"mode": "normal"},
        timeout=REQUEST_TIMEOUT,
    )

    assert result == {
        "status": "ok",
        "source": "mock_external_service",
        "attempts": 2,
        "degraded": False,
    }


def test_request_external_status_failure():
    error = requests.exceptions.ConnectionError(
        "Connection failed"
    )

    with patch(
        "external_service.requests.get",
        side_effect=error,
    ):
        result = _request_external_status("error", 2)

    assert result is None


def test_wait_before_retry():
    with patch(
        "external_service.time.sleep"
    ) as mock_sleep:
        _wait_before_retry(1)
        _wait_before_retry(2)

    assert mock_sleep.call_args_list == [
        call(BACKOFF_SECONDS),
        call(BACKOFF_SECONDS * 2),
    ]


def test_no_wait_after_last_attempt():
    with patch(
        "external_service.time.sleep"
    ) as mock_sleep:
        _wait_before_retry(MAX_ATTEMPTS)

    mock_sleep.assert_not_called()


def test_fallback_response():
    result = _fallback_response()

    assert result == {
        "status": "degraded",
        "source": "fallback",
        "message": "External service temporarily unavailable",
        "attempts": MAX_ATTEMPTS,
        "degraded": True,
    }


def test_external_service_success():
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "status": "ok",
        "source": "mock_external_service",
    }

    with patch(
        "external_service.requests.get",
        return_value=response,
    ) as mock_get:
        result = get_external_status("normal")

    assert result["status"] == "ok"
    assert result["source"] == "mock_external_service"
    assert result["degraded"] is False
    assert result["attempts"] == 1

    mock_get.assert_called_once_with(
        EXTERNAL_SERVICE_URL,
        params={"mode": "normal"},
        timeout=REQUEST_TIMEOUT,
    )


def test_success_after_retry():
    success = {
        "status": "ok",
        "source": "mock_external_service",
        "attempts": 2,
        "degraded": False,
    }

    with patch(
        "external_service._request_external_status",
        side_effect=[None, success],
    ) as mock_request, patch(
        "external_service._wait_before_retry"
    ) as mock_wait:
        result = get_external_status("normal")

    assert result == success

    assert mock_request.call_args_list == [
        call("normal", 1),
        call("normal", 2),
    ]

    mock_wait.assert_called_once_with(1)


def test_external_service_fallback_after_retries():
    with patch(
        "external_service.requests.get",
        side_effect=requests.exceptions.HTTPError(
            "500 Server Error"
        ),
    ) as mock_get, patch(
        "external_service.time.sleep"
    ) as mock_sleep:
        result = get_external_status("error")

    assert result == {
        "status": "degraded",
        "source": "fallback",
        "message": "External service temporarily unavailable",
        "attempts": MAX_ATTEMPTS,
        "degraded": True,
    }

    assert mock_get.call_count == MAX_ATTEMPTS

    assert mock_sleep.call_args_list == [
        call(BACKOFF_SECONDS),
        call(BACKOFF_SECONDS * 2),
    ]


def test_default_mode_is_normal():
    result_value = {
        "status": "ok",
        "attempts": 1,
        "degraded": False,
    }

    with patch(
        "external_service._request_external_status",
        return_value=result_value,
    ) as mock_request:
        result = get_external_status()

    assert result == result_value
    mock_request.assert_called_once_with(
        "normal",
        1,
    )
