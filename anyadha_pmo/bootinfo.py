


import frappe


def extend_bootinfo(bootinfo):
    user = frappe.session.user

    role_profile = frappe.db.get_value(
        "User",
        user,
        "role_profile_name",
    )

    # Preserve the existing PMO bootinfo field.
    bootinfo["anyadha_role_profile"] = role_profile

    # Restrict app tiles only for Field Coordinator - Agri.
    if role_profile != "Field Coordinator - Agri":
        return

    hidden_apps = {"erpnext", "india_compliance"}

    app_data = bootinfo.get("app_data") or []

    bootinfo["app_data"] = [
        app
        for app in app_data
        if app.get("app_name") not in hidden_apps
    ]

