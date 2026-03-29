# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for formatting helpers."""


from fx_report.utils.formatting import (
    format_pct,
    format_rate,
    normalize_quotes,
    pct_change,
)


def test_pct_change_handles_zero_previous() -> None:
    assert pct_change(10.0, 0.0) == 0.0


def test_pct_change_calculates_change() -> None:
    assert pct_change(110.0, 100.0) == 0.1


def test_formatters_are_stable() -> None:
    assert format_rate(1.23456) == "1.2346"
    assert format_pct(0.1234) == "+12.34%"


def test_normalize_quotes_preserves_order() -> None:
    assert normalize_quotes("usd, gbp, , chf") == ("USD", "GBP", "CHF")
