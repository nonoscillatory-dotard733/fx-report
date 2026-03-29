<!-- Copyright (c) 2026 s0llarr -->

# Справочник API

В этом файле описан публичный интерфейс, экспортируемый из `fx_report`.

## Публичные экспорты

Из корня пакета экспортируются:

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

## Модели данных

### `SeriesResult`

```python
SeriesResult(
    dates: tuple[str, ...],
    data: FXSeries,
    source: str,
)
```

Нормализованный ряд FX, возвращаемый провайдером. `dates` содержит видимое окно отчёта и одну дополнительную точку сравнения, если используется встроенный клиент.

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

Описывает один запуск отчёта.

### `RunResult`

```python
RunResult(
    ok: bool,
    message: str,
    output: Path | None = None,
    error_output: Path | None = None,
)
```

Возвращается `fx_report.app.run(...)`.

## Исключения

### `FXReportError`

Базовый класс всех ошибок пакета.

### `DataFetchError`

Возникает, когда источник данных не может вернуть пригодные FX-данные.

### `ReportWriteError`

Возникает, когда отчёт не удалось записать на диск.

## Протоколы

### `HttpResponse`

Минимальный интерфейс ответа, который принимает `FrankfurterClient`.

Требуемые методы:

- `raise_for_status() -> None`
- `json() -> JsonList`

### `HttpSession`

Минимальный интерфейс HTTP-сессии, который принимает `FrankfurterClient`.

Требуемый метод:

- `get(url, *, params, timeout) -> HttpResponse`

### `SeriesProvider`

Интерфейс источника FX-данных.

Требуемый метод:

- `fetch_series(base, quotes, days) -> SeriesResult`

### `ReportWorkflow`

Высокоуровневый workflow-интерфейс, который использует CLI и `run(...)`.

Требуемые методы:

- `build_report(request) -> str`
- `build_error_report(request, message) -> str`
- `save_report(path, content) -> None`

## Клиент Frankfurter

### `FrankfurterClient`

```python
FrankfurterClient(
    session: HttpSession | None = None,
    api_url: str = API_URL,
    timeout_s: int = REQUEST_TIMEOUT_S,
)
```

Получает FX-данные из Frankfurter API. Клиент принимает собственную HTTP-сессию, чтобы тесты могли подменять сетевой слой.

## Сервисный слой

### `ReportService`

```python
ReportService(provider: SeriesProvider | None = None)
```

Методы:

- `build_report(request) -> str`
- `build_error_report(request, message) -> str`
- `save_report(path, content) -> None`

`ReportService` — это стандартный слой оркестрации для CLI и библиотечного использования.

## Вспомогательные средства рендеринга

Внутренний Markdown-рендерер находится в `fx_report.report.markdown` и экспортирует:

- `render_table(headers, rows) -> str`
- `build_markdown(request, result) -> str`
- `build_error_markdown(request, message) -> str`

Эти функции полезны для тестов и расширенных интеграций, но публичной точкой входа остаётся `ReportService`.

## Пример расширения

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

Любой объект с совместимым методом `fetch_series(...)` может выступать как провайдер.
