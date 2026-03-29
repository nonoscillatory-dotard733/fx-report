# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Typed data structures used by the report pipeline."""


from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

FXSeries: TypeAlias = dict[str, dict[str, float]]
"""Mapping of date -> quote -> exchange rate."""


@dataclass(frozen=True, slots=True)
class SeriesResult:
    """Normalized FX time series returned by a provider."""

    dates: tuple[str, ...]
    data: FXSeries
    source: str


@dataclass(frozen=True, slots=True)
class ReportRequest:
    """Parameters describing one report build."""

    base: str
    quotes: tuple[str, ...]
    days: int
    output: Path
    error_output: Path | None = None


@dataclass(frozen=True, slots=True)
class RunResult:
    """Outcome of one CLI or library run."""

    ok: bool
    message: str
    output: Path | None = None
    error_output: Path | None = None
