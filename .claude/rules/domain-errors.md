---
paths: ["domain/**/*.py"]
---

# Domain Services Error Handling Standard

## Error Response Format
Whenever a service function in `domain/services.py` encounters a business logic failure (e.g., out of stock, security limit, invalid ID), it MUST return a structured dictionary instead of raising generic exceptions or returning simple error strings.

The error dictionary must strictly contain the following keys:
1. `"success"`: Always `False`.
2. `"errorCategory"`: Must be one of:
   - `"validation"` (for invalid user inputs, wrong IDs).
   - `"permission"` (for business rule block, e.g. refund > $500).
   - `"transient"` (for temporary failures like lock blocks).
3. `"isRetryable"`: Boolean (`True` or `False`).
4. `"message"`: A clear, human-readable description of the error.

## Example (How to write service errors):
```python
# Bad:
# return {"error": "No stock"}

# Good:
return {
    "success": False,
    "errorCategory": "validation",
    "isRetryable": False,
    "message": "Insufficient stock. Only 2 units available."
}