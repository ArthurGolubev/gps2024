# AGENTS.md

## Build / Lint / Test Commands

This repository uses **Poetry** to manage dependencies and virtual environments.

| Task | Command | Notes |
|------|---------|-------|
| Install dependencies | `poetry install` | Creates a virtual env and installs all `tool.poetry.dependencies` and `tool.poetry.group.dev.dependencies`. |
| Run tests (all) | `poetry run pytest` | Executes the test suite using **pytest**. If you only have a single test to run, specify it directly: `poetry run pytest tests/test_example.py::test_foo`. |
| Run a single test | `poetry run pytest path/to/file.py::test_name` | Replace `path/to/file.py` with the relative path from the repository root and `test_name` with the test function or method. |
| Lint & format | `poetry run black .` and `poetry run isort .` | These commands enforce code style and import ordering.
| Static type checking | `poetry run mypy src` | Verify that the project passes type checks. (`mypy` is recommended to be added to `tool.poetry.group.dev.dependencies`). |
| Run the main script | `poetry run python -m main` | For quick experimentation. |
|

> **Tip**: If you want to run the application in a different environment (e.g., Docker), ensure you use the same `pyproject.toml` configuration.

## Code Style Guidelines

All contributors should adhere to the following style rules to keep the codebase clean, consistent, and type‑safe.

### 1. Imports

* Group imports in the following order: **standard-library**, **third‑party**, **local**.
* Keep each group separated by a single empty line.
* Sort each group alphabetically.
* Use absolute imports wherever possible.
* Avoid `from x import *`.
* Example:

```python
# Good
import os
import sys

import httpx
import requests

from schemas import ProtocolSchema
```

### 2. Formatting

* Use **Black** with the default configuration (`line-length = 88`).
* Use **isort** to keep imports tidy.
* No trailing whitespace.
* Functions and classes should end with a single newline.

### 3. Naming Conventions

| Symbol | Pattern | Example |
|--------|---------|---------|
| Variables / attributes | snake_case | `protocol_list`, `file_path` |
| Functions | snake_case | `download_protocols()` |
| Classes / Dataclasses | PascalCase | `Competition`, `ProtocolSchema` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT` |
| Type hints | PEP 604 where appropriate | `list[int]` |
| Generic type names | `T`, `K`, `V` | `T_co` |

### 4. Type Usage

* Prefer Pydantic `BaseModel` for data validation.
* Provide explicit type hints for all public functions and methods.
* Use `Optional[T]` when a value can be `None` – otherwise use a default value.

### 5. Error Handling

* Catch only expected exceptions.
* Wrap external calls in time‑outs (e.g., `requests` timeout, `httpx` timeout).
* Log errors with context using the standard `logging` module.
* Raise custom exceptions (`ProtocolError`, `DownloadError`) where reusable.

### 6. Docstrings & Comments

* All public modules, classes, and functions must have a concise docstring following the NumPy style.
* Inline comments should explain *why* something is done, not *what*.

### 7. Testing

* Tests must live under a `tests/` directory.
* Use PyTest fixtures for setup/teardown.
* Cover edge cases (e.g., missing data, timeouts, malformed JSON).
* Naming scheme: `test_<module>_<feature>`. |

### 8. Performance & Security

* Avoid blocking I/O in the main thread; use async if needed.
* Sanitize any user‑generated input, especially in URLs or file paths.
* Keep secrets out of the repository (use environment variables or `.env` files).

## Cursor / Copilot Rules

> **There are no `.cursor` or `.cursorrules` files in this repository.**

If you wish to add Cursor rules, place them in `./.cursor/rules/` following the standard format.

## Copilot Guidance

> **No `.github/copilot-instructions.md` file exists.**

If you plan to use GitHub Copilot, consider adding a `.github/copilot-instructions.md` to provide context to the model.

---

**Length**: Approximately 150 lines.
**Purpose**: This guide equips any agent or developer with clear instructions on building, linting, testing, and maintaining consistent code style across the project.