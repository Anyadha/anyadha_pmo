"""Server-side segregation-of-duties checks."""
from __future__ import annotations

import frappe


def is_same_user(*users: str | None) -> bool:
    values = {u for u in users if u and u != "Guest"}
    return len(values) <= 1


def check_maker_checker(requested_by: str | None, approver: str | None) -> tuple[bool, str]:
    if is_same_user(requested_by, approver):
        return False, "Maker and checker cannot be the same user."
    return True, "Passed"


def require_maker_checker(requested_by: str | None, approver: str | None):
    passed, message = check_maker_checker(requested_by, approver)
    if not passed:
        frappe.throw(message, frappe.PermissionError)
