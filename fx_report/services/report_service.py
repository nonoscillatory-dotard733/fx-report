# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Service layer for report generation and persistence."""


from __future__ import annotations

from pathlib import Path

from fx_report.api.client import FrankfurterClient
from fx_report.errors import DataFetchError, ReportWriteError
from fx_report.models import ReportRequest, SeriesResult
from fx_report.protocols import SeriesProvider
from fx_report.report.markdown import build_error_markdown, build_markdown


class ReportService:
    """Coordinate data fetching, validation, rendering, and saving."""

    def __init__(self, provider: SeriesProvider | None = None) -> None:
        self._provider = provider or FrankfurterClient()

    def build_report(self, request: ReportRequest) -> str:
        """Fetch FX data, validate the result, and render Markdown."""
        try:
            result = self._provider.fetch_series(
                request.base,
                request.quotes,
                request.days,
            )
        except DataFetchError:
            raise
        except Exception as exc:  # pragma: no cover - defensive wrapper
            raise DataFetchError(str(exc)) from exc

        self._validate_result(result, request)
        return build_markdown(request, result)

    def build_error_report(self, request: ReportRequest, message: str) -> str:
        """Render a Markdown page that explains the failure."""
        return build_error_markdown(request, message)

    def save_report(self, path: Path, content: str) -> None:
        """Persist a rendered report to disk, creating parent directories."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise ReportWriteError(f"Unable to write report: {path}") from exc

    def _validate_result(
        self,
        result: SeriesResult,
        request: ReportRequest,
    ) -> None:
        """Ensure the requested quotes exist in the latest two data points."""
        if len(result.dates) < 2:
            raise DataFetchError("At least two dates are required.")

        latest = result.dates[-1]
        previous = result.dates[-2]

        for quote in request.quotes:
            if quote not in result.data.get(latest, {}):
                raise DataFetchError(f"Missing {quote} in the latest series.")

            if quote not in result.data.get(previous, {}):
                raise DataFetchError(f"Missing {quote} in the previous series.")
