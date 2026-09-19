from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

from anyadha_pmo.core.validation import ensure_date_order


class PMOAuthorityMatrix(Document):
    def validate(self):
        ensure_date_order(self, "effective_from", "effective_to")
        if self.status == "Active" and not self.effective_from:
            frappe.throw("Effective From is required for an active Authority Matrix.")
        if self.priority is not None and self.priority < 1:
            frappe.throw("Priority must be at least 1.")
        self._validate_overlap()

    def _validate_overlap(self):
        if self.status != "Active" or not self.effective_from:
            return
        filters = {"status": "Active", "name": ["!=", self.name]}
        if self.company:
            filters["company"] = self.company
        if self.entity:
            filters["entity"] = self.entity
        if self.business_unit:
            filters["business_unit"] = self.business_unit
        for row in frappe.get_all("PMO Authority Matrix", filters=filters, fields=["name", "effective_from", "effective_to"]):
            start = max(getdate(self.effective_from), getdate(row.effective_from))
            end_self = getdate(self.effective_to) if self.effective_to else None
            end_other = getdate(row.effective_to) if row.effective_to else None
            end = min([d for d in (end_self, end_other) if d], default=None)
            if end is None or start <= end:
                frappe.throw(f"Authority Matrix period overlaps active matrix {row.name}.")
