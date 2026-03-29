<!-- Copyright (c) 2026 s0llarr -->

# Установка

`fx-report` рассчитан на Python 3.11+ и использует небольшой набор зависимостей.

## Установка для локальной разработки

Проект пока не опубликован на PyPI, поэтому самый простой вариант — editable-установка из исходников:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

Такой способ даёт:

- команду `fx-report`;
- сам пакет для импорта из Python-кода;
- тестовую зависимость `pytest`.

## Установка только runtime-зависимости

Если нужен только библиотечный или CLI-вариант, установите runtime-зависимость напрямую:

```bash
pip install requests
pip install -e .
```

`requests` — единственная сторонняя зависимость, которую использует встроенный клиент Frankfurter API.

## Проверка установки

Проверьте CLI через справку или короткий запуск отчёта:

```bash
fx-report --help
fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

Команда записывает отчёт в `output/fx_report.md` и при ошибке может дополнительно сохранить отдельный error-report.

Полный сценарий использования описан в [docs/translations/ru/usage.md](usage.md).
