import requests


EXTERNAL_SERVICE_URL = "http://127.0.0.1:5001/external/status"


def get_external_status(mode="normal"):
    response = requests.get(
        EXTERNAL_SERVICE_URL,
        params={"mode": mode},
        timeout=2
    )

    response.raise_for_status()

    return response.json()