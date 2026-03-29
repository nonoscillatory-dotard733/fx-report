# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Public exports for the fx_report package."""


from fx_report.api import FrankfurterClient
from fx_report.app import run
from fx_report.errors import DataFetchError, FXReportError, ReportWriteError
from fx_report.models import FXSeries, ReportRequest, RunResult, SeriesResult
from fx_report.protocols import HttpResponse, HttpSession, JsonList, ReportWorkflow
from fx_report.services import ReportService

__all__ = [
    "DataFetchError",
    "FXReportError",
    "FXSeries",
    "FrankfurterClient",
    "JsonList",
    "HttpResponse",
    "HttpSession",
    "ReportRequest",
    "ReportService",
    "ReportWorkflow",
    "ReportWriteError",
    "RunResult",
    "SeriesResult",
    "run",
]
