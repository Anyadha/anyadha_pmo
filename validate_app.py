import json
from pathlib import Path
for p in Path(__file__).parent.rglob("*.json"):
    json.loads(p.read_text(encoding="utf-8"))
print("All JSON valid.")
