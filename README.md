# E-Commerce Sales & Inventory Core

## Overview

An in-memory e-commerce backend built to be driven by an AI agent (Anthropic Claude). It covers catalog and inventory, order creation, payments, refunds, sales tax and salesperson tracking. All business rules live in the `domain/` service modules, not in prompts. Every service returns structured results, with a standard error shape (`success`, `errorCategory`, `isRetryable`, `message`) that an agent can act on.

## Project Structure

```
claude-agent-lab/
├── CLAUDE.md                  # Project rules and commands
├── security-rules.md          # Security & compliance rules
├── pyproject.toml             # Project metadata (uv)
├── uv.lock
├── domain/
│   ├── CLAUDE.md              # Domain-directory rules
│   ├── models.py              # In-memory database (catalog, orders, salespeople)
│   ├── services.py            # Inventory, orders, payments, refunds
│   ├── salespeople.py         # Salesperson assignment and sales tracking
│   └── tax.py                 # Order tax calculation
├── src/
│   └── claude_agent_lab/      # Application package entry point
└── .claude/
    ├── rules/domain-errors.md
    └── skills/                # audit-domain, generate-docs
```

## Business Domain Logic

### Models (`domain/models.py`)

In-memory stores. They are module-level dicts named `<ENTITY_PLURAL>_DB`, except the catalog, which is named `CATALOG`.

| Store | Key | Fields |
|---|---|---|
| `CATALOG` | `ITEM-xxx` | `name`, `price`, `stock` |
| `ORDERS_DB` | `ORD-xxx` | `item_id`, `qty`, `status`, `total`, `customer`, `salesperson_id` |
| `SALES_PEOPLE_DB` | `SP-xxx` | `name`, `email`, `region` |

`get_record(db, id, label)` is a generic lookup that returns a validation error dict for unknown IDs.

### Services (`domain/services.py`)

- **`check_inventory(item_id)`** returns the catalog entry, or a validation error for an unknown item.
- **`create_order(item_id, qty, customer, salesperson_id=None)`** validates the item, the optional salesperson and stock. It then decrements stock, computes `total = price * qty`, and stores the order with status `Processing`.
- **`get_order_status(order_id)`** returns the order record.
- **`pay_for_order(order_id, payment_method)`** requires a non-empty payment method. Orders that are `Shipped` or `Delivered` cannot be paid for. Otherwise the order becomes `Paid`.
- **`request_refund(order_id, reason)`** enforces the **$500 security refund limit**. If the order total exceeds $500, the refund is blocked with `errorCategory: "permission"` and `escalationRequired: True`, and manager approval is required. Refunds of $500 or less are processed automatically.

### Salespeople (`domain/salespeople.py`)

- `assign_salesperson(order_id, salesperson_id)` assigns or reassigns a salesperson to an order.
- `get_salesperson_sales(salesperson_id)` derives total sales from `ORDERS_DB`, excluding `Cancelled` and `Refunded` orders.

### Tax (`domain/tax.py`)

`calculate_order_total_with_tax(order_id, tax_rate=0.08)` returns the subtotal, tax and grand total, rounded to cents. The tax rate must be between 0 and 1.

### Conventions

- Functions that handle financial amounts are marked `# SECURITY AUDITED`.
- Files in `domain/` carry the `# DOMAIN CERTIFIED` header.
- Other Python files carry the `# APPROVED BY ARCHITECT` header.

## How to Run

Use [uv](https://docs.astral.sh/uv/) for everything:

```bash
uv sync                          # install dependencies
uv run claude-agent-lab          # run the app entry point
uv run python -c "from domain.services import check_inventory; print(check_inventory('ITEM-001'))"
uv run pytest                    # run tests (if present)
```

Requires Python 3.15 or later. Put your Anthropic API key in `.env` (loaded via `python-dotenv`).
