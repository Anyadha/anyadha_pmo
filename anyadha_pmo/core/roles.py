"""Idempotent creation of Anyadha PMO application roles."""

from __future__ import annotations

import frappe

PMO_ROLES = [
    "PMO Administrator",
    "PMO Head",
    "PMO Manager",
    "PMO Coordinator",
    "PMO Officer",
    "PMO Viewer",
    "PMO Governance Manager",
    "PMO Programme Manager",
    "PMO Project Manager",
    "PMO M&E Manager",
    "PMO Grants Manager",
    "PMO CSR Manager",
    "PMO Compliance Manager",
    "PMO Internal Auditor",
    "PMO Finance Manager",
]


def ensure_pmo_roles() -> None:
    """Create missing PMO roles; safe to run repeatedly."""
    for role_name in PMO_ROLES:
        if frappe.db.exists("Role", role_name):
            continue

        frappe.get_doc(
            {
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1,
            }
        ).insert(ignore_permissions=True)

    frappe.db.commit()
