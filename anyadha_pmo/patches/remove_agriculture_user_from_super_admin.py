import frappe


def execute():
    profile_name = "Super Admin"
    role_to_remove = "Agriculture User"

    if not frappe.db.exists("Role Profile", profile_name):
        return

    profile = frappe.get_doc("Role Profile", profile_name)

    original_count = len(profile.roles)
    profile.roles = [
        row for row in profile.roles
        if row.role != role_to_remove
    ]

    if len(profile.roles) != original_count:
        profile.save(ignore_permissions=True)
