import frappe
from frappe.model.document import Document


class PMOProjectBudget(Document):
    def validate(self):
        for field in ("approved_amount", "revised_amount", "utilized_amount"):
            value = getattr(self, field, None)
            if value is not None and value < 0:
                frappe.throw(f"{field.replace('_',' ').title()} cannot be negative.")
        approved = self.approved_amount or 0
        revised = self.revised_amount if self.revised_amount is not None else approved
        utilized = self.utilized_amount or 0
        self.variance = revised - utilized
        self.variance_percent = ((self.variance / revised) * 100) if revised else 0
