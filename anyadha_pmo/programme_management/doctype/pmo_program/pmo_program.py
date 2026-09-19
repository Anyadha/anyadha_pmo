import frappe
from frappe.model.document import Document


class PMOProgram(Document):
    def _sync_status_from_workflow(self):
        if getattr(self, "workflow_state", None) and hasattr(self, "status"):
            self.status = self.workflow_state

    def validate(self):
        self._sync_status_from_workflow()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            frappe.throw("End Date cannot be earlier than Start Date.")
        if self.approved_budget is not None and self.approved_budget < 0:
            frappe.throw("Approved Budget cannot be negative.")
        if self.portfolio and frappe.db.exists("PMO Portfolio", self.portfolio):
            portfolio = frappe.db.get_value("PMO Portfolio", self.portfolio, ["company", "entity", "business_unit"], as_dict=True)
            for field in ("company", "entity", "business_unit"):
                if getattr(self, field, None) and portfolio.get(field) and getattr(self, field) != portfolio.get(field):
                    frappe.throw(f"Programme {field.replace('_',' ').title()} must match the selected Portfolio.")
