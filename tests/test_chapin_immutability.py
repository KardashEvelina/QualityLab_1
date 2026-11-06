from dataclasses import FrozenInstanceError

import pytest

from external_service import ExternalRequest, ExternalStatus


def test_external_request_is_immutable():
    request = ExternalRequest(
        mode="normal",
        attempt=1,
    )

    with pytest.raises(FrozenInstanceError):
        request.mode = "error"


def test_external_status_is_immutable():
    status = ExternalStatus(
        status="ok",
        source="mock_external_service",
        attempts=1,
        degraded=False,
    )

    with pytest.raises(FrozenInstanceError):
        status.status = "degraded"


def test_dict_change_does_not_mutate_value_object():
    status = ExternalStatus(
        status="ok",
        source="mock_external_service",
        attempts=1,
        degraded=False,
    )

    result = status.to_dict()
    result["status"] = "degraded"

    assert status.status == "ok"
