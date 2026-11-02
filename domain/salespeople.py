# APPROVED BY ARCHITECT
# domain/salespeople.py — Salespeople / account managers: order assignment and sales tracking

from domain.models import ORDERS_DB, SALES_PEOPLE_DB

# Orders in these statuses do not count toward a salesperson's sales.
NON_SALE_STATUSES = {"Cancelled", "Refunded"}


def salesperson_exists(salesperson_id: str) -> bool:
    return salesperson_id in SALES_PEOPLE_DB


def get_salesperson(salesperson_id: str):
    """Returns salesperson details."""
    if salesperson_id not in SALES_PEOPLE_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Salesperson {salesperson_id} not found."
        }
    return SALES_PEOPLE_DB[salesperson_id]


def assign_salesperson(order_id: str, salesperson_id: str):
    """Assigns (or reassigns) a salesperson to an existing order."""
    if order_id not in ORDERS_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Order {order_id} not found."
        }
    if salesperson_id not in SALES_PEOPLE_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Salesperson {salesperson_id} not found."
        }

    ORDERS_DB[order_id]["salesperson_id"] = salesperson_id
    return {"success": True, "order_id": order_id, "salesperson_id": salesperson_id}


def get_salesperson_sales(salesperson_id: str):
    """Returns total sales, derived from orders so it never drifts from ORDERS_DB."""
    if salesperson_id not in SALES_PEOPLE_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Salesperson {salesperson_id} not found."
        }

    order_ids = [
        oid for oid, o in ORDERS_DB.items()
        if o.get("salesperson_id") == salesperson_id and o["status"] not in NON_SALE_STATUSES
    ]
    return {
        "salesperson_id": salesperson_id,
        "name": SALES_PEOPLE_DB[salesperson_id]["name"],
        "order_count": len(order_ids),
        "total_sales": sum(ORDERS_DB[oid]["total"] for oid in order_ids),
        "order_ids": order_ids,
    }
