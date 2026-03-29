# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Protocols that describe the package extension points."""


from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Protocol, TypeAlias

from fx_report.models import ReportRequest, SeriesResult

JsonList: TypeAlias = list[dict[str, Any]]
"""JSON payload shape expected from the built-in HTTP client."""


class HttpResponse(Protocol):
    """Minimal response interface accepted by :class:`FrankfurterClient`."""

    def raise_for_status(self) -> None:
        """Raise an exception when the response is not successful."""
        ...

    def json(self) -> JsonList:
        """Return a decoded JSON payload."""
        ...


class HttpSession(Protocol):
    """Minimal session interface accepted by :class:`FrankfurterClient`."""

    def get(
        self,
        url: str,
        *,
        params: Mapping[str, str],
        timeout: float | int,
    ) -> HttpResponse:
        """Execute one HTTP GET request and return a response object."""
        ...


class SeriesProvider(Protocol):
    """Object capable of returning a normalized FX series."""

    def fetch_series(
        self,
        base: str,
        quotes: Sequence[str],
        days: int,
    ) -> SeriesResult:
        """Fetch the requested series for the given window."""
        ...


class ReportWorkflow(Protocol):
    """High-level workflow used by the CLI and :func:`fx_report.run`."""

    def build_report(self, request: ReportRequest) -> str:
        """Render the primary Markdown report."""
        ...

    def build_error_report(self, request: ReportRequest, message: str) -> str:
        """Render a Markdown report describing the failure."""
        ...

    def save_report(self, path: Path, content: str) -> None:
        """Persist rendered Markdown to disk."""
        ...
