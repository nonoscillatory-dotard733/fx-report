# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for application orchestration."""


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from fx_report.app import run
from fx_report.errors import DataFetchError
from fx_report.models import ReportRequest
from fx_report.protocols import ReportWorkflow


@dataclass
class SuccessWorkflow(ReportWorkflow):
    saved: list[tuple[Path, str]] = field(default_factory=list)

    def build_report(self, request: ReportRequest) -> str:
        return "# demo report\n"

    def build_error_report(self, request: ReportRequest, message: str) -> str:
        return f"# error report\n{message}\n"

    def save_report(self, path: Path, content: str) -> None:
        self.saved.append((path, content))

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@dataclass
class FailingWorkflow(SuccessWorkflow):
    def build_report(self, request: ReportRequest) -> str:
        raise DataFetchError("network down")


def test_run_saves_report(tmp_path: Path) -> None:
    output = tmp_path / "report.md"
    request = ReportRequest(
        base="EUR",
        quotes=("USD",),
        days=2,
        output=output,
    )
    workflow = SuccessWorkflow()

    result = run(request, service=workflow)

    assert result.ok is True
    assert output.read_text(encoding="utf-8") == "# demo report\n"
    assert workflow.saved[0][0] == output


def test_run_preserves_existing_report_on_error(
    tmp_path: Path,
) -> None:
    output = tmp_path / "report.md"
    error_output = tmp_path / "error.md"
    output.write_text("keep me", encoding="utf-8")

    request = ReportRequest(
        base="EUR",
        quotes=("USD",),
        days=2,
        output=output,
        error_output=error_output,
    )
    workflow = FailingWorkflow()

    result = run(request, service=workflow)

    assert result.ok is False
    assert output.read_text(encoding="utf-8") == "keep me"
    assert error_output.read_text(encoding="utf-8").startswith(
        "# error report"
    )
