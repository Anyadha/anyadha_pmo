import frappe

from anyadha_pmo.security.roles import PMO_ROLES


def ensure_roles():
    """Create PMO roles if they do not already exist.

    Existing roles are never overwritten. This makes installation and
    migration idempotent and safe for an already-running site.
    """
    for role_name, desk_access in PMO_ROLES:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc(
                {
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": desk_access,
                }
            ).insert(ignore_permissions=True)

    frappe.db.commit()


def after_install():
    ensure_roles()


def after_migrate():
    ensure_roles()
