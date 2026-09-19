import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import require_attachment
class PMORiskAssessment(Document):
    def validate(self):
        if self.inherent_probability and self.inherent_impact:
            self.inherent_score={'Low':1,'Medium':2,'High':3,'Critical':4}.get(self.inherent_probability,0)*{'Low':1,'Medium':2,'High':3,'Critical':4}.get(self.inherent_impact,0)
        if self.residual_probability and self.residual_impact:
            self.residual_score={'Low':1,'Medium':2,'High':3,'Critical':4}.get(self.residual_probability,0)*{'Low':1,'Medium':2,'High':3,'Critical':4}.get(self.residual_impact,0)
        if self.is_current and not self.assessor: frappe.throw("Assessor is required for a current risk assessment.")
