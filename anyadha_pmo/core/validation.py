"""Shared validation helpers for Anyadha PMO.

Keep business rules in individual DocType controllers. This module contains
small, dependency-light helpers that are safe to reuse across modules.
"""

from __future__ import annotations

from typing import Any

import frappe


def require_non_negative(doc: Any, *fieldnames: str) -> None:
    """Reject negative numeric values for the supplied fields."""
    for fieldname in fieldnames:
        value = doc.get(fieldname)
        if value is not None and value < 0:
            label = frappe.get_meta(doc.doctype).get_label(fieldname) or fieldname
            frappe.throw(f"{label} cannot be negative.")


def require_link_value(doc: Any, fieldname: str, message: str | None = None) -> None:
    """Require a Link-like field to be populated when business logic demands it."""
    if not doc.get(fieldname):
        label = frappe.get_meta(doc.doctype).get_label(fieldname) or fieldname
        frappe.throw(message or f"{label} is required.")


def ensure_date_order(doc: Any, from_field: str, to_field: str) -> None:
    """Ensure an optional start/end date pair is logically ordered."""
    start = doc.get(from_field)
    end = doc.get(to_field)
    if start and end and start > end:
        meta = frappe.get_meta(doc.doctype)
        start_label = meta.get_label(from_field) or from_field
        end_label = meta.get_label(to_field) or to_field
        frappe.throw(f"{start_label} cannot be after {end_label}.")
