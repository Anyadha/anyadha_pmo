"""Lightweight diagnostic APIs for Anyadha PMO."""

from __future__ import annotations

import frappe


@frappe.whitelist()
def health_check() -> dict:
    """Return basic app/site health information for administrators."""
    frappe.only_for("System Manager")
    return {
        "app": "anyadha_pmo",
        "status": "ok",
        "site": frappe.local.site,
        "frappe_version": frappe.get_attr("frappe.__version__"),
    }


@frappe.whitelist()
def architecture_summary() -> dict:
    """Return installed PMO module and DocType counts."""
    frappe.only_for("System Manager")

    modules = frappe.get_all(
        "Module Def",
        filters={"app_name": "anyadha_pmo"},
        pluck="name",
    )

    doctypes = frappe.get_all(
        "DocType",
        filters={"module": ["in", modules]},
        pluck="name",
    ) if modules else []

    return {
        "modules": len(modules),
        "doctypes": len(doctypes),
        "module_names": sorted(modules),
    }
