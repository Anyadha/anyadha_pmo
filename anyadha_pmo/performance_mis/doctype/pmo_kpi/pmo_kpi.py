import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class PMOKPI(Document):
    def validate(self):
        if self.effective_from and self.effective_to and getdate(self.effective_to) < getdate(self.effective_from):
            frappe.throw("Effective To cannot be before Effective From")
        if self.direction == "Target Range" and not self.unit:
            frappe.throw("Unit is required when Performance Direction is Target Range")
