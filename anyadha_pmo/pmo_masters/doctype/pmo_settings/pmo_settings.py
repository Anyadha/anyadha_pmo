from __future__ import annotations

import frappe
from frappe.model.document import Document

from anyadha_pmo.core.validation import ensure_date_order, require_non_negative


class PMOSettings(Document):
    def validate(self):
        require_non_negative(
            self,
            "approval_escalation_days",
            "compliance_reminder_days",
            "risk_review_days",
            "audit_retention_days",
            "dashboard_refresh_minutes",
        )
        ensure_date_order(self, "effective_from", "effective_to")
        if self.dashboard_refresh_minutes and self.dashboard_refresh_minutes < 1:
            frappe.throw("Dashboard Refresh Minutes must be at least 1.")
        if self.audit_retention_days and self.audit_retention_days < 365:
            frappe.throw("Audit Retention Days must be at least 365.")
        if self.allow_admin_override:
            frappe.msgprint("Admin override is enabled; every override must carry a reason.", alert=True)
