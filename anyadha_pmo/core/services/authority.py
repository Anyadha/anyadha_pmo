"""Effective-dated delegation-of-authority resolution."""
from __future__ import annotations

import frappe
from frappe.utils import getdate


def resolve_matrix(company=None, entity=None, business_unit=None, on_date=None):
    on_date = getdate(on_date) if on_date else getdate()
    filters = {"status": "Active", "effective_from": ["<=", on_date]}
    matrices = frappe.get_all(
        "PMO Authority Matrix",
        filters=filters,
        fields=["name", "company", "entity", "business_unit", "priority", "effective_from", "effective_to"],
        order_by="priority asc, effective_from desc, modified desc",
    )
    candidates = []
    for matrix in matrices:
        if matrix.effective_to and getdate(matrix.effective_to) < on_date:
            continue
        if matrix.company and matrix.company != company:
            continue
        if matrix.entity and matrix.entity != entity:
            continue
        if matrix.business_unit and matrix.business_unit != business_unit:
            continue
        specificity = sum(bool(matrix.get(k)) for k in ("company", "entity", "business_unit"))
        candidates.append((specificity, matrix))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (-x[0], x[1].priority or 999999, -getdate(x[1].effective_from).toordinal()))
    return candidates[0][1]


def resolve_rules(matrix_name, transaction_type, amount=None, currency=None):
    filters = {"authority_matrix": matrix_name, "transaction_type": transaction_type, "active": 1}
    rules = frappe.get_all(
        "PMO Authority Rule",
        filters=filters,
        fields=["*"],
        order_by="sequence asc, threshold_from asc",
    )
    result = []
    amount = amount if amount is not None else 0
    for rule in rules:
        if rule.currency and currency and rule.currency != currency:
            continue
        if rule.threshold_from is not None and amount < rule.threshold_from:
            continue
        if rule.threshold_to is not None and amount > rule.threshold_to:
            continue
        result.append(rule)
    return result
