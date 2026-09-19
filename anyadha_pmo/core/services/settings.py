"""PMO configuration accessors.

Keep settings reads centralized so domain code does not depend on the layout of
PMO Settings.  The helpers are deliberately defensive for patch/migration time.
"""
from __future__ import annotations

import frappe


def get_settings():
    return frappe.get_single("PMO Settings")


def get_value(fieldname: str, default=None):
    try:
        value = get_settings().get(fieldname)
    except Exception:
        return default
    return default if value in (None, "") else value


def is_enabled(fieldname: str, default: bool = False) -> bool:
    return bool(get_value(fieldname, int(default)))
