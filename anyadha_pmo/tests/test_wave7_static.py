from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "anyadha_pmo"


class TestWave7Static(unittest.TestCase):
    def test_all_doctypes_have_controllers_and_permissions(self):
        for path in APP.glob("*/doctype/*/*.json"):
            data = json.loads(path.read_text())
            if data.get("doctype") != "DocType" or data.get("issingle"):
                continue
            self.assertTrue(path.with_suffix(".py").exists(), path)
            self.assertTrue(data.get("permissions"), path)

    def test_performance_workspace_contains_all_wave6_reports(self):
        path = APP / "performance_mis/workspace/performance_mis/performance_mis.json"
        data = json.loads(path.read_text())
        names = {x.get("link_to") for x in data["links"]}
        for name in (
            "PMO KPI Performance", "PMO KRI Status", "PMO KCI Status",
            "PMO Indicator Readings", "PMO Management MIS", "PMO Performance Reviews",
        ):
            self.assertIn(name, names)

    def test_wave7_service_metadata(self):
        from anyadha_pmo.core.services.release import release_metadata
        meta = release_metadata()
        self.assertEqual(meta["app"], "anyadha_pmo")
        self.assertTrue(meta["wave"].startswith("Wave 7"))


if __name__ == "__main__":
    unittest.main()
