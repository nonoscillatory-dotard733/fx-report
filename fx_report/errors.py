# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Package-specific exception types."""


from __future__ import annotations


class FXReportError(Exception):
    """Base class for all fx-report failures."""


class DataFetchError(FXReportError):
    """Raised when a provider cannot supply FX data."""


class ReportWriteError(FXReportError):
    """Raised when a report cannot be written to disk."""
