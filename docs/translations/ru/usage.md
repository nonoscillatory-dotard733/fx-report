<!-- Copyright (c) 2026 s0llarr -->

# Использование

## Командная строка

Самый быстрый способ получить отчёт:

```bash
fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

Полезные параметры:

- `--base`: базовая валюта, по умолчанию `EUR`;
- `--quotes`: список котируемых валют через запятую;
- `--days`: число торговых дней, отображаемых в отчёте;
- `--output`: путь к основному Markdown-отчёту;
- `--error-output`: необязательный путь для отчёта об ошибке;
- `--default-error-output`: записывать error-report в путь по умолчанию.

Файл отчёта по умолчанию — `output/fx_report.md`. При сбое основной отчёт остаётся без изменений, а вместо него может быть записан `output/fx_report_error.md`.

## Использование как библиотеки

Для программного использования создайте `ReportRequest` и вызовите `run(...)` или `ReportService` напрямую:

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

Слой сервиса удобен, когда нужно подставить собственный источник данных или переиспользовать рендеринг в другом приложении.

## Формат результата

Сгенерированный отчёт содержит:

- заголовок с базовой валютой;
- сводную таблицу для последнего видимого торгового дня;
- таблицу дневного ряда за запрошенное окно;
- краткую секцию с источником данных.

Отчёт об ошибке содержит параметры запроса и сообщение о сбое, поэтому он подходит для CI-логов и плановых запусков.

Далее см. [docs/translations/ru/api.md](api.md) и [docs/translations/ru/tests.md](tests.md).
