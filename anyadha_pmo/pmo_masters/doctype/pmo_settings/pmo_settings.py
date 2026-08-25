import frappe
from frappe.model.document import Document


class PMOSettings(Document):
    def validate(self):
        if self.approval_escalation_days is not None and self.approval_escalation_days < 0:
            frappe.throw("Approval Escalation Days cannot be negative.")
        if self.compliance_reminder_days is not None and self.compliance_reminder_days < 0:
            frappe.throw("Compliance Reminder Days cannot be negative.")
        if self.risk_review_days is not None and self.risk_review_days < 0:
            frappe.throw("Risk Review Days cannot be negative.")
