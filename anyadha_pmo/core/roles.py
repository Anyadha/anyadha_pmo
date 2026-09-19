"""Backward-compatible role helper; canonical role definitions live in security.roles."""
from __future__ import annotations

from anyadha_pmo.security.roles import PMO_ROLE_NAMES


def ensure_pmo_roles() -> None:
    import frappe

    for role_name in sorted(PMO_ROLE_NAMES):
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({"doctype": "Role", "role_name": role_name, "desk_access": 1}).insert(
                ignore_permissions=True
            )
    frappe.db.commit()
