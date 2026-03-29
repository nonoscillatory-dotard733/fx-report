# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Project-wide configuration constants."""


from __future__ import annotations

from pathlib import Path
from typing import Final


API_URL: Final = "https://api.frankfurter.dev/v2/rates"
DEFAULT_BASE: Final = "EUR"
DEFAULT_QUOTES: Final = ("USD", "GBP", "CHF", "JPY")
DEFAULT_DAYS: Final = 5
DEFAULT_OUTPUT: Final = Path("output/fx_report.md")
DEFAULT_ERROR_OUTPUT: Final = Path("output/fx_report_error.md")
REQUEST_TIMEOUT_S: Final = 20
LOOKBACK_PADDING_DAYS: Final = 7
