from __future__ import annotations

from datetime import datetime, timezone

from .checks import CHECKS


STATUS_ORDER = {"fail": 0, "warning": 1, "human_review": 2, "pass": 3}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def run_qa(payload: dict, config: dict) -> dict:
    campaign = payload.get("campaign", {})
    message = payload.get("message", {})
    findings = [check(message, config) for check in CHECKS]
    findings.sort(key=lambda item: (STATUS_ORDER.get(item["status"], 9), SEVERITY_ORDER.get(item["severity"], 9)))

    counts = {status: sum(item["status"] == status for item in findings) for status in STATUS_ORDER}
    blocked = counts["fail"] > 0
    return {
        "campaign": campaign,
        "metadata": payload.get("metadata", {}),
        "policy": {
            "organization": config.get("organization", "Unknown organization"),
            "version": config.get("policy_version", "unversioned"),
        },
        "run_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "launch_blocked" if blocked else "ready_for_human_review",
        "summary": counts,
        "findings": findings,
    }
