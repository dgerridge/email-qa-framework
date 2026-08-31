import json
import unittest
from pathlib import Path

from email_qa_framework.runner import run_qa


ROOT = Path(__file__).parents[1]
CONFIG = json.loads((ROOT / "config/example-company.json").read_text())


def load_example(name):
    return json.loads((ROOT / "examples/data" / name).read_text())


class FrameworkTests(unittest.TestCase):
    def test_blocked_example_has_expected_findings(self):
        report = run_qa(load_example("synthetic-campaign.json"), CONFIG)
        self.assertEqual(report["verdict"], "launch_blocked")
        failed = {item["rule_id"] for item in report["findings"] if item["status"] == "fail"}
        self.assertTrue({"content.preheader", "content.placeholders", "tracking.required_parameters"} <= failed)

    def test_ready_example_retains_human_checkpoint(self):
        report = run_qa(load_example("synthetic-campaign-ready.json"), CONFIG)
        self.assertEqual(report["verdict"], "ready_for_human_review")
        self.assertEqual(report["summary"]["fail"], 0)
        self.assertEqual(report["summary"]["human_review"], 1)


if __name__ == "__main__":
    unittest.main()
