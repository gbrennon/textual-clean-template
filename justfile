run:
    uv run task-tracker-tui

test:
    uv run pytest

unit-test:
    uv run pytest tests/core --cov=src/task_tracker_tui/core

integration-test:
    uv run pytest tests/infrastructure --cov=src/task_tracker_tui/infrastructure

e2e-test:
    uv run pytest tests/presentation --cov=src/task_tracker_tui/presentation
