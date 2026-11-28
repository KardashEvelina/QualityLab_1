import sys

import requests


EXTERNAL_SERVICE_URL = "http://127.0.0.1:5001/external/status"
TIMEOUT_SECONDS = 1


def check_external_dependency():
    """Перевіряє доступність зовнішнього сервісу."""
    try:
        response = requests.get(
            EXTERNAL_SERVICE_URL,
            params={"mode": "normal"},
            timeout=TIMEOUT_SECONDS,
        )

        if response.ok:
            print("EXTERNAL DEPENDENCY: AVAILABLE")
            print("HTTP:", response.status_code)
            return True

        print("EXTERNAL DEPENDENCY: UNHEALTHY")
        print("HTTP:", response.status_code)
        return False

    except requests.RequestException as error:
        print("EXTERNAL DEPENDENCY: UNAVAILABLE")
        print("ERROR:", error)
        return False


if __name__ == "__main__":
    sys.exit(
        0 if check_external_dependency() else 1
    )
