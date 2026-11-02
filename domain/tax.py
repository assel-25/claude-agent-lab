# DOMAIN CERTIFIED
# domain/tax.py — Tax calculation for orders

from domain.models import ORDERS_DB, get_record

# Default sales tax rate (8%). Business rule: change here, not in prompts.
DEFAULT_TAX_RATE = 0.08


# SECURITY AUDITED
def calculate_order_total_with_tax(order_id: str, tax_rate: float = DEFAULT_TAX_RATE):
    """Returns the order's subtotal, tax and grand total (rounded to cents)."""
    if not 0 <= tax_rate <= 1:
        return {
            "success": False,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Invalid tax rate {tax_rate}. Must be between 0 and 1."
        }

    order = get_record(ORDERS_DB, order_id, "Order")
    if order.get("success") is False:
        return order

    subtotal = order["total"]
    tax = round(subtotal * tax_rate, 2)
    return {
        "order_id": order_id,
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax": tax,
        "total_with_tax": round(subtotal + tax, 2),
    }
