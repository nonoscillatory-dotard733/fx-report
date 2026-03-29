<!-- Copyright (c) 2026 s0llarr -->

# Installation

`fx-report` targets Python 3.11+ and uses a very small runtime dependency set.

## Install for local development

The project is not published to PyPI yet, so the easiest setup is an editable install from a checkout:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

The editable install gives you:

- the `fx-report` command;
- the package itself for imports in Python code;
- the test dependency `pytest`.

## Install only the runtime dependency

When you only need the library or CLI, install the runtime requirement directly:

```bash
pip install requests
pip install -e .
```

`requests` is the only third-party dependency used by the built-in Frankfurter API client.

## Verify the installation

Run the CLI help or a tiny report command:

```bash
fx-report --help
fx-report --base EUR --quotes USD,GBP,CHF --days 1 --output output/fx_report.md
```

The command writes the report to `output/fx_report.md` and, on failure, can also write a separate error report.

For the full usage flow, continue with [docs/usage.md](docs/usage.md).
