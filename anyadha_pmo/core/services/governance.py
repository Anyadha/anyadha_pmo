"""Shared Wave 3 governance validation services."""
from __future__ import annotations

import frappe
from frappe.utils import getdate, today

from anyadha_pmo.core.services.scope import validate_scope


def validate_dates(doc, start_field="effective_from", end_field="effective_to"):
    start = doc.get(start_field)
    end = doc.get(end_field)
    if start and end and getdate(end) < getdate(start):
        frappe.throw(f"{end_field.replace('_', ' ').title()} cannot be before {start_field.replace('_', ' ').title()}.")


def validate_due_date(doc, due_field="due_date", completion_field="completion_date"):
    due = doc.get(due_field)
    completion = doc.get(completion_field)
    if due and completion and getdate(completion) > getdate(due):
        # Late completion is permitted; this is informational, not a blocking rule.
        return


def validate_governance_scope(doc):
    validate_scope(doc)
    validate_dates(doc)


def require_attachment(doc, fieldname="evidence", condition=True, message=None):
    if condition and not doc.get(fieldname):
        frappe.throw(message or f"{fieldname.replace('_', ' ').title()} is required before this record can proceed.")


def prevent_self_verification(doc, owner_fields=("responsible", "responsible_employee", "document_owner"), verifier_field="verified_by"):
    verifier = doc.get(verifier_field)
    if not verifier:
        return
    for field in owner_fields:
        owner = doc.get(field)
        if owner and verifier == owner:
            frappe.throw("The person responsible for the action/control/document cannot independently verify the same record.", frappe.PermissionError)
