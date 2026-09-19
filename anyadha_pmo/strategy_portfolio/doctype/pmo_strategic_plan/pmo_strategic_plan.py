import frappe
from frappe.model.document import Document


class PMOStrategicPlan(Document):
    def _sync_status_from_workflow(self):
        if getattr(self, "workflow_state", None) and hasattr(self, "status"):
            self.status = self.workflow_state

    def validate(self):
        self._sync_status_from_workflow()
        if self.period_from and self.period_to and self.period_from > self.period_to:
            frappe.throw("Period To cannot be earlier than Period From.")
        if self.version is not None and self.version < 1:
            frappe.throw("Version must be at least 1.")
        if self.status == "Approved" and not self.approved_by:
            frappe.throw("Approved By is required when the Strategic Plan is Approved.")
