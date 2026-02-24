---
applyTo: "**/*.py"
---

# SOLID Principles

Apply all five SOLID principles consistently. These principles are language-agnostic; code examples below show how they are expressed in Python for this project.

## Single Responsibility Principle (SRP)
Each class has exactly one reason to change. Never mix domain logic with persistence, I/O, or UI concerns in the same class.

```python
# ✅ Correct — one responsibility
class CreateTaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def execute(self, command: CreateTaskCommand) -> Task:
        task = Task(title=command.title, description=command.description)
        await self._repository.save(task)
        return task


# ❌ Wrong — mixes domain logic with persistence
class TaskManager:
    def create_and_save_and_notify(self, title: str) -> None:
        task = Task(title=title, description="")
        with open("tasks.json", "w") as f:
            json.dump(task.to_dict(), f)
        print(f"Task {title} created")
```

## Open/Closed Principle (OCP)
Classes are open for extension, closed for modification. Favor abstractions and composition over branching on types (e.g. `if/elif isinstance(...)`).

```python
# ✅ Correct — extend by adding new classes, not modifying existing ones
class TaskRepository(Protocol):
    async def save(self, task: Task) -> None: ...

class JsonTaskRepository:
    async def save(self, task: Task) -> None:
        # JSON-specific implementation

class InMemoryTaskRepository:
    async def save(self, task: Task) -> None:
        # In-memory implementation
```

## Liskov Substitution Principle (LSP)
Any implementation of an interface or abstract base must be fully substitutable for it. Never override in ways that weaken preconditions or strengthen postconditions.

```python
# ✅ Correct — InMemoryTaskRepository honours the full TaskRepository contract
class InMemoryTaskRepository:
    async def find_by_id(self, task_id: str) -> Task | None:
        return self._store.get(task_id)  # returns Task or None, as declared
```

## Interface Segregation Principle (ISP)
Define narrow, role-specific interfaces. Clients must not depend on methods they don't use. In Python, use `Protocol` to declare them.

```python
# ✅ Correct — focused protocols
class TaskReader(Protocol):
    async def find_by_id(self, task_id: str) -> Task | None: ...
    async def find_all(self) -> list[Task]: ...

class TaskWriter(Protocol):
    async def save(self, task: Task) -> None: ...
    async def delete(self, task_id: str) -> None: ...


# ❌ Wrong — fat interface forces all clients to depend on everything
class TaskRepository(Protocol):
    async def save(self, task: Task) -> None: ...
    async def find_by_id(self, task_id: str) -> Task | None: ...
    async def find_all(self) -> list[Task]: ...
    async def delete(self, task_id: str) -> None: ...
    async def export_to_csv(self, path: str) -> None: ...   # unrelated to core CRUD
```

## Dependency Inversion Principle (DIP)
Depend on abstractions (interfaces), never on concretions. Inject all dependencies via the constructor; never instantiate infrastructure collaborators inside business logic. In Python, declare abstractions with `Protocol` or ABC.

```python
# ✅ Correct — depends on abstraction, injected from outside
class CompleteTaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository


# ❌ Wrong — instantiates concrete infrastructure inside domain logic
class CompleteTaskService:
    def __init__(self) -> None:
        self._repository = JsonTaskRepository("tasks.json")  # hard dependency
```
