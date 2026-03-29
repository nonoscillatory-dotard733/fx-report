<!-- Copyright (c) 2026 s0llarr -->

# Tests

The project uses `pytest`.

## Run the full suite

```bash
pytest
```

## Run a focused subset

```bash
pytest tests/test_service.py
pytest tests/test_cli.py
```

The tests cover:

- CLI parsing and exit codes;
- orchestration and error handling;
- provider abstraction;
- Markdown rendering helpers;
- HTTP client behavior.

## Notes for contributors

The repository is designed so the public API can be tested without real network calls. Custom providers, sessions, and workflows can be substituted directly in tests.

For the package surface and extension points, see [docs/api.md](docs/api.md).
