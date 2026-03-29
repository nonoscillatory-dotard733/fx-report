# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for the report service."""


from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import pytest

from fx_report.errors import DataFetchError
from fx_report.models import ReportRequest, SeriesResult
from fx_report.protocols import SeriesProvider
from fx_report.services.report_service import ReportService


@dataclass
class StubProvider(SeriesProvider):
    result: SeriesResult
    calls: list[tuple[str, tuple[str, ...], int]]

    def fetch_series(
        self,
        base: str,
        quotes: Sequence[str],
        days: int,
    ) -> SeriesResult:
        self.calls.append((base, tuple(quotes), days))
        return self.result


@dataclass
class BrokenProvider(SeriesProvider):
    def fetch_series(
        self,
        base: str,
        quotes: Sequence[str],
        days: int,
    ) -> SeriesResult:
        raise DataFetchError("offline")


def test_service_builds_report_from_protocol_provider() -> None:
    provider = StubProvider(
        SeriesResult(
            dates=("2026-03-25", "2026-03-26"),
            data={
                "2026-03-25": { "USD": 1.0, "GBP": 0.8 },
                "2026-03-26": { "USD": 1.1, "GBP": 0.81 },
            },
            source="Custom API",
        ),
        calls=[],
    )
    service = ReportService(provider=provider)
    request = ReportRequest(
        base="EUR",
        quotes=("USD", "GBP"),
        days=2,
        output=Path("report.md"),
    )

    report = service.build_report(request)

    assert provider.calls == [("EUR", ("USD", "GBP"), 2)]
    assert "Daily FX Snapshot Report (EUR)" in report
    assert "Custom API" in report
    assert "1.1000" in report


def test_service_saves_report(tmp_path: Path) -> None:
    service = ReportService(provider=BrokenProvider())
    target = tmp_path / "report.md"

    service.save_report(target, "hello")

    assert target.read_text(encoding="utf-8") == "hello"


def test_service_rejects_incomplete_series() -> None:
    provider = StubProvider(
        SeriesResult(
            dates=("2026-03-26",),
            data={ "2026-03-26": { "USD": 1.0 } },
            source="Custom API",
        ),
        calls=[],
    )
    service = ReportService(provider=provider)
    request = ReportRequest(
        base="EUR",
        quotes=("USD",),
        days=1,
        output=Path("report.md"),
    )

    with pytest.raises(DataFetchError):
        service.build_report(request)
