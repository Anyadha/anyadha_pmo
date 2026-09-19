import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope, require_attachment, prevent_self_verification
class PMOComplianceItem(Document):
    def validate(self):
        validate_governance_scope(self)
        if self.compliance_status == "Compliant" and self.evidence_required:
            require_attachment(self, "evidence", True, "Evidence is required to mark a compliance item Compliant.")
        if self.verification_status == "Verified" and not self.verified_by:
            frappe.throw("Verified By is required when verification status is Verified.")
        prevent_self_verification(self, ("responsible",), "verified_by")
