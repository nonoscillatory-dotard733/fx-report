# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for the Frankfurter API client."""


from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import pytest

from fx_report.api.client import FrankfurterClient
from fx_report.errors import DataFetchError
from fx_report.protocols import HttpResponse, HttpSession, JsonList


@dataclass
class DummyResponse(HttpResponse):
    payload: JsonList

    def raise_for_status(self) -> None:
        return None

    def json(self) -> JsonList:
        return self.payload


@dataclass
class DummySession(HttpSession):
    payload: JsonList
    calls: JsonList = field(default_factory=list)

    def get(
        self,
        url: str,
        *,
        params: Mapping[str, str],
        timeout: float | int,
    ) -> DummyResponse:
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return DummyResponse(self.payload)


class ErrorSession(HttpSession):
    def get(self, *_args: object, **_kwargs: object) -> HttpResponse:
        raise RuntimeError("boom")


def test_fetch_series_uses_session_protocol() -> None:
    session = DummySession(
        [
            { "date": "2026-03-25", "quote": "USD", "rate": 1.1 },
            { "date": "2026-03-26", "quote": "USD", "rate": 1.2 },
            { "date": "2026-03-25", "quote": "GBP", "rate": 0.8 },
            { "date": "2026-03-26", "quote": "GBP", "rate": 0.81 },
        ]
    )
    client = FrankfurterClient(session=session, api_url="https://example.test")

    result = client.fetch_series("EUR", ["USD", "GBP"], 2)

    assert result.source == "Frankfurter API"
    assert result.dates == ("2026-03-25", "2026-03-26")
    assert result.data["2026-03-26"]["USD"] == 1.2
    assert session.calls[0]["url"] == "https://example.test"
    assert session.calls[0]["params"]["base"] == "EUR"


def test_fetch_series_wraps_session_errors() -> None:
    client = FrankfurterClient(session=ErrorSession())

    with pytest.raises(DataFetchError):
        client.fetch_series("EUR", ["USD"], 2)
