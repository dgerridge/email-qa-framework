from __future__ import annotations

import argparse
import json
from pathlib import Path

from .report import write_report
from .runner import run_qa


def main():
    parser = argparse.ArgumentParser(description="Run email QA against a canonical campaign JSON file.")
    parser.add_argument("campaign", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = run_qa(campaign, config)
    output = write_report(report, args.output)
    print(f"{report['verdict']}: {output}")


if __name__ == "__main__":
    main()
