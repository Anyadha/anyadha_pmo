from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

from anyadha_pmo.core.services.evidence import require_evidence
from anyadha_pmo.core.services.scope import validate_scope
from anyadha_pmo.core.services.sod import check_maker_checker


class PMOApprovalRequest(Document):
    def before_insert(self):
        self.requested_by = self.requested_by or frappe.session.user
        self.requested_on = self.requested_on or now_datetime()
        self.status = self.status or "Draft"
        self.final_decision = self.final_decision or "Pending"
        self.current_sequence = self.current_sequence or 1

    def validate(self):
        validate_scope(self)
        if self.reference_doctype and self.reference_name:
            if not frappe.db.exists(self.reference_doctype, self.reference_name):
                frappe.throw("The approval reference document does not exist.")
        if self.approval_amount is not None and self.approval_amount < 0:
            frappe.throw("Approval Amount cannot be negative.")
        if self.evidence_required:
            require_evidence(self)
            self.evidence_complete = 1
        if self.override_used and not self.override_reason:
            frappe.throw("Override Reason is mandatory when an override is used.")
        self._validate_steps()

    def _validate_steps(self):
        steps = frappe.get_all(
            "PMO Approval Step",
            filters={"approval_request": self.name},
            fields=["name", "approver", "sequence", "decision"],
            order_by="sequence asc",
        )
        for step in steps:
            if step.approver and self.requested_by:
                passed, message = check_maker_checker(self.requested_by, step.approver)
                if not passed:
                    frappe.throw(message)

    def before_save(self):
        state_to_status = {
            "Draft": "Draft",
            "Open": "Open",
            "Pending Approval": "Pending Approval",
            "Approved": "Approved",
            "Rejected": "Rejected",
            "Closed": "Closed",
            "Cancelled": "Cancelled",
        }
        if self.workflow_state in state_to_status:
            self.status = state_to_status[self.workflow_state]
        if self.status in {"Approved", "Rejected", "Closed", "Cancelled"} and not self.completed_on:
            self.completed_on = now_datetime()
        if self.status == "Approved":
            self.final_decision = "Approved"
        elif self.status == "Rejected":
            self.final_decision = "Rejected"
