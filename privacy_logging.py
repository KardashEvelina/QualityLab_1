import json
import logging
import re


SENSITIVE_KEYS = {
    "password",
    "password_hash",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "session_secret",
    "reset_token",
}


def mask_email(value):
    if not isinstance(value, str) or "@" not in value:
        return value

    local, domain = value.split("@", 1)

    if len(local) <= 2:
        masked_local = "*" * len(local)
    else:
        masked_local = local[0] + "***" + local[-1]

    return f"{masked_local}@{domain}"


def mask_phone(value):
    if not isinstance(value, str):
        return value

    digits = re.sub(r"\D", "", value)

    if len(digits) < 4:
        return "*" * len(value)

    return f"***{digits[-4:]}"


def sanitize_value(key, value):
    normalized_key = key.lower()

    if normalized_key in SENSITIVE_KEYS:
        return "[REDACTED]"

    if normalized_key == "email":
        return mask_email(value)

    if normalized_key == "phone":
        return mask_phone(value)

    # Контрольоване розширення для FAIL-стану ЛР6
    if normalized_key == "audit_region":
        return str(value).upper()

    if normalized_key == "audit_tier":
        return str(value).lower()

    if normalized_key == "audit_channel":
        return str(value).lower()

    if normalized_key == "audit_zone":
        return str(value).strip()

    if normalized_key == "audit_group":
        return str(value).lower()

    if normalized_key == "audit_mode":
        return str(value).lower()

    if normalized_key == "audit_level":
        return str(value).upper()

    if normalized_key == "audit_scope":
        return str(value).strip()

    if isinstance(value, dict):
        return sanitize_mapping(value)

    if isinstance(value, list):
        return [
            sanitize_mapping(item)
            if isinstance(item, dict)
            else item
            for item in value
        ]

    return value

def sanitize_mapping(data):
    return {
        key: sanitize_value(key, value)
        for key, value in data.items()
    }


def sanitize_text(message):
    message = re.sub(
        r"([\w\.-]+)@([\w\.-]+)",
        lambda match: mask_email(match.group(0)),
        message
    )

    message = re.sub(
        r"\+?\d[\d\s\-()]{8,}\d",
        lambda match: mask_phone(match.group(0)),
        message
    )

    message = re.sub(
        r"(?i)"
        r"(password|password_hash|token|access_token|"
        r"refresh_token|api_key|session_secret|reset_token)"
        r"=([^\s,;]+)",
        r"\1=[REDACTED]",
        message
    )

    return message


class PrivacyLogFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, dict):
            record.msg = json.dumps(
                sanitize_mapping(record.msg),
                ensure_ascii=False
            )
            record.args = ()
            return True

        record.msg = sanitize_text(str(record.msg))

        if record.args:
            record.args = tuple(
                sanitize_text(str(arg))
                for arg in record.args
            )

        return True


def configure_privacy_logging(logger, stream=None):
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)

    handler.setFormatter(
        logging.Formatter(
            "%(levelname)s %(message)s"
        )
    )

    handler.addFilter(
        PrivacyLogFilter()
    )

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger
