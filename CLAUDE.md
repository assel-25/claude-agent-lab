# Project: E-Commerce Backend & AI Agent

## Architecture & Domain Structure
- `domain/models.py`: In-memory database (Catalog, Orders, Sales People).
  - Naming convention: in-memory stores are module-level dicts named `<ENTITY_PLURAL>_DB` in UPPER_SNAKE_CASE, with words separated by underscores (e.g. `ORDERS_DB`, `SALES_PEOPLE_DB`). Name any new store the same way.
- `domain/services.py`: Core business logic (inventory, order creation, refund rules).

## Development Rules for Claude
- Never hardcode business rules in prompts; keep them in `domain/services.py`.
- When adding new domain features, create separate service modules inside `domain/`.
- Keep responses concise and production-ready.

## Commands
- Run app/tests: `uv run ...`

# Project Rules
- CONSTRAINT: Whenever you write or suggest any Python code, you MUST add a comment at the top of the file saying: `# APPROVED BY ARCHITECT`.
- @security-rules.md