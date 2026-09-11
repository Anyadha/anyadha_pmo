import frappe


class PurchaseOrderPortalMixin:
    def has_website_permission(self, ptype="read", user=None, verbose=False):
        user = user or frappe.session.user

        if ptype != "read":
            return False

        if self.docstatus != 1:
            return False

        return bool(
            frappe.db.exists(
                "Portal User",
                {
                    "user": user,
                    "parenttype": "Supplier",
                    "parent": self.supplier,
                },
            )
        )
