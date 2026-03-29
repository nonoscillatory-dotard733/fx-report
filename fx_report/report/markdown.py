# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Markdown rendering helpers for FX snapshot reports."""


from __future__ import annotations

from collections.abc import Sequence

from fx_report.models import ReportRequest, SeriesResult
from fx_report.utils.formatting import format_pct, format_rate, pct_change


def render_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Render a simple pipe table with aligned columns."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def render_row(values: Sequence[str]) -> str:
        cells = [value.ljust(widths[index]) for index, value in enumerate(values)]
        return f"| {' | '.join(cells)} |"

    separator = f"| {' | '.join('-' * width for width in widths)} |"
    return "\n".join([render_row(headers), separator, *map(render_row, rows)])


def build_markdown(
    request: ReportRequest,
    result: SeriesResult,
) -> str:
    """Build the main report body from a normalized series result.

    The report shows the latest `request.days` trading days and compares the
    newest visible day with the previous available trading day.
    """
    dates = result.dates
    if len(dates) < 2:
        raise ValueError("At least two dates are required to build a report.")
    if request.days < 1:
        raise ValueError("At least one report day is required.")

    visible_dates = dates[-request.days:] if request.days <= len(dates) else dates
    latest = visible_dates[-1]
    previous = visible_dates[-2] if len(visible_dates) > 1 else dates[-2]

    summary_rows: list[list[str]] = []
    for quote in request.quotes:
        current_value = result.data[latest][quote]
        previous_value = result.data[previous][quote]
        delta = current_value - previous_value

        summary_rows.append(
            [
                quote,
                format_rate(current_value),
                format_rate(previous_value),
                f"{delta:+.4f}",
                format_pct(pct_change(current_value, previous_value)),
            ]
        )

    series_rows = [
        [
            day,
            *[format_rate(result.data[day][quote]) for quote in request.quotes],
        ]
        for day in visible_dates
    ]

    report = [
        f"# Daily FX Snapshot Report ({request.base})",
        "",
        f"- **Source:** {result.source}",
        f"- **Latest date:** {latest}",
        f"- **Previous date:** {previous}",
        f"- **Window:** {len(visible_dates)} {'day' if len(visible_dates) == 1 else 'days'}",
        "",
        "## Summary",
        "",
        render_table(
            ["Quote", "Latest", "Previous", "Delta", "Delta %"],
            summary_rows,
        ),
        "",
        "## Daily Series",
        "",
        render_table(["Date", *request.quotes], series_rows),
        "",
        "## Notes",
        "",
        "- The report is generated from a public FX API or a custom provider.",
        "",
    ]
    return "\n".join(report)


def build_error_markdown(
    request: ReportRequest,
    message: str,
) -> str:
    """Build a small Markdown report that explains why generation failed."""
    report = [
        "# FX Snapshot Report - Error",
        "",
        f"- **Base:** {request.base}",
        f"- **Quotes:** {', '.join(request.quotes)}",
        f"- **Days:** {request.days}",
        f"- **Output:** {request.output}",
        "",
        "## Problem",
        "",
        message,
        "",
        "## Notes",
        "",
        "- The existing report file was left unchanged.",
        "- Check network access, API availability, or provider settings.",
        "",
    ]
    return "\n".join(report)
