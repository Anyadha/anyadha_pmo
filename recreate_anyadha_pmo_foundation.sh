#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d "anyadha_pmo" || ! -f "pyproject.toml" ]]; then
  echo "ERROR: Run this script from the root of the anyadha_pmo repository."
  exit 1
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP=".recreate_backup_${STAMP}"
mkdir -p "$BACKUP"

backup_if_exists() {
  local f="$1"
  if [[ -e "$f" ]]; then
    mkdir -p "$BACKUP/$(dirname "$f")"
    cp -R "$f" "$BACKUP/$f"
  fi
}

for f in pyproject.toml setup.py anyadha_pmo/hooks.py anyadha_pmo/modules.txt anyadha_pmo/patches.txt anyadha_pmo/install.py anyadha_pmo/config/desktop.py anyadha_pmo/config/docs.py; do backup_if_exists "$f"; done

mkdir -p anyadha_pmo/config anyadha_pmo/fixtures anyadha_pmo/public/css anyadha_pmo/public/js anyadha_pmo/templates/includes anyadha_pmo/www anyadha_pmo/tests anyadha_pmo/api anyadha_pmo/overrides anyadha_pmo/pmo_masters/doctype/pmo_settings anyadha_pmo/workspace anyadha_pmo/workspace_sidebar

touch anyadha_pmo/config/__init__.py anyadha_pmo/tests/__init__.py anyadha_pmo/api/__init__.py anyadha_pmo/overrides/__init__.py

cat > pyproject.toml <<'PYPROJECT'
[project]
name = "anyadha_pmo"
version = "2.1.0"
authors = [{ name = "Anyadha", email = "info@anyadha.com" }]
description = "Anyadha Enterprise PMO - Governance, Strategy, Programme, Project, M&E, Grants, CSR, Risk, Compliance, Audit and MIS"
requires-python = ">=3.14,<3.15"
readme = "README.md"
license = { file = "license.txt" }
dependencies = []

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[tool.bench.frappe-dependencies]
frappe = ">=16.0.0-dev,<17.0.0"
erpnext = ">=16.0.0-dev,<17.0.0"

[tool.ruff]
line-length = 110
target-version = "py314"
PYPROJECT

cat > setup.py <<'SETUP'
from setuptools import setup

setup(name="anyadha_pmo", version="2.1.0")
SETUP

cat > anyadha_pmo/hooks.py <<'HOOKS'
app_name = "anyadha_pmo"
app_title = "Anyadha PMO"
app_publisher = "Anyadha"
app_description = (
    "Anyadha Enterprise PMO - Governance, Strategy, Programme, Project, "
    "M&E, Grants, CSR, Risk, Compliance, Audit and MIS"
)
app_email = "info@anyadha.com"
app_license = "MIT"
app_version = "2.1.0"

required_apps = ["erpnext"]

after_install = "anyadha_pmo.install.after_install"
after_migrate = "anyadha_pmo.install.after_migrate"
HOOKS

cat > anyadha_pmo/modules.txt <<'MODULES'
PMO Masters
Governance
Strategy Portfolio
Proposal DPR
Programme Management
Project Management
Monitoring Evaluation
Grants Donor Management
CSR Management
Risk Internal Controls
Compliance Regulatory
Audit Assurance
SOP Document Control
Performance MIS
MODULES

cat > anyadha_pmo/patches.txt <<'PATCHES'
[post_model_sync]
PATCHES

cat > anyadha_pmo/config/desktop.py <<'PY'
"""Desktop configuration for Anyadha PMO.

Frappe v16 builds the desktop/app experience from public Workspaces.
Navigation is authored through Workspace and Workspace Sidebar records.
"""
PY
cat > anyadha_pmo/config/docs.py <<'PY'
"""Documentation configuration for Anyadha PMO."""
PY

cat > anyadha_pmo/install.py <<'PY'
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
PY

cat > anyadha_pmo/pmo_masters/doctype/pmo_settings/__init__.py <<'PY'
PY
cat > anyadha_pmo/pmo_masters/doctype/pmo_settings/pmo_settings.py <<'PY'
import frappe
from frappe.model.document import Document


class PMOSettings(Document):
    def validate(self):
        if self.approval_escalation_days is not None and self.approval_escalation_days < 0:
            frappe.throw("Approval Escalation Days cannot be negative.")
        if self.compliance_reminder_days is not None and self.compliance_reminder_days < 0:
            frappe.throw("Compliance Reminder Days cannot be negative.")
        if self.risk_review_days is not None and self.risk_review_days < 0:
            frappe.throw("Risk Review Days cannot be negative.")
PY

