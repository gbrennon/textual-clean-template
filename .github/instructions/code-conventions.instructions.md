---
applyTo: "**/*.py"
---

# Python Code Conventions

These conventions apply to every `.py` file in this project.

## One Class Per File
Each file defines exactly one public class. The file name must match the class name in `snake_case`.

```
src/task_tracker_tui/core/models/task.py          → class Task
src/task_tracker_tui/core/models/task_timer.py    → class TaskTimer
src/task_tracker_tui/core/ports/task_repository.py → class TaskRepository (Protocol)
src/task_tracker_tui/core/services/create_task_service.py → class CreateTaskService
```

## No Internal / Nested Classes or Functions
Never define classes or functions inside other classes or functions. All helpers must be top-level or extracted to their own module.

```python
# ✅ Correct — helper extracted to its own module
# src/task_tracker_tui/core/models/task_timer.py
class TaskTimer:
    ...


# ❌ Wrong — nested class
class Task:
    @dataclass
    class Timer:   # nested — not allowed
        elapsed_minutes: float = 0.0


# ❌ Wrong — nested helper function
class CreateTaskService:
    async def execute(self, title: str) -> Task:
        def _build_task(t: str) -> Task:   # nested function — not allowed
            return Task(title=t, description="")
        return _build_task(title)
```

## Imports at the Top of Every File
All `import` and `from … import` statements must appear at the top of the file, before any other code. Group them in this order, separated by a blank line:
1. Standard library
2. Third-party packages
3. Local application imports

```python
# ✅ Correct — imports at the top, properly grouped
from dataclasses import dataclass, field
from datetime import datetime

from textual.app import App

from task_tracker_tui.core.models.task import Task
from task_tracker_tui.core.ports.task_repository import TaskRepository


@dataclass
class SomeClass:
    ...


# ❌ Wrong — import inside a function or method
class SomeService:
    async def execute(self) -> None:
        from task_tracker_tui.core.models.task import Task   # not allowed
        ...
```

## Test Files: Imports at the Top
Test files follow the same rule. All imports — including `pytest`, fixtures, and the class under test — must be at the top of the file.

```python
# ✅ Correct
import pytest

from task_tracker_tui.core.models.task import Task
from task_tracker_tui.core.services.create_task_service import CreateTaskService
from tests.core.fakes.fake_task_repository import FakeTaskRepository


@pytest.mark.asyncio
async def test_execute_creates_task_with_correct_title() -> None:
    repository = FakeTaskRepository()
    service = CreateTaskService(repository)

    task = await service.execute("My Task", "Some description")

    assert task.title == "My Task"


# ❌ Wrong — import inside a test function
async def test_execute_creates_task() -> None:
    from task_tracker_tui.core.services.create_task_service import CreateTaskService  # not allowed
    ...
```

## Additional Rules
- No magic numbers or strings — use named constants.
- No commented-out code — delete it.
- No dead code — remove it.
- Functions and methods should do one thing and stay at a single level of abstraction.
- Prefer early returns and guard clauses to reduce nesting depth.
