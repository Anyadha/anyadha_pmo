from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parent
APP = ROOT / "anyadha_pmo"
errors = []
warnings = []

required = [
    "hooks.py", "__init__.py", "__version__.py", "modules.txt",
    "project_management", "programme_management", "pmo_masters"
]
for item in required:
    if not (APP / item).exists():
        errors.append(f"Missing required app item: {item}")

modules = set((APP / "modules.txt").read_text().splitlines())
doctype_files = list(APP.rglob("doctype/*/*.json"))
names = []

for path in doctype_files:
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        errors.append(f"Invalid JSON: {path}: {e}")
        continue

    if data.get("doctype") != "DocType":
        errors.append(f"Not a DocType JSON: {path}")
    if data.get("custom") is True:
        errors.append(f"Shipped app DocType must not have custom=1: {path}")
    if not data.get("name"):
        errors.append(f"DocType missing name: {path}")
    else:
        names.append(data["name"])
    if not data.get("module"):
        errors.append(f"DocType missing module: {path}")
    elif data["module"] not in modules:
        errors.append(f"Unknown module '{data['module']}' in {path}")
    if "fields" not in data:
        errors.append(f"DocType missing fields: {path}")
    if data.get("istable") and data.get("issingle"):
        errors.append(f"Child table cannot be single: {path}")

    folder = path.parent
    py = folder / (folder.name + ".py")
    js = folder / (folder.name + ".js")
    if not py.exists():
        warnings.append(f"No Python controller for {data.get('name')}: {py}")
    if not js.exists():
        warnings.append(f"No JS controller for {data.get('name')}: {js}")

dupes = sorted({n for n in names if names.count(n) > 1})
if dupes:
    errors.append("Duplicate DocType names: " + ", ".join(dupes))

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)

print("VALIDATION PASSED")
print(f"DocTypes checked: {len(doctype_files)}")
print(f"Modules checked: {len(modules)}")
print(f"Warnings: {len(warnings)}")
for w in warnings[:25]:
    print("WARNING:", w)
