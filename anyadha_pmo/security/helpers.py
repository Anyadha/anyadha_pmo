"""Small helpers for PMO server-side authorization.

Do not use these helpers as a replacement for Frappe Role Permission Manager
or User Permissions. They are for explicit server-side business actions.
"""

from __future__ import annotations

import frappe

from anyadha_pmo.security.roles import PMO_ROLE_NAMES


def get_pmo_roles(user: str | None = None) -> set[str]:
    user = user or frappe.session.user
    return PMO_ROLE_NAMES.intersection(set(frappe.get_roles(user)))


def has_any_role(*roles: str, user: str | None = None) -> bool:
    return bool(get_pmo_roles(user).intersection(roles))


def require_any_role(*roles: str, user: str | None = None) -> None:
    if not has_any_role(*roles, user=user):
        frappe.throw(
            "You do not have the required PMO role for this action.",
            frappe.PermissionError,
        )


def is_pmo_administrator(user: str | None = None) -> bool:
    user = user or frappe.session.user
    return bool({"PMO Administrator", "System Manager"} & set(frappe.get_roles(user)))
