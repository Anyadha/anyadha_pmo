import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope, require_attachment, prevent_self_verification
class PMOAuditFinding(Document):
    def validate(self):
        validate_governance_scope(self)
        if self.status in ("Completed", "Closed") and not self.management_response:
            frappe.throw("Management Response is required before closing an audit finding.")
        if self.status == "Closed" and self.target_closure_date and frappe.utils.getdate(self.target_closure_date) > frappe.utils.getdate(frappe.utils.today()):
            frappe.throw("An audit finding cannot be closed before its target closure date.")
