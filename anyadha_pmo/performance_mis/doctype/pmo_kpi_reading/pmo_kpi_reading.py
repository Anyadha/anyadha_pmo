import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, now_datetime
from anyadha_pmo.core.services.metrics import achievement_percent


class PMOKPIReading(Document):
    def validate(self):
        if self.period and not str(self.period).strip():
            frappe.throw("Period cannot be blank")
        kpi = frappe.db.get_value("PMO KPI", self.kpi, ["direction"], as_dict=True)
        direction = kpi.direction if kpi else "Higher is Better"
        if self.actual_value is not None and self.target_value not in (None, 0):
            self.achievement_percent = achievement_percent(flt(self.actual_value), flt(self.target_value), direction)
        if self.status == "Validated":
            if not self.validated_by:
                self.validated_by = frappe.session.user
            if not self.validated_on:
                self.validated_on = now_datetime()
            if frappe.db.get_single_value("PMO Settings", "require_evidence_for_approval") and not self.evidence:
                frappe.throw("Evidence is required for a validated KPI reading")
