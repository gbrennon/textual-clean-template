# Textual Clean Hex Template

A clean, generic template for building [Textual](https://github.com/Textualize/textual) TUI applications following **Hexagonal Architecture** (Ports & Adapters) principles.

## Architecture Overview

This template enforces a strict **dependency rule**: inner layers never import from outer layers.

```
┌──────────────────────────────────────────────┐
│              Presentation Layer               │
│   (Textual App, Screens, Components, CSS)    │
├──────────────────────────────────────────────┤
│            Infrastructure Layer              │
│  (Persistence Adapters, External Services)   │
├──────────────────────────────────────────────┤
│             Application Layer                │
│       (Use Cases / Services / Ports)         │
├──────────────────────────────────────────────┤
│               Domain Layer                   │
│        (Entities, Value Objects)             │
└──────────────────────────────────────────────┘
         ↑ Dependencies point inward ↑
```

## Project Structure

```
src/tui_app/
├── core/                          # Domain + Application layers
│   ├── models/                    # Domain entities and value objects
│   │   ├── entity.py              # Base domain entity
│   │   └── value_object.py        # Base value object
│   ├── ports/                     # Ports (interfaces/protocols)
│   │   ├── entity_repository.py   # Repository protocol
│   │   ├── create_entity_port.py  # Use case port
│   │   └── navigator_port.py      # Navigation port
│   └── services/                  # Application services (use cases)
│       └── create_entity_service.py
├── infrastructure/                # Adapters (driven side)
│   ├── container.py               # Composition root / DI container
│   └── persistence/
│       └── in_memory_entity_repository.py
└── presentation/                  # Adapters (driving side)
    ├── app.py                     # Main Textual App class
    ├── router.py                  # Screen router
    ├── screens/                   # Textual screens
    ├── components/                # Reusable Textual widgets
    ├── messages/                  # Textual message classes
    ├── mixins/                    # Screen mixins
    ├── navigation/                # Navigator implementation
    ├── services/                  # Presentation-layer services
    └── css/                       # TCSS stylesheets
```

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
uv sync
```

### Running

```bash
uv run tui-app
```

### Running Tests

```bash
uv run pytest
```

## How to Use This Template

1. **Clone** this repository.
2. **Rename** `tui_app` to your package name.
3. **Replace** `Entity` in `core/models/entity.py` with your domain aggregate root.
4. **Replace** `ValueObject` in `core/models/value_object.py` with your domain value objects.
5. **Implement** the `EntityRepository` protocol in `infrastructure/persistence/`.
6. **Implement** the `CreateEntityService` use case in `core/services/`.
7. **Build** your screens in `presentation/screens/`.
8. **Wire** everything in `infrastructure/container.py`.

## Dependency Rule

> Source code dependencies can only point inward. Nothing in an inner layer can know anything about something in an outer layer.

- `core/` (domain + application) — knows nothing about infrastructure or presentation
- `infrastructure/` — knows about `core/` ports, implements adapters
- `presentation/` — knows about `core/` ports, drives use cases via the container

## License

MIT
