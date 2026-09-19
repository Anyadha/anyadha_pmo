"""PMO scope enforcement helpers for company/entity/business-unit boundaries."""
from __future__ import annotations

import frappe

from anyadha_pmo.core.services.settings import is_enabled


def _user_permissions(user=None):
    user = user or frappe.session.user
    rows = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": ["in", ["Company", "PMO Entity", "PMO Business Unit"]]},
        fields=["allow", "for_value"],
    )
    result = {"Company": set(), "PMO Entity": set(), "PMO Business Unit": set()}
    for row in rows:
        result.setdefault(row.allow, set()).add(row.for_value)
    return result


def validate_scope(doc, user=None):
    if not is_enabled("enforce_company_restrictions", True) and not is_enabled("enforce_entity_restrictions", True):
        return
    permissions = _user_permissions(user)
    if is_enabled("enforce_company_restrictions", True) and doc.get("company"):
        allowed = permissions["Company"]
        if allowed and doc.company not in allowed:
            frappe.throw("The selected Company is outside the user's PMO scope.", frappe.PermissionError)
    if is_enabled("enforce_entity_restrictions", True) and doc.get("entity"):
        allowed = permissions["PMO Entity"]
        if allowed and doc.entity not in allowed:
            frappe.throw("The selected PMO Entity is outside the user's PMO scope.", frappe.PermissionError)
    if doc.get("business_unit"):
        allowed = permissions["PMO Business Unit"]
        if allowed and doc.business_unit not in allowed:
            frappe.throw("The selected Business Unit is outside the user's PMO scope.", frappe.PermissionError)
