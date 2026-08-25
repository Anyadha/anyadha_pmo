"""Anyadha PMO application access control."""

import frappe


PMO_ROLES = {
    "PMO Administrator",
    "PMO Head",
    "Programme Manager",
    "Project Manager",
    "PMO Officer",
    "M&E Manager",
    "M&E Officer",
    "Grants Manager",
    "CSR Manager",
    "Compliance Officer",
    "Internal Auditor",
    "Executive / Management",
    "Board Member",
}


def check_app_permission():
    """Return whether the current user can access Anyadha PMO."""

    if frappe.session.user == "Guest":
        return False

    roles = set(frappe.get_roles())

    if "System Manager" in roles:
        return True

    return bool(roles & PMO_ROLES)
