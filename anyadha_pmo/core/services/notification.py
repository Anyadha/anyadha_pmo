"""Central notification entry points for PMO workflows."""
from __future__ import annotations

import frappe

from anyadha_pmo.core.services.settings import is_enabled


def notify_user(user: str, subject: str, message: str):
    if not user or not is_enabled("enable_notifications", True):
        return
    frappe.sendmail(recipients=[user], subject=subject, message=message, now=False)
