from __future__ import annotations

import frappe
from frappe.model.document import Document


class PMOAuthorityRule(Document):
    def validate(self):
        if self.threshold_from is not None and self.threshold_to is not None and self.threshold_from > self.threshold_to:
            frappe.throw("Threshold From cannot exceed Threshold To.")
        if (self.minimum_approvals or 0) < 1:
            frappe.throw("Minimum Approvals must be at least 1.")
        if self.sequence is not None and self.sequence < 1:
            frappe.throw("Sequence must be at least 1.")
        if not frappe.db.exists("Role", self.approver_role):
            frappe.throw("Approver Role must reference an existing Frappe Role.")
