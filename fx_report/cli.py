# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.

"""Command-line interface for fx-report."""


from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from fx_report.app import run
from fx_report.config import (
    DEFAULT_BASE,
    DEFAULT_DAYS,
    DEFAULT_ERROR_OUTPUT,
    DEFAULT_OUTPUT,
    DEFAULT_QUOTES,
)
from fx_report.models import ReportRequest
from fx_report.protocols import ReportWorkflow
from fx_report.services.report_service import ReportService
from fx_report.utils.formatting import normalize_quotes


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for report generation."""
    parser = argparse.ArgumentParser(
        description="Generate a Markdown FX snapshot report.",
    )

    parser.add_argument("--base", default=DEFAULT_BASE)
    parser.add_argument("--quotes", default=",".join(DEFAULT_QUOTES))
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--error-output", type=Path, default=None)
    parser.add_argument(
        "--default-error-output",
        action="store_true",
        help="Write an error report to the default path when needed.",
    )
    return parser.parse_args(argv)


def build_request(args: argparse.Namespace) -> ReportRequest:
    """Convert parsed CLI arguments into a typed request object."""
    error_output = args.error_output
    if args.default_error_output and error_output is None:
        error_output = DEFAULT_ERROR_OUTPUT

    return ReportRequest(
        base=args.base.upper(),
        quotes=normalize_quotes(args.quotes),
        days=args.days,
        output=args.output,
        error_output=error_output,
    )


def main(
    argv: Sequence[str] | None = None,
    service: ReportWorkflow | None = None,
) -> int:
    """Run the CLI and return a shell-friendly exit code."""
    args = parse_args(argv)
    request = build_request(args)
    result = run(request, service=service or ReportService())

    if result.ok:
        print(result.message)
        return 0

    if result.error_output is not None:
        print(f"Error report saved to {result.error_output}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
