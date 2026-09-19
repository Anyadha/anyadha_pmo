import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope
class PMOComplianceObligation(Document):
    def validate(self):
        validate_governance_scope(self)
        if self.effective_from and self.effective_to and self.effective_to < self.effective_from:
            frappe.throw("Effective To cannot be before Effective From.")
        if self.status == "Active" and not self.obligation_owner:
            frappe.throw("An active compliance obligation must have an Obligation Owner.")
