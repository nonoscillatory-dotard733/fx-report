# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""High-level application orchestration."""


from __future__ import annotations

import sys

from fx_report.errors import FXReportError
from fx_report.models import ReportRequest, RunResult
from fx_report.protocols import ReportWorkflow
from fx_report.services.report_service import ReportService


def run(
    request: ReportRequest,
    service: ReportWorkflow | None = None,
) -> RunResult:
    """Execute one report build and persist the result.

    The function leaves the primary report untouched if fetching or rendering
    fails. When an error output path is configured, a separate error report is
    written instead.
    """
    workflow = service or ReportService()

    try:
        report = workflow.build_report(request)
        workflow.save_report(request.output, report)
    except FXReportError as exc:
        message = str(exc)
        print(message, file=sys.stderr)

        if request.error_output is None:
            return RunResult(ok=False, message=message)

        try:
            error_report = workflow.build_error_report(request, message)
            workflow.save_report(request.error_output, error_report)
        except FXReportError as error_exc:
            error_message = str(error_exc)
            print(error_message, file=sys.stderr)

            return RunResult(
                ok=False,
                message=error_message,
                error_output=request.error_output,
            )

        return RunResult(
            ok=False,
            message=message,
            error_output=request.error_output,
        )

    return RunResult(
        ok=True,
        message=f"Saved {request.output}",
        output=request.output,
    )
