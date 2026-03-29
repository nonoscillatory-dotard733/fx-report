# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Tests for the command-line interface."""


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from fx_report.cli import main
from fx_report.errors import DataFetchError
from fx_report.models import ReportRequest
from fx_report.protocols import ReportWorkflow


@dataclass
class StubWorkflow(ReportWorkflow):
    report: str = "# demo report\n"
    error_report: str = "# error report\n"
    saved: list[tuple[Path, str]] = field(default_factory=list)

    def build_report(self, request: ReportRequest) -> str:
        return self.report

    def build_error_report(self, request: ReportRequest, message: str) -> str:
        return self.error_report + message

    def save_report(self, path: Path, content: str) -> None:
        self.saved.append((path, content))

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@dataclass
class FailingWorkflow(StubWorkflow):
    def build_report(self, request: ReportRequest) -> str:
        raise DataFetchError("service unavailable")


def test_cli_writes_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StubWorkflow()
    output = tmp_path / "fx.md"

    exit_code = main(
        [
            "--base", "eur",
            "--quotes", "usd,gbp",
            "--days", "2",
            "--output", str(output),
        ],
        service=service,
    )

    assert exit_code == 0
    assert output.read_text(encoding="utf-8") == "# demo report\n"
    assert "Saved" in capsys.readouterr().out


def test_cli_writes_error_report_and_keeps_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = FailingWorkflow()
    output = tmp_path / "fx.md"
    error_output = tmp_path / "fx_error.md"
    output.write_text("keep", encoding="utf-8")

    exit_code = main(
        [
            "--base", "eur",
            "--quotes", "usd",
            "--days", "2",
            "--output", str(output),
            "--error-output", str(error_output),
        ],
        service=service,
    )

    captured = capsys.readouterr()

    assert exit_code == 1
    assert output.read_text(encoding="utf-8") == "keep"
    assert error_output.exists()
    assert "service unavailable" in captured.err
