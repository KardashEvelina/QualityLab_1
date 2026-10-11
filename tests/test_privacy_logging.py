import logging
from io import StringIO

from privacy_logging import configure_privacy_logging


def create_test_logger():
    stream = StringIO()

    logger = logging.getLogger(
        "privacy-test"
    )

    configure_privacy_logging(
        logger,
        stream=stream
    )

    return logger, stream


def test_sensitive_values_are_sanitized():
    logger, stream = create_test_logger()

    logger.info({
        "email": "test.user@example.com",
        "phone": "+380501234567",
        "password": "SecretPassword123!",
        "access_token": "synthetic-token"
    })

    output = stream.getvalue()

    assert "test.user@example.com" not in output
    assert "+380501234567" not in output
    assert "SecretPassword123!" not in output
    assert "synthetic-token" not in output

    assert "t***r@example.com" in output
    assert "***4567" in output
    assert "[REDACTED]" in output


def test_nested_and_exception_values_are_sanitized():
    logger, stream = create_test_logger()

    logger.info({
        "profile": {
            "email": "nested.user@example.com",
            "phone": "+380671112233",
            "reset_token": "nested-secret-token"
        }
    })

    try:
        raise ValueError(
            "Failed request for "
            "email=exception.user@example.com "
            "phone=+380931234567 "
            "password=ExceptionPassword123!"
        )

    except ValueError as error:
        logger.error(
            "Operation failed: %s",
            error
        )

    output = stream.getvalue()

    assert "nested.user@example.com" not in output
    assert "+380671112233" not in output
    assert "nested-secret-token" not in output

    assert "exception.user@example.com" not in output
    assert "+380931234567" not in output
    assert "ExceptionPassword123!" not in output

    assert "n***r@example.com" in output
    assert "e***r@example.com" in output
    assert "[REDACTED]" in output
