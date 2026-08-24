from pathlib import Path
import json

def test_doctypes_have_names():
    root = Path(__file__).resolve().parents[1] / "anyadha_pmo"
    files = list(root.rglob("doctype/*/*.json"))
    assert len(files) >= 50
    for f in files:
        data = json.loads(f.read_text())
        assert data["doctype"] == "DocType"
        assert data["name"]
        assert data["module"]
