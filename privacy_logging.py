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


def _identity(value):
    return value


def _redact(value):
    return "[REDACTED]"


def _upper_text(value):
    return str(value).upper()


def _lower_text(value):
    return str(value).lower()


def _strip_text(value):
    return str(value).strip()


def sanitize_mapping(data):
    return {
        key: sanitize_value(key, value)
        for key, value in data.items()
    }


def _sanitize_list(values):
    item_handlers = {
        dict: sanitize_mapping,
    }

    return [
        item_handlers.get(
            type(item),
            _identity
        )(item)
        for item in values
    ]


KEY_HANDLERS = {
    **{
        key: _redact
        for key in SENSITIVE_KEYS
    },
    "email": mask_email,
    "phone": mask_phone,
    "audit_region": _upper_text,
    "audit_tier": _lower_text,
    "audit_channel": _lower_text,
    "audit_zone": _strip_text,
    "audit_group": _lower_text,
    "audit_mode": _lower_text,
    "audit_level": _upper_text,
    "audit_scope": _strip_text,
}


TYPE_HANDLERS = {
    dict: sanitize_mapping,
    list: _sanitize_list,
}


def sanitize_value(key, value):
    normalized_key = key.lower()

    handler = KEY_HANDLERS.get(
        normalized_key,
        TYPE_HANDLERS.get(
            type(value),
            _identity
        )
    )

    return handler(value)

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
