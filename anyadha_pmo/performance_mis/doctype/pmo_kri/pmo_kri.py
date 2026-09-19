import frappe
from frappe.model.document import Document
from frappe.utils import flt
from anyadha_pmo.core.services.metrics import threshold_status


class PMOKRI(Document):
    def validate(self):
        if self.current_value is not None and self.threshold is not None:
            self.status = threshold_status(flt(self.current_value), flt(self.threshold), self.direction or "Higher is Worse")
