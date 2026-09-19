"""Supplier-only website access for submitted Purchase Orders."""

import frappe


class PurchaseOrderPortalMixin:
	"""Allow a supplier portal user to read only that supplier's submitted POs.

	Frappe calls a document controller's ``has_website_permission`` method before
	the generic website-permission hooks.  This intentionally applies only to the
	website read path; it does not grant Desk, write, submit, or cancel access.
	"""

	def has_website_permission(self, ptype="read", user=None, verbose=False):
		if ptype != "read" or self.docstatus != 1:
			return False

		user = user or frappe.session.user
		if user == "Guest":
			return False

		return bool(
			frappe.db.exists(
				"Portal User",
				{
					"parenttype": "Supplier",
					"parent": self.supplier,
					"user": user,
				},
			)
		)
