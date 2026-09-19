from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from anyadha_pmo.core.services.evidence import require_evidence
from anyadha_pmo.core.services.sod import check_maker_checker


class PMOApprovalStep(Document):
    def before_insert(self):
        self.decision = self.decision or "Pending"
        self.sod_check_status = self.sod_check_status or "Not Checked"

    def validate(self):
        if self.sequence is not None and self.sequence < 1:
            frappe.throw("Sequence must be at least 1.")
        if not self.approval_request:
            frappe.throw("Approval Request is required.")
        request = frappe.get_doc("PMO Approval Request", self.approval_request)
        if self.approver and request.requested_by:
            passed, message = check_maker_checker(request.requested_by, self.approver)
            self.sod_check_status = "Passed" if passed else "Failed"
            self.sod_check_message = message
            if not passed:
                frappe.throw(message, frappe.PermissionError)
        if self.decision in {"Approved", "Rejected", "Returned"} and self.evidence_required:
            require_evidence(self)
            self.evidence_complete = 1

    def on_update(self):
        if self.decision != "Pending" and not self.decision_on:
            self.decision_on = now_datetime()
