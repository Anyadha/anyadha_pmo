import frappe
from frappe.model.document import Document
from frappe.utils import getdate


class PMOKPITarget(Document):
    def validate(self):
        if self.period_start and self.period_end and getdate(self.period_end) < getdate(self.period_start):
            frappe.throw("Period End cannot be before Period Start")
