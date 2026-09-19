"""Reporting-layer service helpers. Query Reports remain the source for current MIS data."""

import frappe


def kpi_performance(kpi=None, period=None, company=None):
    filters = {}
    if kpi:
        filters["kpi"] = kpi
    if period:
        filters["period"] = period
    if company:
        filters["company"] = company
    return frappe.get_all(
        "PMO KPI Reading",
        filters=filters,
        fields=["name", "kpi", "period", "actual_value", "target_value", "achievement_percent", "status", "reading_date"],
        order_by="reading_date desc",
    )


def management_snapshot(period=None, company=None):
    filters = {}
    if period:
        filters["period"] = period
    if company:
        filters["company"] = company
    return frappe.get_all(
        "PMO Management Review",
        filters=filters,
        fields=["name", "review_title", "review_date", "period", "status", "decision", "action_required"],
        order_by="review_date desc",
    )
