# Architecture Tests Documentation

## Overview

Architecture tests are automated tests that enforce design constraints and architectural rules at the code level. They prevent regressions and serve as executable documentation of design decisions.

All architecture tests are located in `tests/presentation/test_architecture.py` and are organized into 8 test categories.

## Why Architecture Tests Matter

Architecture tests provide:
1. **Regression Prevention**: Catch violations immediately when someone accidentally violates architectural rules
2. **Self-Documentation**: Show developers what the architectural constraints are
3. **Confidence**: Green tests guarantee that key properties hold, not just that code runs
4. **Maintainability**: Prevent architectural decay over time

## The 7 Architectural Rules Enforced

### Rule 1: Dependency Direction (Unidirectional)

**Rule**: `App → Screens → Handlers/Components → Services → Ports`

**Tests**: 
- `TestNoCircularDependencies::test_handlers_not_dependent_on_screens`
- `TestNoCircularDependencies::test_services_not_dependent_on_handlers`

**What fails the test**:
```python
# ❌ FAILS: Handler imports from screens
from task_tracker_tui.presentation.screens import SomeScreen

# ❌ FAILS: Service imports from handlers  
from task_tracker_tui.presentation.handlers import SomeHandler
```

**What passes the test**:
```python
# ✅ PASSES: Handler depends only on injected services
def __init__(self, screen_messenger_service: ScreenMessengerService):
    self.screen_messenger = screen_messenger_service

# ✅ PASSES: Service has port dependency
from task_tracker_tui.presentation.services.screen_messenger_service import ScreenMessengerPort
```

**Why this matters**: Circular dependencies cause maintenance problems and make testing difficult. Unidirectional flow ensures that:
- Outer layers (App) can coordinate all other layers
- Inner layers (Services) have no knowledge of who uses them
- Testing is possible by mocking only lower layers

### Rule 2: No Multiple Inheritance

**Rule**: Classes should use single inheritance only. Use composition instead of inheriting from multiple classes.

**Tests**:
- `TestNoMultipleInheritance::test_confirmation_handler_single_inheritance`
- `TestNoMultipleInheritance::test_form_handler_single_inheritance`

**What fails the test**:
```python
# ❌ FAILS: Multiple inheritance
class ConfirmationHandler(HandlerPort, ABC, SomethingElse):
    pass
```

**What passes the test**:
```python
# ✅ PASSES: Single inheritance only
class ConfirmationHandler:
    def __init__(self, screen_messenger_service):
        self.screen_messenger = screen_messenger_service  # Composition
```

**Why this matters**: Multiple inheritance creates:
- Diamond problem (method resolution ambiguity)
- Tight coupling between classes
- Difficult testing (unclear which parent to mock)

Using composition (dependency injection) is clearer and more testable.

### Rule 3: Dependency Injection

**Rule**: All dependencies must be explicitly injected through constructors. No global state or implicit dependencies.

**Tests**:
- `TestHandlerDependencies::test_confirmation_handler_has_constructor`
- `TestHandlerDependencies::test_form_handler_has_constructor`
- `TestServiceDependencies::test_screen_messenger_service_constructor`
- `TestServiceDependencies::test_error_display_service_methods`

**What fails the test**:
```python
# ❌ FAILS: Implicit/global dependency
class ConfirmationHandler:
    def __init__(self):
        self.messenger = ScreenMessengerService()  # Magic dependency

    def handle(self, request):
        self.GLOBAL_MESSENGER.post_message(...)  # Hidden dependency
```

**What passes the test**:
```python
# ✅ PASSES: Explicit dependency injection
class ConfirmationHandler:
    def __init__(self, screen_messenger_service: ScreenMessengerService):
        self.screen_messenger = screen_messenger_service  # Explicit
```

