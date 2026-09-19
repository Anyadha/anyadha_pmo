import frappe
from frappe.model.document import Document
from anyadha_pmo.core.services.governance import validate_governance_scope
class PMOControl(Document):
    def validate(self):
        validate_governance_scope(self)
        if self.key_control and not self.control_owner and not self.responsible_employee:
            frappe.throw("A key control must have a Control Owner or Responsible Employee.")
