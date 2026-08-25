import frappe

ROLES = [
    ("PMO Administrator", 1),
    ("PMO Head", 0),
    ("Programme Manager", 0),
    ("Project Manager", 0),
    ("PMO Officer", 0),
    ("M&E Manager", 0),
    ("M&E Officer", 0),
    ("Grants Manager", 0),
    ("CSR Manager", 0),
    ("Compliance Officer", 0),
    ("Internal Auditor", 0),
    ("Executive / Management", 0),
    ("Board Member", 0),
]


def ensure_roles():
    for role_name, desk_access in ROLES:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": desk_access,
            }).insert(ignore_permissions=True)
    frappe.db.commit()


def after_install():
    ensure_roles()


def after_migrate():
    ensure_roles()
