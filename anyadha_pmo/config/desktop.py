"""Desktop configuration and synchronization for Anyadha PMO."""

import frappe


def sync_pmo_desktop_icons():
    """Synchronize Desktop Icons for public Anyadha PMO workspaces."""

    workspaces = frappe.get_all(
        "Workspace",
        filters={
            "app": "anyadha_pmo",
            "public": 1,
            "type": "Workspace",
        },
        fields=["name", "icon"],
        order_by="sequence_id asc, name asc",
    )

    for workspace in workspaces:
        icon_name = frappe.db.exists(
            "Desktop Icon",
            {
                "label": workspace.name,
                "link_type": "Workspace Sidebar",
                "link_to": workspace.name,
                "icon_type": "Link",
            },
        )

        if icon_name:
            icon = frappe.get_doc("Desktop Icon", icon_name)

            changed = False

            if icon.icon != workspace.icon:
                icon.icon = workspace.icon
                changed = True

            if icon.hidden:
                icon.hidden = 0
                changed = True

            if changed:
                icon.save(ignore_permissions=True)

        else:
            icon = frappe.get_doc(
                {
                    "doctype": "Desktop Icon",
                    "label": workspace.name,
                    "icon_type": "Link",
                    "link_type": "Workspace Sidebar",
                    "link_to": workspace.name,
                    "icon": workspace.icon,
                    "standard": 0,
                    "hidden": 0,
                }
            )
            icon.insert(ignore_permissions=True)
