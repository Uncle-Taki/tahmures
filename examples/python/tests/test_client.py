import pytest
from tahmures.client import FixtureClient
from tahmures.types import (
    FixtureRecord,
    GenerationRequest,
    GenerationResponse,
    Message,
)


def test_fixture_client_selects_exact_record() -> None:
    response = GenerationResponse(text="task", model_id="fixture-v1")
    client = FixtureClient((FixtureRecord("case", "explicit", 1, response),))
    request = GenerationRequest(
        messages=(Message("user", "input"),),
        metadata={"case_id": "case", "variant_id": "explicit", "trial": 1},
    )
    assert client.generate(request) == response


def test_fixture_client_rejects_missing_record() -> None:
    client = FixtureClient(())
    request = GenerationRequest(
        messages=(Message("user", "input"),),
        metadata={"case_id": "case", "variant_id": "missing", "trial": 1},
    )
    with pytest.raises(LookupError):
        client.generate(request)
