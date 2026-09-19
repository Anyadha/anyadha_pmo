"""Evidence checks using Frappe's native File attachments."""
from __future__ import annotations

import frappe


def has_attachments(doctype: str, name: str) -> bool:
    return bool(frappe.get_all("File", filters={"attached_to_doctype": doctype, "attached_to_name": name}, limit=1))


def require_evidence(doc):
    if doc.get("evidence_required") and not has_attachments(doc.doctype, doc.name):
        frappe.throw("Evidence is required before this approval can proceed.")
