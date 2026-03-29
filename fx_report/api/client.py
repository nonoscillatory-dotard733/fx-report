# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Frankfurter API client implementation."""


from __future__ import annotations

from collections import OrderedDict
from collections.abc import Sequence
from datetime import date, timedelta
from typing import Any

from fx_report.config import API_URL, LOOKBACK_PADDING_DAYS, REQUEST_TIMEOUT_S
from fx_report.errors import DataFetchError
from fx_report.models import FXSeries, SeriesResult
from fx_report.protocols import HttpSession, SeriesProvider


class FrankfurterClient(SeriesProvider):
    """Fetch FX time series from the Frankfurter API.

    The client accepts a custom HTTP session for tests or alternative request
    implementations. When no session is provided, a `requests.Session` object
    is created lazily.

    The requested window is treated as the number of report days to display.
    One extra data point is fetched automatically so the renderer can compare
    the latest visible day against the previous trading day, including the
    `--days 1` workflow.
    """

    def __init__(
        self,
        session: HttpSession | None = None,
        api_url: str = API_URL,
        timeout_s: int = REQUEST_TIMEOUT_S,
    ) -> None:
        self._session = session
        self._api_url = api_url
        self._timeout_s = timeout_s

    def fetch_series(
        self,
        base: str,
        quotes: Sequence[str],
        days: int,
    ) -> SeriesResult:
        """Fetch and normalize the requested FX history window."""
        session = self._session or self._default_session()

        end = date.today()
        start = end - timedelta(days=days + LOOKBACK_PADDING_DAYS + 1)
        params = self._build_params(start, end, base, list(quotes))

        try:
            response = session.get(
                self._api_url,
                params=params,
                timeout=self._timeout_s,
            )
            response.raise_for_status()

            data = self._parse_payload(response.json())
            dates = sorted(data)

            if len(dates) < 2:
                raise DataFetchError("API returned too few data points.")

            window = max(days + 1, 2)
            return SeriesResult(tuple(dates[-window:]), data, "Frankfurter API")
        except DataFetchError:
            raise
        except Exception as exc:  # pragma: no cover - defensive wrapper
            raise DataFetchError(
                "Unable to fetch FX data from Frankfurter API."
            ) from exc

    def _default_session(self) -> HttpSession:
        """Create the default requests session only when it is actually needed."""
        import requests

        return requests.Session()

    def _build_params(
        self,
        start: date,
        end: date,
        base: str,
        quotes: list[str],
    ) -> dict[str, str]:
        """Build the query string expected by the Frankfurter endpoint."""
        return {
            "from": start.isoformat(),
            "to": end.isoformat(),
            "quotes": ",".join(quotes),
            "base": base,
        }

    def _parse_payload(self, payload: Any) -> FXSeries:
        """Convert a flat list of API rows into the nested FX series format."""
        series: FXSeries = OrderedDict()
        for row in payload:
            series.setdefault(row["date"], {})[row["quote"]] = float(row["rate"])

        return series
