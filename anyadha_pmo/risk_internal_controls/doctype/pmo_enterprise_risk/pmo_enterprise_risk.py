import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope

LEVELS={"Low":1,"Medium":2,"High":3,"Critical":4}
class PMOEnterpriseRisk(Document):
    def validate(self):
        validate_governance_scope(self)
        p=self.residual_probability or self.probability
        i=self.residual_impact or self.impact
        if p and i: self.score=LEVELS.get(p,0)*LEVELS.get(i,0)
        if self.risk_response and self.risk_response != "Accept" and not self.treatment_plan and self.status not in ("Closed","Cancelled"):
            frappe.throw("A risk treatment is required for risks not accepted.")
