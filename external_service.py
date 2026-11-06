import logging
import time
from dataclasses import dataclass

import requests


EXTERNAL_SERVICE_URL = "http://127.0.0.1:5001/external/status"

MAX_ATTEMPTS = 3
REQUEST_TIMEOUT = 2
BACKOFF_SECONDS = 0.2

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExternalRequest:
    """Незмінний Value Object параметрів зовнішнього запиту."""

    mode: str
    attempt: int
    url: str = EXTERNAL_SERVICE_URL
    timeout: int = REQUEST_TIMEOUT
    max_attempts: int = MAX_ATTEMPTS


@dataclass(frozen=True, slots=True)
class ExternalStatus:
    """Незмінний Value Object результату зовнішнього сервісу."""

    status: str
    source: str
    attempts: int
    degraded: bool

    @classmethod
    def from_http_response(cls, response, attempt):
        response.raise_for_status()

        payload = response.json()

        return cls(
            status=payload["status"],
            source=payload["source"],
            attempts=attempt,
            degraded=False,
        )

    def to_dict(self):
        return {
            "status": self.status,
            "source": self.source,
            "attempts": self.attempts,
            "degraded": self.degraded,
        }


def _request_external_status(mode, attempt):
    request = ExternalRequest(
        mode=mode,
        attempt=attempt,
    )

    try:
        return ExternalStatus.from_http_response(
            response=requests.get(
                request.url,
                params={"mode": request.mode},
                timeout=request.timeout,
            ),
            attempt=request.attempt,
        ).to_dict()

    except requests.RequestException as error:
        logger.warning(
            "External service request failed. "
            "Attempt %s/%s. Error: %s",
            request.attempt,
            request.max_attempts,
            error,
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
        "degraded": True,
    }


def get_external_status(mode="normal"):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        result = _request_external_status(
            mode,
            attempt,
        )

        if result is not None:
            return result

        _wait_before_retry(attempt)

    return _fallback_response()
