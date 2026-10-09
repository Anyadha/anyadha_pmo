import frappe


def execute():
    profile_name = "Super Admin"

    if not frappe.db.exists("Role Profile", profile_name):
        return

    profile = frappe.get_doc("Role Profile", profile_name)

    if profile.roles:
        profile.roles = []
        profile.save(ignore_permissions=True)
