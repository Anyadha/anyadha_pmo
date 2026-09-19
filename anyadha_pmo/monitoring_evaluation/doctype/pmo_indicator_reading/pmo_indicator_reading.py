import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class PMOIndicatorReading(Document):
    def validate(self):
        if self.validation_status == "Validated":
            if not self.validated_by:
                self.validated_by = frappe.session.user
            if not self.validated_on:
                self.validated_on = now_datetime()
