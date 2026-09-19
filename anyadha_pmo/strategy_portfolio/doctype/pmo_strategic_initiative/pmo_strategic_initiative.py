import frappe
from frappe.model.document import Document


class PMOStrategicInitiative(Document):
    def _sync_status_from_workflow(self):
        if getattr(self, "workflow_state", None) and hasattr(self, "status"):
            self.status = self.workflow_state

    def validate(self):
        self._sync_status_from_workflow()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            frappe.throw("End Date cannot be earlier than Start Date.")
