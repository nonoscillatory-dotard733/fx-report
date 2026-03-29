<!-- Copyright (c) 2026 s0llarr -->

# API Reference

This file describes the public surface exported by `fx_report`.

## Public exports

The package root exports:

- `ReportService`
- `FrankfurterClient`
- `ReportRequest`
- `RunResult`
- `SeriesResult`
- `FXSeries`
- `FXReportError`
- `DataFetchError`
- `ReportWriteError`
- `HttpSession`
- `HttpResponse`
- `SeriesProvider`
- `ReportWorkflow`
- `JsonList`
- `run(...)`

## Data models

### `SeriesResult`

```python
SeriesResult(
    dates: tuple[str, ...],
    data: FXSeries,
    source: str,
)
```

Normalized FX time series returned by a provider. `dates` contains the visible reporting window plus one comparison point when the built-in client is used.

### `ReportRequest`

```python
ReportRequest(
    base: str,
    quotes: tuple[str, ...],
    days: int,
    output: Path,
    error_output: Path | None = None,
)
```

Describes one report run.

### `RunResult`

```python
RunResult(
    ok: bool,
    message: str,
    output: Path | None = None,
    error_output: Path | None = None,
)
```

Returned by `fx_report.app.run(...)`.

## Exceptions

### `FXReportError`

Base class for all package-specific failures.

### `DataFetchError`

Raised when the data source cannot provide usable FX data.

### `ReportWriteError`

Raised when a report cannot be written to disk.

## Protocols

### `HttpResponse`

Minimal response interface accepted by `FrankfurterClient`.

Required methods:

- `raise_for_status() -> None`
- `json() -> JsonList`

### `HttpSession`

Minimal session interface accepted by `FrankfurterClient`.

Required method:

- `get(url, *, params, timeout) -> HttpResponse`

### `SeriesProvider`

Provider interface for FX data sources.

Required method:

- `fetch_series(base, quotes, days) -> SeriesResult`

### `ReportWorkflow`

High-level workflow interface used by the CLI and `run(...)`.

Required methods:

- `build_report(request) -> str`
- `build_error_report(request, message) -> str`
- `save_report(path, content) -> None`

## Frankfurter client

### `FrankfurterClient`

```python
FrankfurterClient(
    session: HttpSession | None = None,
    api_url: str = API_URL,
    timeout_s: int = REQUEST_TIMEOUT_S,
)
```

Fetches FX data from the Frankfurter API. The built-in client accepts a custom session object so tests can supply a stubbed HTTP layer.

## Service layer

### `ReportService`

```python
ReportService(provider: SeriesProvider | None = None)
```

Methods:

- `build_report(request) -> str`
- `build_error_report(request, message) -> str`
- `save_report(path, content) -> None`

`ReportService` is the default orchestration layer for the CLI and for library consumers that want a ready-made pipeline.

## Rendering helpers

The internal Markdown renderer lives in `fx_report.report.markdown` and exposes:

- `render_table(headers, rows) -> str`
- `build_markdown(request, result) -> str`
- `build_error_markdown(request, message) -> str`

These helpers are useful for tests or for advanced integrations, but `ReportService` remains the public entry point.

## Extension example

```python
from fx_report import ReportRequest, ReportService, SeriesResult


class MyProvider:
    def fetch_series(self, base, quotes, days):
        return SeriesResult(
            dates=("2026-03-26", "2026-03-27"),
            data={
                "2026-03-26": {"USD": 1.0, "GBP": 0.8},
                "2026-03-27": {"USD": 1.1, "GBP": 0.81},
            },
            source="My API",
        )


service = ReportService(provider=MyProvider())
```

Any object with a compatible `fetch_series(...)` method can act as a provider.
