<!-- Copyright (c) 2026 s0llarr -->

# fx-report

Main translations: [Russian README](docs/translations/ru/README.md) and the translated docs in [docs/translations/ru/](docs/translations/ru/).

`fx-report` is a small Python library and CLI for generating Markdown FX reports from a pluggable data source. It is designed for repeatable daily snapshots, automated publishing, and simple reuse inside other Python projects.

## What this project solves

The package turns an FX time-series source into a readable Markdown report. It is useful when you need a stable report format, a simple command-line entry point, or a library interface that can be wired into a custom pipeline.

Key capabilities:

- library-first API with a small service layer;
- CLI for one-command report generation;
- protocol-based extension points for custom data providers;
- automatic error report output when generation fails;
- test-friendly HTTP/session abstraction.

## Installation and quick start

The setup and usage guides are in [docs/installation.md](docs/installation.md) and [docs/usage.md](docs/usage.md).

A minimal local setup looks like this:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]

fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

The `--days` value controls how many trading days are shown in the report. The renderer automatically keeps one extra comparison point so the latest day can be compared against the previous trading day.

## Minimal library example

This example uses a custom provider, renders a report, and writes it to disk.

```python
from pathlib import Path

from fx_report import ReportRequest, ReportService, SeriesResult


class StaticProvider:
    def fetch_series(self, base, quotes, days):
        return SeriesResult(
            dates=("2026-03-26", "2026-03-27"),
            data={
                "2026-03-26": {"USD": 1.0832, "GBP": 0.8371, "CHF": 0.9614},
                "2026-03-27": {"USD": 1.0874, "GBP": 0.8394, "CHF": 0.9641},
            },
            source="Static sample data",
        )


service = ReportService(provider=StaticProvider())
request = ReportRequest(
    base="EUR",
    quotes=("USD", "GBP", "CHF"),
    days=1,
    output=Path("output/fx_report.md"),
    error_output=Path("output/fx_report_error.md"),
)

report = service.build_report(request)
service.save_report(request.output, report)
print(report)
```

More details are in [docs/api.md](docs/api.md) and [docs/tests.md](docs/tests.md).

## License

This project is licensed under the MIT License. The full text is in [LICENSE](LICENSE).
