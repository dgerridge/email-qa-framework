from __future__ import annotations

from html import escape
from pathlib import Path


STATUS = {
    "fail": ("Fail", "#b42318", "#fee4e2"),
    "warning": ("Warning", "#b54708", "#fffaeb"),
    "human_review": ("Human review", "#175cd3", "#eff8ff"),
    "pass": ("Pass", "#067647", "#ecfdf3"),
}


def _finding_card(item):
    label, color, background = STATUS[item["status"]]
    evidence = ""
    if item.get("evidence"):
        evidence = '<ul class="evidence">' + "".join(f"<li>{escape(str(value))}</li>" for value in item["evidence"]) + "</ul>"
    recommendation = f'<p class="recommendation"><strong>Recommended action:</strong> {escape(item["recommendation"])}</p>' if item.get("recommendation") else ""
    return f"""
    <article class="finding">
      <div class="finding-top">
        <span class="badge" style="color:{color};background:{background}">{label}</span>
        <span class="severity">{escape(item['severity'])}</span>
        <code>{escape(item['rule_id'])}</code>
      </div>
      <h3>{escape(item['title'])}</h3>
      <p>{escape(item['detail'])}</p>
      {evidence}{recommendation}
    </article>"""


def render_report(report):
    campaign = report["campaign"]
    summary = report["summary"]
    blocked = report["verdict"] == "launch_blocked"
    verdict = "Launch blocked" if blocked else "Ready for human review"
    verdict_class = "blocked" if blocked else "ready"
    cards = "".join(_finding_card(item) for item in report["findings"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Email QA Report — {escape(str(campaign.get('name', 'Campaign')))}</title>
  <style>
    :root{{--ink:#17212b;--muted:#667085;--line:#e4e7ec;--surface:#fff;--canvas:#f5f7fa;--accent:#5b46e8}}
    *{{box-sizing:border-box}} body{{margin:0;background:var(--canvas);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.5}}
    .page{{max-width:960px;margin:0 auto;padding:56px 24px 80px}} .eyebrow{{color:var(--accent);font-size:12px;font-weight:750;letter-spacing:.1em;text-transform:uppercase}}
    h1{{font-size:34px;line-height:1.15;margin:10px 0 8px;letter-spacing:-.03em}} .meta{{color:var(--muted);font-size:14px}} .hero{{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:28px;margin:28px 0;box-shadow:0 8px 30px rgba(16,24,40,.05)}}
    .verdict{{display:inline-flex;padding:8px 13px;border-radius:999px;font-size:13px;font-weight:750}} .blocked{{background:#fee4e2;color:#b42318}} .ready{{background:#ecfdf3;color:#067647}}
    .counts{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px}} .count{{border:1px solid var(--line);border-radius:12px;padding:14px}} .count strong{{display:block;font-size:24px}} .count span{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em}}
    h2{{font-size:20px;margin:36px 0 14px}} .finding{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px;margin:12px 0}} .finding-top{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}} .badge{{font-size:12px;font-weight:750;border-radius:999px;padding:4px 9px}} .severity{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}} code{{font-size:12px;color:#475467;background:#f2f4f7;border-radius:5px;padding:3px 6px}} h3{{font-size:17px;margin:13px 0 5px}} .finding p{{margin:5px 0;color:#475467}} .recommendation{{border-left:3px solid #b9afff;padding-left:12px;margin-top:14px!important}} .evidence{{color:#475467;font-size:13px;overflow-wrap:anywhere}} footer{{margin-top:36px;color:var(--muted);font-size:12px}}
    @media(max-width:640px){{.page{{padding:32px 16px}}h1{{font-size:28px}}.counts{{grid-template-columns:repeat(2,1fr)}}}}
  </style>
</head>
<body><main class="page">
  <div class="eyebrow">Email QA Framework</div>
  <h1>{escape(str(campaign.get('name', 'Campaign')))}</h1>
  <div class="meta">Campaign {escape(str(campaign.get('id', '—')))} · {escape(str(campaign.get('kind', 'unknown')).title())} · Policy {escape(report['policy']['version'])}</div>
  <section class="hero">
    <span class="verdict {verdict_class}">{verdict}</span>
    <div class="counts">
      <div class="count"><strong>{summary['fail']}</strong><span>Fails</span></div>
      <div class="count"><strong>{summary['warning']}</strong><span>Warnings</span></div>
      <div class="count"><strong>{summary['human_review']}</strong><span>Human review</span></div>
      <div class="count"><strong>{summary['pass']}</strong><span>Passes</span></div>
    </div>
  </section>
  <h2>Findings</h2>{cards}
  <footer>Generated from synthetic demonstration data. A QA result does not authorize deployment; final approval remains with the designated reviewer.</footer>
</main></body></html>"""


def write_report(report, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(report), encoding="utf-8")
    return path
