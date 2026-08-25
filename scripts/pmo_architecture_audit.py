#!/usr/bin/env python3
"""Static audit of the Anyadha PMO app.

This intentionally checks the whole application in one pass. It does not try
to replace bench migrate or Frappe's own DocType validation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "anyadha_pmo"
EXPECTED_APP = "anyadha_pmo"
errors: list[str] = []
warnings: list[str] = []

def fail(msg: str) -> None:
    errors.append(msg)

def warn(msg: str) -> None:
    warnings.append(msg)

doctype_files = sorted(APP.glob("*/doctype/*/*.json"))

if not doctype_files:
    fail("No DocType JSON files found.")

seen_names: dict[str, Path] = {}

for path in doctype_files:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path}: invalid JSON: {exc}")
        continue

    if data.get("doctype") != "DocType":
        continue

    name = data.get("name")
    module = data.get("module")
    if not name:
        fail(f"{path}: missing name")
    if not module:
        fail(f"{path}: missing module")
    if data.get("custom", 0) not in (0, False):
        warn(f"{path}: custom DocType metadata is set; confirm this is intentional")

    if name in seen_names:
        fail(f"Duplicate DocType name: {name} in {seen_names[name]} and {path}")
    else:
        seen_names[name] = path

    fields = data.get("fields", [])
    fieldnames = []
    for field in fields:
        fn = field.get("fieldname")
        if fn:
            fieldnames.append(fn)

    duplicates = sorted({x for x in fieldnames if fieldnames.count(x) > 1})
    if duplicates:
        fail(f"{path}: duplicate fieldnames: {', '.join(duplicates)}")

    if data.get("track_changes") != 1 and not data.get("issingle"):
        warn(f"{path}: track_changes is not enabled")

    permissions = data.get("permissions", [])
    if not permissions and not data.get("issingle"):
        warn(f"{path}: no DocType permissions declared")

    controller = path.with_name(path.stem + ".py")
    if not controller.exists():
        fail(f"{path}: missing controller {controller.name}")

# Workspace checks
workspace_files = sorted(APP.glob("workspace/*/*.json"))
for path in workspace_files:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path}: invalid workspace JSON: {exc}")
        continue

    if data.get("doctype") != "Workspace":
        fail(f"{path}: not a Workspace")
    if data.get("app") != EXPECTED_APP:
        fail(f"{path}: workspace app must be {EXPECTED_APP}")
    if not data.get("module"):
        fail(f"{path}: workspace module is empty")
    if "sidebar_items" not in data:
        fail(f"{path}: sidebar_items missing")

print(f"DocTypes audited : {len(seen_names)}")
print(f"Workspaces found : {len(workspace_files)}")
print(f"Errors           : {len(errors)}")
print(f"Warnings         : {len(warnings)}")

for item in errors:
    print("ERROR:", item)
for item in warnings:
    print("WARN :", item)

if errors:
    sys.exit(1)

print("STATIC PMO ARCHITECTURE AUDIT: PASS")
