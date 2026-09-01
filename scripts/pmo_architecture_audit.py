#!/usr/bin/env python3

"""
Static architecture audit for the Anyadha PMO app.

Architecture:

anyadha_pmo/
    <module>/
        modules.txt
        doctype/
        report/
        workspace/
            <workspace>/
                <workspace>.json

This audit validates the complete PMO application structure before
Git commit / GitHub push / Frappe Cloud deployment.

It does NOT run bench migrate and does NOT access a Frappe site.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------
# ROOT
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "anyadha_pmo"

EXPECTED_APP = "anyadha_pmo"

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path}: invalid JSON: {exc}")
        return None


# ---------------------------------------------------------------------
# EXPECTED MODULES
# ---------------------------------------------------------------------

EXPECTED_MODULES = [
    "PMO Masters",
    "Governance",
    "Strategy Portfolio",
    "Proposal DPR",
    "Programme Management",
    "Project Management",
    "Monitoring Evaluation",
    "Grants Donor Management",
    "CSR Management",
    "Risk Internal Controls",
    "Compliance Regulatory",
    "Audit Assurance",
    "SOP Document Control",
    "Performance MIS",
]


# Folder mapping is deliberately explicit.
# This prevents accidental renaming of module folders from going unnoticed.

MODULE_FOLDERS = {
    "PMO Masters": "pmo_masters",
    "Governance": "governance",
    "Strategy Portfolio": "strategy_portfolio",
    "Proposal DPR": "proposal_dpr",
    "Programme Management": "programme_management",
    "Project Management": "project_management",
    "Monitoring Evaluation": "monitoring_evaluation",
    "Grants Donor Management": "grants_donor_management",
    "CSR Management": "csr_management",
    "Risk Internal Controls": "risk_internal_controls",
    "Compliance Regulatory": "compliance_regulatory",
    "Audit Assurance": "audit_assurance",
    "SOP Document Control": "sop_document_control",
    "Performance MIS": "performance_mis",
}


# ---------------------------------------------------------------------
# CHILD TABLES
# ---------------------------------------------------------------------

child_tables: set[str] = set()


# ---------------------------------------------------------------------
# GLOBAL DOCTYPE INVENTORY
# ---------------------------------------------------------------------

doctype_files = sorted(APP.glob("*/doctype/*/*.json"))

if not doctype_files:
    fail("No DocType JSON files found.")

seen_doctypes: dict[str, Path] = {}
doctype_modules: dict[str, str] = {}
doctype_paths: dict[str, Path] = {}

for path in doctype_files:
    data = load_json(path)

    if not data:
        continue

    if data.get("doctype") != "DocType":
        continue

    name = data.get("name")
    module = data.get("module")

    if not name:
        fail(f"{path}: missing name")
        continue

    if not module:
        fail(f"{path}: missing module")

    if name in seen_doctypes:
        fail(
            f"Duplicate DocType name: {name} in "
            f"{seen_doctypes[name]} and {path}"
        )
    else:
        seen_doctypes[name] = path

    if module:
        doctype_modules[name] = module

    doctype_paths[name] = path

    if data.get("istable"):
        child_tables.add(name)

    if data.get("custom", 0) not in (0, False):
        warn(
            f"{path}: custom DocType metadata is set; "
            "confirm this is intentional"
        )

    # Fieldname duplication
    fieldnames = []

    for field in data.get("fields", []):
        fieldname = field.get("fieldname")

        if fieldname:
            fieldnames.append(fieldname)

    duplicates = sorted(
        {x for x in fieldnames if fieldnames.count(x) > 1}
    )

    if duplicates:
        fail(
            f"{path}: duplicate fieldnames: "
            + ", ".join(duplicates)
        )

    # Controller
    if not data.get("issingle"):
        controller = path.with_name(path.stem + ".py")

        if not controller.exists():
            fail(
                f"{path}: missing controller "
                f"{controller.name}"
            )

    # Track changes
    if (
        data.get("track_changes") != 1
        and not data.get("issingle")
    ):
        warn(f"{path}: track_changes is not enabled")

    # Permissions
    if (
        not data.get("permissions")
        and not data.get("issingle")
    ):
        warn(
            f"{path}: no DocType permissions declared"
        )


# ---------------------------------------------------------------------
# MODULE VALIDATION
# ---------------------------------------------------------------------

module_data: dict[str, dict] = {}

for module, folder_name in MODULE_FOLDERS.items():

    module_dir = APP / folder_name

    if not module_dir.exists():
        fail(
            f"Module folder missing: {module} -> {module_dir}"
        )
        continue

    modules_txt = module_dir / "modules.txt"

    if not modules_txt.exists():
        fail(
            f"{module}: modules.txt missing: {modules_txt}"
        )
    else:
        declared = modules_txt.read_text(
            encoding="utf-8"
        ).strip()

        if declared != module:
            fail(
                f"{module}: modules.txt contains "
                f"{declared!r}, expected {module!r}"
            )

    doctype_dir = module_dir / "doctype"

    if not doctype_dir.exists():
        fail(
            f"{module}: doctype directory missing"
        )

    report_dir = module_dir / "report"

    workspace_dir = module_dir / "workspace"

    module_data[module] = {
        "folder": folder_name,
        "path": module_dir,
        "doctype_dir": doctype_dir,
        "report_dir": report_dir,
        "workspace_dir": workspace_dir,
        "doctypes": [],
        "reports": [],
        "workspaces": [],
    }


# ---------------------------------------------------------------------
# DOC TYPE OWNERSHIP
# ---------------------------------------------------------------------

for name, module in sorted(doctype_modules.items()):

    if module not in EXPECTED_MODULES:
        fail(
            f"DocType {name}: unknown module {module!r}"
        )
        continue

    module_info = module_data.get(module)

    if module_info:
        module_info["doctypes"].append(name)


# ---------------------------------------------------------------------
# REPORT INVENTORY
# ---------------------------------------------------------------------

report_files = sorted(APP.glob("*/report/*/*.json"))

seen_reports: dict[str, Path] = {}
report_modules: dict[str, str] = {}

for path in report_files:

    data = load_json(path)

    if not data:
        continue

    if data.get("doctype") != "Report":
        continue

    name = data.get("name")
    module = data.get("module")

    if not name:
        fail(f"{path}: report missing name")
        continue

    if not module:
        fail(f"{path}: report missing module")

    if name in seen_reports:
        fail(
            f"Duplicate Report name: {name} in "
            f"{seen_reports[name]} and {path}"
        )
    else:
        seen_reports[name] = path

    if module:
        report_modules[name] = module

        if module in module_data:
            module_data[module]["reports"].append(name)
        elif module not in EXPECTED_MODULES:
            fail(
                f"Report {name}: unknown module {module!r}"
            )


# ---------------------------------------------------------------------
# WORKSPACE INVENTORY
# ---------------------------------------------------------------------

workspace_files = sorted(
    APP.glob("*/workspace/*/*.json")
)

if not workspace_files:
    fail(
        "No module workspaces found under "
        "*/workspace/*/*.json"
    )


seen_workspaces: dict[str, Path] = {}

workspace_modules: dict[str, str] = {}


for path in workspace_files:

    data = load_json(path)

    if not data:
        continue

    name = data.get("name")
    module = data.get("module")

    if not name:
        fail(f"{path}: workspace missing name")
        continue

    if name in seen_workspaces:
        fail(
            f"Duplicate Workspace name: {name} in "
            f"{seen_workspaces[name]} and {path}"
        )
    else:
        seen_workspaces[name] = path

    if data.get("doctype") != "Workspace":
        fail(
            f"{path}: doctype must be 'Workspace'"
        )

    if data.get("type") != "Workspace":
        fail(
            f"{path}: type must be 'Workspace'"
        )

    if data.get("standard") != 1:
        fail(
            f"{path}: standard must be 1"
        )

    if data.get("app") != EXPECTED_APP:
        fail(
            f"{path}: app must be {EXPECTED_APP!r}"
        )

    if not module:
        fail(
            f"{path}: workspace module is empty"
        )
        continue

    workspace_modules[name] = module

    if module not in EXPECTED_MODULES:
        fail(
            f"{path}: workspace belongs to unknown "
            f"module {module!r}"
        )
        continue

    module_info = module_data.get(module)

    if module_info:
        module_info["workspaces"].append(
            {
                "name": name,
                "path": path,
                "data": data,
            }
        )

    if "sidebar_items" not in data:
        fail(
            f"{path}: sidebar_items missing"
        )


# ---------------------------------------------------------------------
# MODULE → WORKSPACE VALIDATION
# ---------------------------------------------------------------------

for module in EXPECTED_MODULES:

    info = module_data.get(module)

    if not info:
        continue

    workspaces = info["workspaces"]

    if len(workspaces) == 0:
        fail(
            f"{module}: no Workspace found"
        )

    elif len(workspaces) > 1:
        fail(
            f"{module}: multiple Workspaces found: "
            + ", ".join(
                x["name"] for x in workspaces
            )
        )


# ---------------------------------------------------------------------
# WORKSPACE SIDEBAR VALIDATION
# ---------------------------------------------------------------------

for module in EXPECTED_MODULES:

    info = module_data.get(module)

    if not info or len(info["workspaces"]) != 1:
        continue

    workspace = info["workspaces"][0]
    path = workspace["path"]
    data = workspace["data"]

    expected_doctypes = set(info["doctypes"])
    expected_reports = set(info["reports"])

    sidebar = data.get("sidebar_items", [])
    links = data.get("links", [])

    sidebar_doctypes: set[str] = set()
    sidebar_reports: set[str] = set()

    # --------------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------------

    for item in sidebar:

        link_type = item.get("link_type")
        link_to = item.get("link_to")
        item_type = item.get("type")

        if item_type == "Section Break":
            continue

        if link_type == "DocType":

            if not link_to:
                fail(
                    f"{path}: sidebar DocType item "
                    f"{item.get('label')!r} has empty link_to"
                )
                continue

            sidebar_doctypes.add(link_to)

            if link_to not in seen_doctypes:
                fail(
                    f"{path}: sidebar references unknown "
                    f"DocType {link_to!r}"
                )
                continue

            owner = doctype_modules.get(link_to)

            if owner != module:
                fail(
                    f"{path}: sidebar DocType {link_to!r} "
                    f"belongs to {owner!r}, not {module!r}"
                )

            if link_to in child_tables:
                fail(
                    f"{path}: child-table DocType "
                    f"{link_to!r} must not appear "
                    "as a standalone sidebar item"
                )

        elif link_type == "Report":

            if not link_to:
                fail(
                    f"{path}: sidebar Report item "
                    f"{item.get('label')!r} has empty link_to"
                )
                continue

            sidebar_reports.add(link_to)

            if link_to not in seen_reports:
                fail(
                    f"{path}: sidebar references unknown "
                    f"Report {link_to!r}"
                )
                continue

            owner = report_modules.get(link_to)

            if owner != module:
                fail(
                    f"{path}: sidebar Report {link_to!r} "
                    f"belongs to {owner!r}, not {module!r}"
                )

    # --------------------------------------------------------------
    # LINKS
    # --------------------------------------------------------------

    link_doctypes: set[str] = set()
    link_reports: set[str] = set()

    for item in links:

        link_type = item.get("link_type")
        link_to = item.get("link_to")

        if item.get("type") == "Card Break":
            continue

        if link_type == "DocType":

            if not link_to:
                fail(
                    f"{path}: Workspace DocType link "
                    f"{item.get('label')!r} has empty link_to"
                )
                continue

            link_doctypes.add(link_to)

            if link_to not in seen_doctypes:
                fail(
                    f"{path}: Workspace links unknown "
                    f"DocType {link_to!r}"
                )
                continue

            owner = doctype_modules.get(link_to)

            if owner != module:
                fail(
                    f"{path}: Workspace DocType {link_to!r} "
                    f"belongs to {owner!r}, not {module!r}"
                )

        elif link_type == "Report":

            if not link_to:
                fail(
                    f"{path}: Workspace Report link "
                    f"{item.get('label')!r} has empty link_to"
                )
                continue

            link_reports.add(link_to)

            if link_to not in seen_reports:
                fail(
                    f"{path}: Workspace links unknown "
                    f"Report {link_to!r}"
                )
                continue

            owner = report_modules.get(link_to)

            if owner != module:
                fail(
                    f"{path}: Workspace Report {link_to!r} "
                    f"belongs to {owner!r}, not {module!r}"
                )

    # --------------------------------------------------------------
    # EXPECTED COVERAGE
    # --------------------------------------------------------------

    missing_sidebar_doctypes = (
        expected_doctypes
        - child_tables
        - sidebar_doctypes
    )

    if missing_sidebar_doctypes:
        fail(
            f"{path}: standalone DocTypes missing from "
            "sidebar: "
            + ", ".join(sorted(missing_sidebar_doctypes))
        )

    missing_sidebar_reports = (
        expected_reports - sidebar_reports
    )

    if missing_sidebar_reports:
        fail(
            f"{path}: Reports missing from sidebar: "
            + ", ".join(sorted(missing_sidebar_reports))
        )

    missing_link_doctypes = (
        expected_doctypes
        - child_tables
        - link_doctypes
    )

    if missing_link_doctypes:
        fail(
            f"{path}: standalone DocTypes missing from "
            "Workspace links: "
            + ", ".join(sorted(missing_link_doctypes))
        )

    missing_link_reports = (
        expected_reports - link_reports
    )

    if missing_link_reports:
        fail(
            f"{path}: Reports missing from Workspace links: "
            + ", ".join(sorted(missing_link_reports))
        )


# ---------------------------------------------------------------------
# LEGACY WORKSPACE DETECTION
# ---------------------------------------------------------------------

legacy_workspace_dir = APP / "workspace"

if legacy_workspace_dir.exists():

    legacy_files = sorted(
        legacy_workspace_dir.glob("*/*.json")
    )

    if legacy_files:

        for path in legacy_files:
            fail(
                f"Legacy workspace definition remains: {path}"
            )


# ---------------------------------------------------------------------
# WORKSPACE FILE LOCATION VALIDATION
# ---------------------------------------------------------------------

for path in workspace_files:

    relative_parts = path.relative_to(APP).parts

    # Expected:
    # module_folder / workspace / workspace_folder / file.json

    if len(relative_parts) != 4:
        fail(
            f"{path}: unexpected Workspace path structure"
        )
        continue

    folder_name = relative_parts[0]

    module_matches = [
        module
        for module, folder in MODULE_FOLDERS.items()
        if folder == folder_name
    ]

    if not module_matches:
        fail(
            f"{path}: Workspace is under unknown "
            f"module folder {folder_name!r}"
        )


# ---------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------

total_doctypes = len(seen_doctypes)
total_child_tables = len(child_tables)
total_standalone = (
    total_doctypes - total_child_tables
)

total_reports = len(seen_reports)
total_workspaces = len(workspace_files)


print("=" * 80)
print("ANYADHA PMO — STATIC ARCHITECTURE AUDIT")
print("=" * 80)

print()
print(f"DocTypes audited       : {total_doctypes}")
print(f"Child-table DocTypes   : {total_child_tables}")
print(f"Standalone DocTypes    : {total_standalone}")
print(f"Reports audited        : {total_reports}")
print(f"Workspaces found       : {total_workspaces}")
print(f"Modules expected       : {len(EXPECTED_MODULES)}")
print(f"Errors                 : {len(errors)}")
print(f"Warnings               : {len(warnings)}")

print()
print("===== MODULE WORKSPACE SUMMARY =====")

for module in EXPECTED_MODULES:

    info = module_data.get(module)

    if not info:
        print(
            f"FAIL | {module:<30} | module data missing"
        )
        continue

    workspace_names = [
        x["name"] for x in info["workspaces"]
    ]

    print(
        f"{module:<30} | "
        f"DocTypes={len(info['doctypes']):<3} | "
        f"Reports={len(info['reports']):<2} | "
        f"Workspace={', '.join(workspace_names) if workspace_names else 'MISSING'}"
    )

print()

if errors:

    print("===== ERRORS =====")

    for item in errors:
        print("ERROR:", item)

if warnings:

    print()
    print("===== WARNINGS =====")

    for item in warnings:
        print("WARN :", item)

print()

if errors:

    print("STATIC PMO ARCHITECTURE AUDIT: FAIL")
    sys.exit(1)

print("STATIC PMO ARCHITECTURE AUDIT: PASS")
print()
print("Architecture is ready for Git validation.")