cat > anyadha_pmo/pmo_masters/doctype/pmo_settings/pmo_settings.json <<'JSON'
{
  "actions": [],
  "allow_rename": 0,
  "autoname": "PMO Settings",
  "creation": "2026-08-25 00:00:00.000000",
  "doctype": "DocType",
  "editable_grid": 1,
  "engine": "InnoDB",
  "field_order": [
    "general_section", "enable_pmo", "default_company", "default_pmo_entity", "default_business_unit", "default_project_type",
    "defaults_section", "default_fiscal_year", "default_currency",
    "naming_section", "project_naming_series", "programme_naming_series", "proposal_naming_series", "dpr_naming_series", "risk_naming_series", "audit_naming_series", "compliance_naming_series", "sop_naming_series",
    "workflow_section", "enable_workflows", "approval_escalation_days",
    "notification_section", "enable_notifications", "compliance_reminder_days", "risk_review_days",
    "security_section", "enforce_company_restrictions", "enforce_entity_restrictions", "require_sensitive_record_approval", "enable_maker_checker",
    "reporting_section", "enable_executive_dashboard", "enable_management_dashboard", "default_reporting_frequency"
  ],
  "fields": [
    {"fieldname":"general_section","fieldtype":"Section Break","label":"General"},
    {"default":"1","fieldname":"enable_pmo","fieldtype":"Check","label":"Enable PMO"},
    {"fieldname":"default_company","fieldtype":"Link","label":"Default Company","options":"Company"},
    {"fieldname":"default_pmo_entity","fieldtype":"Link","label":"Default PMO Entity","options":"PMO Entity"},
    {"fieldname":"default_business_unit","fieldtype":"Link","label":"Default Business Unit","options":"PMO Business Unit"},
    {"fieldname":"default_project_type","fieldtype":"Link","label":"Default Project Type","options":"PMO Project Type"},
    {"fieldname":"defaults_section","fieldtype":"Section Break","label":"Defaults"},
    {"fieldname":"default_fiscal_year","fieldtype":"Link","label":"Default Fiscal Year","options":"Fiscal Year"},
    {"fieldname":"default_currency","fieldtype":"Link","label":"Default Currency","options":"Currency"},
    {"fieldname":"naming_section","fieldtype":"Section Break","label":"Naming"},
    {"default":"PROJ-.YYYY.-.#####","fieldname":"project_naming_series","fieldtype":"Data","label":"Project Naming Series"},
    {"default":"PROG-.YYYY.-.#####","fieldname":"programme_naming_series","fieldtype":"Data","label":"Programme Naming Series"},
    {"default":"PROP-.YYYY.-.#####","fieldname":"proposal_naming_series","fieldtype":"Data","label":"Proposal Naming Series"},
    {"default":"DPR-.YYYY.-.#####","fieldname":"dpr_naming_series","fieldtype":"Data","label":"DPR Naming Series"},
    {"default":"RISK-.YYYY.-.#####","fieldname":"risk_naming_series","fieldtype":"Data","label":"Risk Naming Series"},
    {"default":"AUD-.YYYY.-.#####","fieldname":"audit_naming_series","fieldtype":"Data","label":"Audit Naming Series"},
    {"default":"COMP-.YYYY.-.#####","fieldname":"compliance_naming_series","fieldtype":"Data","label":"Compliance Naming Series"},
    {"default":"SOP-.YYYY.-.#####","fieldname":"sop_naming_series","fieldtype":"Data","label":"SOP Naming Series"},
    {"fieldname":"workflow_section","fieldtype":"Section Break","label":"Workflow"},
    {"default":"1","fieldname":"enable_workflows","fieldtype":"Check","label":"Enable Workflows"},
    {"default":"3","fieldname":"approval_escalation_days","fieldtype":"Int","label":"Approval Escalation Days"},
    {"fieldname":"notification_section","fieldtype":"Section Break","label":"Notifications"},
    {"default":"1","fieldname":"enable_notifications","fieldtype":"Check","label":"Enable Notifications"},
    {"default":"7","fieldname":"compliance_reminder_days","fieldtype":"Int","label":"Compliance Reminder Days"},
    {"default":"30","fieldname":"risk_review_days","fieldtype":"Int","label":"Risk Review Days"},
    {"fieldname":"security_section","fieldtype":"Section Break","label":"Security"},
    {"default":"1","fieldname":"enforce_company_restrictions","fieldtype":"Check","label":"Enforce Company Restrictions"},
    {"default":"1","fieldname":"enforce_entity_restrictions","fieldtype":"Check","label":"Enforce PMO Entity Restrictions"},
    {"fieldname":"require_sensitive_record_approval","fieldtype":"Check","label":"Require Sensitive Record Approval"},
    {"fieldname":"enable_maker_checker","fieldtype":"Check","label":"Enable Maker Checker"},
    {"fieldname":"reporting_section","fieldtype":"Section Break","label":"Reporting"},
    {"default":"1","fieldname":"enable_executive_dashboard","fieldtype":"Check","label":"Enable Executive Dashboard"},
    {"default":"1","fieldname":"enable_management_dashboard","fieldtype":"Check","label":"Enable Management Dashboard"},
    {"default":"Monthly","fieldname":"default_reporting_frequency","fieldtype":"Select","label":"Default Reporting Frequency","options":"Weekly\nMonthly\nQuarterly\nHalf-Yearly\nAnnual"}
  ],
  "index_web_pages_for_search": 0,
  "issingle": 1,
  "istable": 0,
  "module": "PMO Masters",
  "name": "PMO Settings",
  "permissions": [
    {"create":1,"delete":1,"email":1,"export":1,"print":1,"read":1,"role":"PMO Administrator","share":1,"write":1},
    {"read":1,"write":1,"role":"PMO Head"}
  ],
  "sort_field": "modified",
  "sort_order": "DESC",
  "states": [],
  "title_field": "name"
}
JSON

