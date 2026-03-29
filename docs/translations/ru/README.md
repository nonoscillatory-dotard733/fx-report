<!-- Copyright (c) 2026 s0llarr -->

# fx-report

`fx-report` — небольшая Python-библиотека и CLI для генерации Markdown-отчётов по FX-курсам из подключаемого источника данных.

## Для чего нужен проект

Пакет преобразует временной ряд FX в читаемый Markdown-отчёт. Он полезен, когда нужен стабильный формат отчёта, простая командная точка входа или библиотечный интерфейс для встроенной автоматизации.

Ключевые возможности:

- API, ориентированный на библиотечное использование, с небольшим сервисным слоем;
- CLI для генерации отчёта одной командой;
- расширяемые протоколы для собственных провайдеров данных;
- автоматический текстовый отчёт об ошибке при сбое генерации;
- HTTP/session-абстракция, удобная для тестов.

## Установка и быстрый старт

Подробные инструкции находятся в [docs/translations/ru/installation.md](installation.md) и [docs/translations/ru/usage.md](usage.md).

Минимальный локальный запуск:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]

fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

Параметр `--days` задаёт, сколько торговых дней показывать в отчёте. Рендерер автоматически добавляет одну дополнительную точку для сравнения, чтобы последний день можно было сравнить с предыдущим торговым днём.

## Минимальный пример использования библиотеки

Пример использует собственный провайдер, строит отчёт и записывает его на диск.

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

Подробности см. в [docs/translations/ru/api.md](api.md) и [docs/translations/ru/tests.md](tests.md).

## Лицензия

Проект распространяется по лицензии MIT. Полный текст находится в [LICENSE](../../../LICENSE).
