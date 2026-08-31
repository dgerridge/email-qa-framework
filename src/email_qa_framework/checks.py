from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse


def finding(rule_id, status, severity, title, detail, recommendation=None, evidence=None):
    result = {
        "rule_id": rule_id,
        "status": status,
        "severity": severity,
        "title": title,
        "detail": detail,
    }
    if recommendation:
        result["recommendation"] = recommendation
    if evidence:
        result["evidence"] = evidence
    return result


class _EmailHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "img":
            self.images.append(values)


def _parsed_html(message):
    parser = _EmailHTMLParser()
    parser.feed(message.get("html", ""))
    return parser


def check_subject(message, config):
    subject = message.get("subject", "").strip()
    limit = int(config.get("subject_warning_length", 60))
    if not subject:
        return finding("content.subject", "fail", "high", "Subject line", "The subject line is empty.", "Add the approved subject before launch.")
    if len(subject) > limit:
        return finding("content.subject", "warning", "low", "Subject line length", f"The subject is {len(subject)} characters; the configured warning threshold is {limit}.", "Confirm the most important words remain visible on mobile.")
    return finding("content.subject", "pass", "low", "Subject line", f"Subject is present and within the {limit}-character threshold.")


def check_preheader(message, _config):
    if message.get("preheader", "").strip():
        return finding("content.preheader", "pass", "low", "Preheader", "A preheader is present.")
    return finding("content.preheader", "fail", "high", "Preheader", "The preheader is empty.", "Add the approved preheader before launch.")


def check_unsubscribe(message, config):
    html = message.get("html", "")
    markers = config.get("unsubscribe_markers", [])
    if any(marker in html for marker in markers):
        return finding("compliance.unsubscribe", "pass", "low", "Unsubscribe mechanism", "A configured unsubscribe marker is present.")
    return finding("compliance.unsubscribe", "fail", "critical", "Unsubscribe mechanism", "No configured unsubscribe marker was found.", "Add the ESP's unsubscribe token before launch.")


def check_placeholders(message, config):
    text = "\n".join(str(message.get(key, "")) for key in ("subject", "preheader", "plain_text", "html"))
    matches = [pattern for pattern in config.get("placeholder_patterns", []) if re.search(re.escape(pattern), text, re.IGNORECASE)]
    if matches:
        return finding("content.placeholders", "fail", "high", "Placeholder content", f"Possible unfinished content matched {len(matches)} configured pattern(s).", "Replace or remove placeholder content.", matches)
    return finding("content.placeholders", "pass", "low", "Placeholder content", "No configured placeholder patterns were detected.")


def check_tracking(message, config):
    parser = _parsed_html(message)
    required = config.get("required_tracking_parameters", {})
    domains = set(config.get("tracking_domains", []))
    exemptions = config.get("tracking_exempt_paths", [])
    failures = []
    for href in parser.links:
        parsed = urlparse(href)
        if parsed.hostname not in domains or any(parsed.path.startswith(path) for path in exemptions):
            continue
        params = parse_qs(parsed.query)
        missing = [key for key, expected in required.items() if key not in params or (expected != "*" and expected not in params[key])]
        if missing:
            failures.append(f"{href} — missing or invalid: {', '.join(missing)}")
    if failures:
        return finding("tracking.required_parameters", "fail", "high", "Required tracking parameters", f"{len(failures)} tracked destination(s) do not meet policy.", "Add the configured tracking parameters.", failures)
    return finding("tracking.required_parameters", "pass", "low", "Required tracking parameters", "All in-scope destinations meet the configured tracking policy.")


def check_https(message, _config):
    insecure = [href for href in _parsed_html(message).links if href.lower().startswith("http://")]
    if insecure:
        return finding("links.https", "fail", "high", "Secure links", f"{len(insecure)} link(s) use insecure HTTP.", "Update destinations to HTTPS.", insecure)
    return finding("links.https", "pass", "low", "Secure links", "No insecure HTTP destinations were found.")


def check_image_alt(message, _config):
    missing = [image.get("src", "unnamed image") for image in _parsed_html(message).images if not image.get("alt", "").strip()]
    if missing:
        return finding("accessibility.image_alt", "warning", "medium", "Image alternative text", f"{len(missing)} image(s) have no alternative text.", "Add meaningful alt text or alt=\"\" for decorative images.", missing)
    return finding("accessibility.image_alt", "pass", "low", "Image alternative text", "All images include an alt attribute.")


def human_checkpoint(_message, _config):
    return finding("approval.final_review", "human_review", "medium", "Final content approval", "Confirm copy, offer terms, audience, destinations, and rendered appearance against the approved brief.")


CHECKS = [check_subject, check_preheader, check_unsubscribe, check_placeholders, check_tracking, check_https, check_image_alt, human_checkpoint]