**Why this matters**: Explicit dependencies:
- Make code easier to understand (you can see what's needed)
- Enable testing (you can mock dependencies)
- Reduce coupling (handler doesn't know how to create messenger)
- Follow the principle of Inversion of Control (IoC)

### Rule 4: Protocol-Based Design (Not ABC Inheritance)

**Rule**: Handlers should implement protocols (interfaces), not inherit from ABC or other handlers.

**Tests**:
- `TestHandlerPortGeneric::test_handler_port_is_protocol`
- `TestHandlerPortGeneric::test_handler_port_has_handle_method`
- `TestHandlerPortGeneric::test_confirmation_handler_implements_handle`

**What fails the test**:
```python
# ❌ FAILS: Handler inherits from HandlerPort (ABC)
class ConfirmationHandler(HandlerPort, ABC):
    async def handle(self, request):
        pass

# ❌ FAILS: Handle method is not async
def handle(self, request):  # Should be: async def handle(...)
    pass
```

**What passes the test**:
```python
# ✅ PASSES: Handler implements protocol (composition)
class ConfirmationHandler:
    async def handle(self, request: PauseResumeRequest) -> PauseResumeResponse:
        # Implementation
        pass

# ✅ PASSES: Protocol defines expected interface
class HandlerPort(Protocol[RequestT, ResponseT]):
    async def handle(self, request: RequestT) -> ResponseT: ...
```

**Why this matters**: Protocols over inheritance:
- Structural typing (what matters is what the object can do)
- No forced inheritance hierarchies
- Better type safety with generics
- Easier to test (duck typing for mocks)

### Rule 5: Generic Types for Type Safety

**Rule**: Use generic types to avoid `Any` types. Handler protocols should be parameterized with request/response types.

**Tests**:
- `TestHandlerPortGeneric::test_handler_port_is_protocol`

**What fails the test**:
```python
# ❌ FAILS: Using Any types
class HandlerPort(Protocol):
    async def handle(self, request: Any) -> Any:
        pass

# ❌ FAILS: No type information
class ConfirmationHandler:
    async def handle(self, request):  # Missing type hints
        pass
```

**What passes the test**:
```python
# ✅ PASSES: Generic types with proper parameterization
from typing import TypeVar, Protocol

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")

class HandlerPort(Protocol[RequestT, ResponseT]):
    async def handle(self, request: RequestT) -> ResponseT: ...

# ✅ PASSES: Concrete handler with specific types
class ConfirmationHandler:
    async def handle(self, request: PauseResumeRequest) -> PauseResumeResponse:
        pass
```

**Why this matters**: Generic types:
- Enable static type checking (mypy can verify types)
- Document expected request/response types
- Prevent type errors at runtime
- Make code self-documenting

### Rule 6: Immutable Request/Response Models

**Rule**: Request and response models should be frozen dataclasses to prevent mutation and enable safe sharing.

**Tests**:
- `TestRequestResponseModels::test_pause_resume_request_exists`
- `TestRequestResponseModels::test_models_are_frozen_dataclasses`

**What fails the test**:
```python
# ❌ FAILS: Mutable dataclass
@dataclass
class PauseResumeRequest:
    task_id: str
    is_running: bool
    # Someone could do: request.task_id = "different_id"
```

**What passes the test**:
```python
# ✅ PASSES: Frozen dataclass (immutable)
@dataclass(frozen=True)
class PauseResumeRequest:
    task_id: str
    is_running: bool
    # TypeError if someone tries to modify: request.task_id = "different_id"
```

**Why this matters**: Frozen dataclasses:
- Prevent accidental modifications
- Enable safe sharing between functions
- Can be used as dict keys or in sets
- Show intent (these values don't change)

### Rule 7: Message Package Organization

**Rule**: Message classes should be organized in a package with one message per file, with exports in `__init__.py`.

**Tests**:
- `TestMessagePackageExports::test_navigate_to_exported`
- `TestMessagePackageExports::test_pop_screen_exported`
- `TestMessagePackageExports::test_push_screen_exported`
- `TestMessagePackageExports::test_exit_app_exported`
- `TestMessagePackageExports::test_all_messages_in_init`

**What fails the test**:
```python
# ❌ FAILS: Message not exported in __init__.py
# File: src/.../presentation/messages/__init__.py
# NavigateTo is defined but not in __all__

# ❌ FAILS: Multiple messages in one file (not modular)
# File: src/.../presentation/messages.py (old monolithic approach)
```

**What passes the test**:
```python
# ✅ PASSES: Individual message files with package exports
# File: src/.../presentation/messages/navigate_to.py
class NavigateTo(Message):
    screen: str
    kwargs: dict[str, Any] = field(default_factory=dict)

# File: src/.../presentation/messages/__init__.py
from .navigate_to import NavigateTo
from .pop_screen import PopScreen
from .push_screen import PushScreen
from .exit_app import ExitApp

__all__ = ["NavigateTo", "PopScreen", "PushScreen", "ExitApp"]
```

**Why this matters**: Message package organization:
- Single Responsibility (one message per file)
- Easy to find message definitions
- Clear what messages are available (__all__)
- Scalable (new messages don't touch existing ones)

## Test Organization

### Test Classes and Their Purpose

1. **TestMessagePackageExports** (5 tests)
   - Verifies all messages are properly exported
   - Ensures package __all__ is complete

2. **TestHandlerDependencies** (4 tests)
   - Confirms handlers have proper constructor injection
   - Validates handler methods exist (handle, convenience methods)

3. **TestServiceDependencies** (4 tests)
   - Verifies services have port interfaces
   - Confirms constructor injection patterns
   - Validates service methods exist

4. **TestNoCircularDependencies** (2 tests)
   - Handlers don't import screens
   - Services don't import handlers

5. **TestHandlerPortGeneric** (3 tests)
   - Confirms HandlerPort is a Protocol
   - Validates handle() method signature
   - Confirms async implementation

6. **TestRequestResponseModels** (7 tests)
   - All request/response models exist
   - All models are frozen dataclasses
   - Immutability verified

7. **TestNoMultipleInheritance** (2 tests)
   - Single inheritance only
   - No problematic base class combinations

## How to Read Architecture Test Failures

### Example 1: Missing Dependency Injection
```
FAILED test_confirmation_handler_has_constructor
AssertionError: 'screen_messenger_service' not in sig.parameters
```

**Meaning**: ConfirmationHandler constructor doesn't accept `screen_messenger_service` parameter.

**Fix**: Add parameter to constructor:
```python
def __init__(self, screen_messenger_service: ScreenMessengerService):
    self.screen_messenger = screen_messenger_service
```

### Example 2: Circular Import
```
FAILED test_handlers_not_dependent_on_screens
AssertionError: Handler imports from screens detected
```

**Meaning**: A handler file imports something from `presentation.screens`.

**Fix**: Remove the import from handler and pass data through dependency injection instead.

### Example 3: Missing Message Export
```
FAILED test_all_messages_in_init
KeyError: 'NewMessage'
```

**Meaning**: A new message class exists but isn't exported in `__init__.py`.

**Fix**: Add to `src/.../presentation/messages/__init__.py`:
```python
from .new_message import NewMessage

__all__ = [..., "NewMessage"]
```

## Running Architecture Tests

```bash
# Run only architecture tests
pytest tests/presentation/test_architecture.py -v

# Run with detailed output
pytest tests/presentation/test_architecture.py -vv

# Run specific test class
pytest tests/presentation/test_architecture.py::TestMessagePackageExports -v

# Run and show test names that passed
pytest tests/presentation/test_architecture.py -v | grep PASSED
```

## Integration with CI/CD

Architecture tests should:
1. Run on every commit
2. Be part of the required checks (PR cannot merge if architecture tests fail)
3. Pass with 100% success rate (cannot be flaky)
4. Complete in under 1 second (no external resources)

## Future Extensions

### Possible Additional Architecture Tests

1. **Service Port Consistency**: Verify that every service has a corresponding Port interface
2. **Import Path Consistency**: Ensure all imports use `task_tracker_tui.*` not `src.task_tracker_tui.*`
3. **Screen Constructor Validation**: All screens should accept only port dependencies, not concrete services
4. **Component Isolation**: Components should not import handlers or other components
5. **Message Handler Mapping**: Verify every message type has a corresponding handler

### Adding New Architecture Tests

When adding new architectural rules:
1. Write the test first (TDD)
2. Create a test class (e.g., `TestNewRule`)
3. Add descriptive docstrings explaining the rule
4. Document the rule in this file
5. Ensure test is fast and doesn't depend on external resources

## Related Documentation

- `docs/ARCHITECTURE.md` - High-level architecture overview
- `docs/DEPENDENCY_INJECTION.md` - Dependency injection patterns
- `docs/TESTING.md` - General testing guidelines
- `src/task_tracker_tui/presentation/handlers/handler_port.py` - Protocol definition
