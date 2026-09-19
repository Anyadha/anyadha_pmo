"""Thin boundary around native Frappe Workflow operations."""
from __future__ import annotations

import frappe


def get_workflow_state(doc):
    meta = frappe.get_meta(doc.doctype)
    if meta.has_field("workflow_state"):
        return doc.get("workflow_state")
    return None


def is_workflow_enabled() -> bool:
    try:
        return bool(frappe.db.get_single_value("PMO Settings", "enable_workflows"))
    except Exception:
        return True
