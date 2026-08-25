import frappe
from frappe.tests.utils import FrappeTestCase


class TestPMOSettings(FrappeTestCase):
    def test_single_settings_exists(self):
        settings = frappe.get_single("PMO Settings")
        self.assertEqual(settings.doctype, "PMO Settings")
