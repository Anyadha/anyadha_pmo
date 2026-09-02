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

    # System Manager must retain access so the PMO can be
    # re-enabled if the master switch is turned off.
    if "System Manager" in roles:
        return True

    # PMO must be explicitly enabled before PMO-role users
    # can access the application.
    try:
        enable_pmo = frappe.db.get_single_value(
            "PMO Settings",
            "enable_pmo",
        )
    except Exception:
        # During installation/migration the singleton may not
        # exist yet. Do not block application installation.
        enable_pmo = 1

    if not enable_pmo:
        return False

    return bool(roles & PMO_ROLES)
