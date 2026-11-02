# DOMAIN CERTIFIED
# domain/services.py — Бизнес-логика (Сервисный слой)

from domain.models import CATALOG, ORDERS_DB
from domain.salespeople import salesperson_exists

def check_inventory(item_id: str):
    """Проверяет наличие товара на складе."""
    if item_id not in CATALOG:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Item {item_id} does not exist in catalog."
        }
    return CATALOG[item_id]

def create_order(item_id: str, qty: int, customer: str, salesperson_id: str | None = None):
    """Создает новый заказ с проверкой склада и остатков."""
    if item_id not in CATALOG:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Item not found."
        }
    if salesperson_id is not None and not salesperson_exists(salesperson_id):
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Salesperson {salesperson_id} not found."
        }
    
    item = CATALOG[item_id]
    if item["stock"] < qty:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Insufficient stock. Only {item['stock']} units available."
        }
    
    # Списываем со склада
    CATALOG[item_id]["stock"] -= qty
    total_amount = item["price"] * qty
    
    order_id = f"ORD-{len(ORDERS_DB) + 101}"
    ORDERS_DB[order_id] = {
        "item_id": item_id,
        "qty": qty,
        "status": "Processing",
        "total": total_amount,
        "customer": customer,
        "salesperson_id": salesperson_id
    }
    
    return {
        "success": True,
        "order_id": order_id,
        "total": total_amount,
        "status": "Processing",
        "salesperson_id": salesperson_id
    }

def get_order_status(order_id: str):
    """Возвращает статус заказа."""
    if order_id not in ORDERS_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Order {order_id} not found."
        }
    return ORDERS_DB[order_id]

def request_refund(order_id: str, reason: str):
    """Запрашивает возврат средств (срабатывает бизнес-правило безопасности для сумм > $500)."""
    if order_id not in ORDERS_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Order {order_id} not found."
        }
    
    order = ORDERS_DB[order_id]
    
    # Бизнес-правило / хук
    if order["total"] > 500.00:
        return {
            "success": False,
            "errorCategory": "permission",
            "isRetryable": False,
            "escalationRequired": True,
            "message": f"SECURITY BLOCK: Order total (${order['total']}) exceeds automated $500 refund limit. Manager approval required."
        }
        
    return {
        "success": True,
        "message": f"Refund of ${order['total']} for order {order_id} processed successfully."
    }

# Orders in these statuses can no longer be paid for.
NON_PAYABLE_STATUSES = {"Shipped", "Delivered"}

# SECURITY AUDITED
def pay_for_order(order_id: str, payment_method: str):
    """Marks an order as paid. Fails for unknown orders and orders already shipped/delivered."""
    if order_id not in ORDERS_DB:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Order {order_id} not found."
        }
    if not payment_method or not payment_method.strip():
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Payment method is required."
        }

    order = ORDERS_DB[order_id]
    if order["status"] in NON_PAYABLE_STATUSES:
        return {
            "success": False,
            "errorCategory": "permission",
            "isRetryable": False,
            "message": f"Order {order_id} is already {order['status']} and cannot be paid for."
        }

    order["status"] = "Paid"
    return {
        "success": True,
        "order_id": order_id,
        "amount": order["total"],
        "payment_method": payment_method,
        "status": "Paid",
    }
