import logging
import time

import requests

EXTERNAL_SERVICE_URL = "http://127.0.0.1:5001/external/status"

MAX_ATTEMPTS = 3
REQUEST_TIMEOUT = 2
BACKOFF_SECONDS = 0.2

logger = logging.getLogger(__name__)


def _request_external_status(mode, attempt):
    try:
        response = requests.get(
            EXTERNAL_SERVICE_URL,
            params={"mode": mode},
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()
        data["attempts"] = attempt
        data["degraded"] = False

        return data

    except requests.RequestException as error:
        logger.warning(
            "External service request failed. "
            "Attempt %s/%s. Error: %s",
            attempt,
            MAX_ATTEMPTS,
            error
        )

        return None


def _wait_before_retry(attempt):
    if attempt < MAX_ATTEMPTS:
        time.sleep(BACKOFF_SECONDS * attempt)


def _fallback_response():
    logger.error(
        "External service is unavailable. "
        "Fallback response is used."
    )

    return {
        "status": "degraded",
        "source": "fallback",
        "message": "External service temporarily unavailable",
        "attempts": MAX_ATTEMPTS,
        "degraded": True
    }


def get_external_status(mode="normal"):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        result = _request_external_status(mode, attempt)

        if result is not None:
            return result

        _wait_before_retry(attempt)

    return _fallback_response()
