# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Small formatting helpers shared by the report renderer."""


from __future__ import annotations

from collections.abc import Sequence


def pct_change(current: float, previous: float) -> float:
    """Return the relative change between two values.

    A zero previous value yields 0.0 instead of a division error because the
    report prefers a stable presentation over a hard failure.
    """
    if previous == 0:
        return 0.0
    return (current - previous) / previous


def format_rate(value: float) -> str:
    """Format an exchange rate with four decimal places."""
    return f"{value:.4f}"


def format_pct(value: float) -> str:
    """Format a relative change as a signed percentage."""
    return f"{value:+.2%}"


def normalize_quotes(raw: str) -> tuple[str, ...]:
    """Normalize a comma-separated quote list into uppercase tokens."""
    quotes = [quote.strip().upper() for quote in raw.split(",")]
    return tuple(quote for quote in quotes if quote)


def rows_to_list(rows: Sequence[Sequence[str]]) -> list[list[str]]:
    """Convert nested sequences into plain lists for easier assertions."""
    return [list(row) for row in rows]
