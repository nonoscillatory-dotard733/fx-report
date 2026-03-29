# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for Markdown rendering."""


from pathlib import Path

from fx_report.models import ReportRequest, SeriesResult
from fx_report.report.markdown import (
    build_error_markdown,
    build_markdown,
    render_table,
)


DATA = {
    "2026-03-25": { "USD": 1.0855, "GBP": 0.8378 },
    "2026-03-26": { "USD": 1.0861, "GBP": 0.8385 },
}


def test_render_table_shapes_rows() -> None:
    table = render_table(
        ["A", "B"],
        [["1", "2"], ["100", "200"]],
    )

    assert "| A   | B   |" in table
    assert "| 100 | 200 |" in table


def test_build_markdown_contains_sections() -> None:
    request = ReportRequest(
        base="EUR",
        quotes=("USD", "GBP"),
        days=2,
        output=Path("report.md"),
    )
    result = SeriesResult(
        dates=("2026-03-25", "2026-03-26"),
        data=DATA,
        source="Frankfurter API",
    )

    report = build_markdown(request, result)

    assert "# Daily FX Snapshot Report (EUR)" in report
    assert "## Summary" in report
    assert "## Daily Series" in report
    assert "Frankfurter API" in report


def test_build_markdown_supports_single_day_window() -> None:
    request = ReportRequest(
        base="EUR",
        quotes=("USD", "GBP"),
        days=1,
        output=Path("report.md"),
    )
    result = SeriesResult(
        dates=("2026-03-25", "2026-03-26"),
        data=DATA,
        source="Frankfurter API",
    )

    report = build_markdown(request, result)

    assert "- **Window:** 1 day" in report
    assert "2026-03-26" in report
    assert "2026-03-25" not in report.split("## Daily Series", 1)[1]


def test_build_error_markdown_mentions_problem() -> None:
    request = ReportRequest(
        base="EUR",
        quotes=("USD",),
        days=2,
        output=Path("report.md"),
    )

    report = build_error_markdown(request, "network error")

    assert "FX Snapshot Report - Error" in report
    assert "network error" in report
    assert "The existing report file was left unchanged." in report