cat > anyadha_pmo/tests/test_pmo_settings.py <<'PY'
import frappe
from frappe.tests.utils import FrappeTestCase


class TestPMOSettings(FrappeTestCase):
    def test_single_settings_exists(self):
        settings = frappe.get_single("PMO Settings")
        self.assertEqual(settings.doctype, "PMO Settings")
PY

cat > README.md <<'README'
# Anyadha PMO

Anyadha Enterprise PMO application for Frappe Framework v16+ and ERPNext v16+.

## Business modules

1. PMO Masters
2. Governance
3. Strategy Portfolio
4. Proposal DPR
5. Programme Management
6. Project Management
7. Monitoring Evaluation
8. Grants Donor Management
9. CSR Management
10. Risk Internal Controls
11. Compliance Regulatory
12. Audit Assurance
13. SOP Document Control
14. Performance MIS

The existing PMO DocTypes are preserved. Foundation work is separated from business-process implementation.

## v16 navigation

Public Workspaces are shipped under `anyadha_pmo/workspace/`.
Curated v16 Workspace Sidebar records are shipped under `anyadha_pmo/workspace_sidebar/`.

## Dependencies

ERPNext is required. India Compliance, HRMS, Raven, Agriculture and other apps remain optional integrations.
README

# Generate minimal, valid public Workspace records. Sidebar records are generated in a
# separate v16-native folder and contain only links to existing DocTypes.
python3 - <<'PY'
import json
from pathlib import Path

root = Path("anyadha_pmo")
wr = root / "workspace"
sr = root / "workspace_sidebar"

workspaces = [
    ("Executive PMO", "PMO Masters", "chart-line"),
    ("Strategy & Portfolio", "Strategy Portfolio", "target"),
    ("Programme & Projects", "Project Management", "kanban"),
    ("Monitoring & Evaluation", "Monitoring Evaluation", "chart-column"),
    ("Grants & Donor Management", "Grants Donor Management", "handshake"),
    ("CSR Management", "CSR Management", "heart"),
    ("Governance", "Governance", "landmark"),
    ("Risk & Compliance", "Risk Internal Controls", "shield-check"),
    ("Audit & Assurance", "Audit Assurance", "clipboard-check"),
    ("SOP & Document Control", "SOP Document Control", "file-check"),
    ("Performance MIS", "Performance MIS", "chart-no-axes-combined"),
]

