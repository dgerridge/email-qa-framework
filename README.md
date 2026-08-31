# Email QA Framework

An open, configurable reference framework for pre-send marketing email quality assurance.

It combines deterministic checks, optional AI-assisted review, and human approval checkpoints in one portable workflow. The framework is intentionally independent of any particular company, email service provider (ESP), collaboration tool, or model vendor.

> **Portfolio status:** This repository is a working reference implementation built with synthetic campaign data. It demonstrates the product architecture and report experience; it is not a production sending system.

## What it demonstrates

- A canonical campaign format that separates QA logic from ESP APIs
- Composable rule packs for standard, platform, and company-specific policies
- Deterministic checks that work without an LLM
- A consistent finding model: pass, fail, warning, or human review
- A self-contained HTML report suitable for Slack, Teams, or a review portal
- Explicit human approval boundaries—automation informs launch decisions but does not send email

## See it in action

The repository includes two synthetic examples:

- [Launch-blocked report](https://dgerridge.github.io/email-qa-framework/examples/reports/launch-blocked.html): missing tracking, placeholder copy, and other actionable findings
- [Ready-for-review report](https://dgerridge.github.io/email-qa-framework/examples/reports/ready-for-review.html): deterministic checks pass, with final editorial confirmation still required

Generate them again locally:

```bash
python3 -m pip install -e .
python3 -m email_qa_framework.cli \
  examples/data/synthetic-campaign.json \
  --config config/example-company.json \
  --output examples/reports/launch-blocked.html
```

When running from a source checkout without installing the package:

```bash
PYTHONPATH=src python3 -m email_qa_framework.cli examples/data/synthetic-campaign.json \
  --config config/example-company.json \
  --output examples/reports/launch-blocked.html
```

Run the tests without third-party dependencies:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## How it works

```text
ESP, file, or API
       |
       v
Source adapter -> Canonical campaign -> Rule packs -> QA report
                                             |             |
                                      optional AI      Slack / Teams /
                                         review        HTML / webhook
```

The source adapter is the only component that needs to understand Iterable, Braze, Klaviyo, Salesforce Marketing Cloud, or another ESP. Everything downstream receives the same canonical campaign object.

Rule packs can be layered:

1. **Standard:** links, tracking, accessibility, compliance, rendering hygiene
2. **Platform:** Liquid, Handlebars, snippets, authenticated links, ESP limitations
3. **Company:** sender policy, naming conventions, brand voice, promotion mechanics

See [Architecture](docs/architecture.md) and [Product overview](docs/product-overview.md).

## Included checks

The reference implementation intentionally uses a small, inspectable subset:

| Check | Type | Outcome |
|---|---|---|
| Subject length | Deterministic | Warning above configured length |
| Preheader present | Deterministic | Fail when absent |
| Unsubscribe marker | Deterministic | Fail when absent |
| Placeholder copy | Deterministic | Fail on configured patterns |
| Required tracking parameters | Deterministic | Fail when links omit them |
| Insecure HTTP links | Deterministic | Fail on `http://` destinations |
| Image alt text | Deterministic | Warning when meaningful images omit `alt` |
| Final content review | Human checkpoint | Always requires confirmation |

The design supports additional validators without changing the runner or report renderer.

## Repository layout

```text
config/                  Example client policy pack
docs/                    Product and technical narrative
examples/data/           Synthetic canonical campaigns
examples/reports/        Rendered report mockups
src/email_qa_framework/  Reference implementation
tests/                   Unit tests for the example checks
```

## Design principles

- **Deterministic first:** objective checks should be testable and reproducible.
- **AI where judgment helps:** tone, clarity, brief alignment, and ambiguous offers are review tasks—not hidden launch gates.
- **Human accountable:** “ready for review” is not the same as “approved to send.”
- **Configuration over forks:** client policies belong in rule packs rather than duplicated codebases.
- **Adapters at the edges:** vendor APIs and workflow tools do not leak into the core.
- **Evidence with every finding:** reports explain what was detected and what to do next.

## Roadmap

- JSON Schema validation for canonical campaigns and rule packs
- Pluggable ESP adapters
- Optional model-provider interface for editorial review
- Brief comparison adapter for Notion and other work-management systems
- Slack and Teams delivery adapters
- Durable run history, rule-set versioning, and audit logs
- Seed-profile rendering and third-party inbox rendering integrations

## Responsible use

This framework analyzes campaign content, not subscriber records. Production deployments should minimize data collection, use read-only ESP credentials, redact sensitive content from logs, and keep a human approval step before deployment.

## License

The code is provided under the [MIT License](LICENSE). Brand names in documentation are illustrative only and do not imply endorsement.
