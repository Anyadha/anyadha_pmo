import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope, require_attachment
class PMODocumentControl(Document):
    def validate(self):
        validate_governance_scope(self)
        if self.approval_status == "Approved":
            require_attachment(self, "evidence", True, "The approved document attachment is required before approval.")
        if self.review_date and frappe.utils.getdate(self.review_date) < frappe.utils.getdate(frappe.utils.today()) and self.approval_status == "Approved":
            # Existing documents may be overdue; do not block historical migration.
            pass