links = {
    "Executive PMO": [("PMO Project", "Projects"), ("PMO Program", "Programmes"), ("PMO Portfolio", "Portfolios"), ("PMO Enterprise Risk", "Enterprise Risks"), ("PMO KPI", "KPIs")],
    "Strategy & Portfolio": [("PMO Strategic Plan", "Strategic Plans"), ("PMO Strategic Initiative", "Strategic Initiatives"), ("PMO Portfolio", "Portfolios"), ("PMO Portfolio Project", "Portfolio Projects")],
    "Programme & Projects": [("PMO Program", "Programmes"), ("PMO Project", "Projects"), ("PMO Project Milestone", "Milestones"), ("PMO Project Deliverable", "Deliverables"), ("PMO Project Issue", "Issues"), ("PMO Change Request", "Change Requests"), ("PMO Risk", "Project Risks")],
    "Monitoring & Evaluation": [("PMO M and E Framework", "M&E Frameworks"), ("PMO Indicator", "Indicators"), ("PMO Target", "Targets"), ("PMO Monitoring Plan", "Monitoring Plans"), ("PMO Monitoring Visit", "Monitoring Visits"), ("PMO Evaluation", "Evaluations")],
    "Grants & Donor Management": [("PMO Donor", "Donors"), ("PMO Grant", "Grants"), ("PMO Grant Agreement", "Grant Agreements"), ("PMO Grant Budget", "Grant Budgets"), ("PMO Grant Utilization", "Grant Utilization"), ("PMO Fund Reconciliation", "Fund Reconciliation")],
    "CSR Management": [("PMO CSR Partner", "CSR Partners"), ("PMO CSR Project", "CSR Projects"), ("PMO CSR Proposal", "CSR Proposals"), ("PMO CSR Budget", "CSR Budgets"), ("PMO CSR Utilization", "CSR Utilization")],
    "Governance": [("PMO Governance Body", "Governance Bodies"), ("PMO Board Meeting", "Board Meetings"), ("PMO Board Decision", "Board Decisions"), ("PMO Authority Matrix", "Authority Matrix"), ("PMO Approval Request", "Approval Requests")],
    "Risk & Compliance": [("PMO Enterprise Risk", "Enterprise Risks"), ("PMO Risk Assessment", "Risk Assessments"), ("PMO Risk Treatment", "Risk Treatments"), ("PMO Control", "Controls"), ("PMO Control Test", "Control Tests"), ("PMO Compliance Item", "Compliance Items"), ("PMO Non Compliance", "Non-Compliance")],
    "Audit & Assurance": [("PMO Audit Plan", "Audit Plans"), ("PMO Audit Engagement", "Audit Engagements"), ("PMO Audit Finding", "Audit Findings"), ("PMO Audit Action", "Audit Actions"), ("PMO Audit Report", "Audit Reports")],
    "SOP & Document Control": [("PMO SOP", "SOPs"), ("PMO Policy", "Policies"), ("PMO Document Control", "Controlled Documents"), ("PMO Document Version", "Document Versions"), ("PMO Document Review", "Document Reviews"), ("PMO Record Retention Rule", "Retention Rules")],
    "Performance MIS": [("PMO KPI", "KPIs"), ("PMO KPI Target", "KPI Targets"), ("PMO KPI Reading", "KPI Readings"), ("PMO KRI", "KRIs"), ("PMO KCI", "KCIs"), ("PMO Performance Review", "Performance Reviews"), ("PMO MIS Snapshot", "MIS Snapshots")],
}

for idx, (label, module, icon) in enumerate(workspaces, 1):
    slug = ''.join(c for c in label.lower().replace('&', 'and').replace(' ', '-') if c.isalnum() or c == '-')
    wd = wr / slug
    wd.mkdir(parents=True, exist_ok=True)
    ws = {
        "app":"anyadha_pmo","charts":[],"content":"[]","creation":"2026-08-25 00:00:00.000000",
        "custom_blocks":[],"docstatus":0,"doctype":"Workspace","for_user":"","hide_custom":0,
        "icon":icon,"idx":idx,"is_hidden":0,"label":label,"links":[],"modified":"2026-08-25 00:00:00.000000",
        "modified_by":"Administrator","module":module,"module_onboarding":"","name":label,"number_cards":[],
        "owner":"Administrator","parent_page":"","public":1,"quick_lists":[],"restrict_to_domain":"",
        "roles":[],"sequence_id":float(idx),"shortcuts":[],"sidebar_items":[]
    }
    (wd / f"{slug}.json").write_text(json.dumps(ws, indent=2) + "\n")

    items = [{"child":0,"collapsible":1,"icon":"house","indent":0,"keep_closed":0,"label":"Home","link_to":label,"link_type":"Workspace","show_arrow":0,"type":"Link"}]
    for doctype, link_label in links.get(label, []):
        items.append({"child":0,"collapsible":0,"icon":"file","indent":0,"keep_closed":0,"label":link_label,"link_to":doctype,"link_type":"DocType","show_arrow":0,"type":"Link"})
    sidebar = {
        "app":"anyadha_pmo","creation":"2026-08-25 00:00:00.000000","docstatus":0,"doctype":"Workspace Sidebar",
        "header_icon":icon,"idx":idx,"items":items,"modified":"2026-08-25 00:00:00.000000",
        "modified_by":"Administrator","name":label,"owner":"Administrator","title":label
    }
    (sr / f"{slug}.json").write_text(json.dumps(sidebar, indent=2) + "\n")
PY

echo "Foundation recreated. Existing DocTypes were not deleted."
echo "Backup: $BACKUP"
echo "Validate with: python3 -m json.tool anyadha_pmo/pmo_masters/doctype/pmo_settings/pmo_settings.json >/dev/null"
echo "Then: git status --short"
