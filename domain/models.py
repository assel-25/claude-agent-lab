# DOMAIN CERTIFIED
# domain/models.py — Хранилище данных (In-Memory Database)

CATALOG = {
    "ITEM-001": {"name": "Wireless Mouse", "price": 45.00, "stock": 15},
    "ITEM-002": {"name": "Mechanical Keyboard", "price": 120.00, "stock": 4},
    "ITEM-003": {"name": "Ultra-Wide Monitor", "price": 450.00, "stock": 2},
    "ITEM-004": {"name": "High-End Gaming Laptop", "price": 1800.00, "stock": 1}
}

ORDERS_DB = {
    "ORD-101": {"item_id": "ITEM-001", "qty": 1, "status": "Shipped", "total": 45.00, "customer": "Alice", "salesperson_id": "SP-001"},
    "ORD-999": {"item_id": "ITEM-004", "qty": 1, "status": "Delivered", "total": 1800.00, "customer": "Bob", "salesperson_id": "SP-002"}
}

SALES_PEOPLE_DB = {
    "SP-001": {"name": "Dana Whitfield", "email": "dana.whitfield@example.com", "region": "North"},
    "SP-002": {"name": "Marcus Lee", "email": "marcus.lee@example.com", "region": "South"}
}


def get_record(db: dict, record_id: str, label: str = "Record"):
    """Returns db[record_id], or an error dict if the ID is unknown."""
    if record_id not in db:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"{label} {record_id} not found."
        }
    return db[record_id]
