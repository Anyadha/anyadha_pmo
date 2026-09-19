import frappe
from frappe.model.document import Document


class PMOProject(Document):
    def _sync_status_from_workflow(self):
        if getattr(self, "workflow_state", None) and hasattr(self, "status"):
            self.status = self.workflow_state

    def validate(self):
        self._sync_status_from_workflow()
        self._validate_dates()
        self._validate_amounts()
        self._validate_hierarchy()
        self._validate_erpnext_project()

    def _validate_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            frappe.throw("End Date cannot be earlier than Start Date.")

    def _validate_amounts(self):
        if self.approved_budget is not None and self.approved_budget < 0:
            frappe.throw("Approved Budget cannot be negative.")
        if self.actual_cost is not None and self.actual_cost < 0:
            frappe.throw("Actual Cost cannot be negative.")
        if self.percent_complete is not None and not 0 <= self.percent_complete <= 100:
            frappe.throw("Percent Complete must be between 0 and 100.")

    def _validate_hierarchy(self):
        if self.program and frappe.db.exists("PMO Program", self.program):
            parent = frappe.db.get_value("PMO Program", self.program, ["company", "entity", "business_unit", "portfolio"], as_dict=True)
            for field in ("company", "entity", "business_unit"):
                if getattr(self, field, None) and parent.get(field) and getattr(self, field) != parent.get(field):
                    frappe.throw(f"Project {field.replace('_',' ').title()} must match the selected Programme.")
            if self.portfolio and parent.get("portfolio") and self.portfolio != parent.get("portfolio"):
                frappe.throw("Project Portfolio must match the Programme Portfolio.")

        if self.portfolio and frappe.db.exists("PMO Portfolio", self.portfolio):
            parent = frappe.db.get_value("PMO Portfolio", self.portfolio, ["company", "entity", "business_unit"], as_dict=True)
            for field in ("company", "entity", "business_unit"):
                if getattr(self, field, None) and parent.get(field) and getattr(self, field) != parent.get(field):
                    frappe.throw(f"Project {field.replace('_',' ').title()} must match the selected Portfolio.")

    def _validate_erpnext_project(self):
        if not self.erpnext_project or not frappe.db.exists("Project", self.erpnext_project):
            return
        erp_company = frappe.db.get_value("Project", self.erpnext_project, "company")
        if self.company and erp_company and self.company != erp_company:
            frappe.throw("PMO Project Company must match the linked ERPNext Project Company.")
