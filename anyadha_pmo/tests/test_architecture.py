from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPMOArchitecture(FrappeTestCase):
    """Fast smoke tests for the installed PMO application."""

    def test_pmo_settings_exists(self):
        self.assertTrue(frappe.db.exists("DocType", "PMO Settings"))

    def test_core_masters_exist(self):
        for doctype in (
            "PMO Entity",
            "PMO Business Unit",
            "PMO Project Type",
            "PMO Project Category",
            "PMO Risk Category",
        ):
            self.assertTrue(
                frappe.db.exists("DocType", doctype),
                f"Missing expected PMO master: {doctype}",
            )

    def test_governance_doctypes_exist(self):
        for doctype in (
            "PMO Approval Request",
            "PMO Authority Matrix",
            "PMO Board Meeting",
            "PMO Governance Action",
        ):
            self.assertTrue(
                frappe.db.exists("DocType", doctype),
                f"Missing expected Governance DocType: {doctype}",
            )
