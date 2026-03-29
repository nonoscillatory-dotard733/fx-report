<!-- Copyright (c) 2026 s0llarr -->

# Usage

## Command-line interface

The CLI is the fastest way to generate a report:

```bash
fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

Useful flags:

- `--base`: base currency, defaults to `EUR`;
- `--quotes`: comma-separated quote list;
- `--days`: number of trading days shown in the report;
- `--output`: path to the main Markdown report;
- `--error-output`: optional path for the error report;
- `--default-error-output`: write the error report to the default path when needed.

The default report file is `output/fx_report.md`. A failed run leaves the main report untouched and can write `output/fx_report_error.md` instead.

## Library usage

For programmatic use, build a `ReportRequest` and call `run(...)` or `ReportService` directly:

```python
from pathlib import Path

from fx_report import ReportRequest, ReportService, run

request = ReportRequest(
    base="EUR",
    quotes=("USD", "GBP", "CHF"),
    days=5,
    output=Path("output/fx_report.md"),
    error_output=Path("output/fx_report_error.md"),
)

result = run(request, service=ReportService())
print(result.ok, result.message)
```

The service layer is the best entry point when you want to inject your own provider or reuse the rendering logic in another application.

## Output format

The generated report contains:

- a title with the base currency;
- a summary table for the latest visible trading day;
- a daily series table for the requested window;
- a short note block with the data source.

The error report contains the request parameters and the failure message, which makes it suitable for CI logs or scheduled runs.

Continue with [docs/api.md](docs/api.md) for the public surface and [docs/tests.md](docs/tests.md) for verification.
