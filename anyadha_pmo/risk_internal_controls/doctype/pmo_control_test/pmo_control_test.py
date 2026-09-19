import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import require_attachment, prevent_self_verification
class PMOControlTest(Document):
    def validate(self):
        if self.exceptions_count and self.exceptions_count > 0 and self.test_conclusion == "Pass":
            frappe.throw("A control test with exceptions cannot have a Pass conclusion.")
        if self.evidence_required:
            require_attachment(self, "evidence", True, "Evidence is required for this control test.")
        prevent_self_verification(self, ("tester",), "verified_by")
