# Product overview

## The problem

Marketing emails combine content, HTML, tracking, personalization, offer logic, accessibility, and legal requirements. Those concerns are often owned by different teams, so manual review varies by reviewer and important context can be lost during handoffs.

The Email QA Framework makes the repeatable portion of pre-send review mechanical while preserving human judgment where context matters.

## The proposed experience

A marketer or production partner initiates QA from an existing workflow. A source adapter retrieves the campaign and converts it into a canonical format. Configured rule packs inspect the campaign, and optional AI-assisted reviewers evaluate areas such as copy clarity or brief alignment. The result is delivered wherever the team already works.

```text
Manual command or workflow status change
                    |
                    v
             QA run requested
                    |
          +---------+---------+
          |                   |
    Campaign source       Approved brief
          |                   |
          +---------+---------+
                    v
       Deterministic + assisted review
                    |
                    v
       Report with evidence and fixes
                    |
                    v
         Human approves or remediates
```

## What is universal and what is configurable

Universal capabilities include checking links, tracking structure, placeholder content, accessibility basics, message size, and common compliance elements.

Client-specific rule packs define approved senders, naming conventions, required tracking values, brand voice, promotional mechanics, template requirements, and severity thresholds.

Platform adapters handle differences among ESP APIs and template languages. Collaboration adapters handle Slack, Teams, Notion, webhooks, and other workflow surfaces.

## Why AI is useful—but not the whole product

AI-assisted review is well suited to grammar, tone, offer clarity, personalization edge cases, and comparison against an approved brief. Objective requirements remain deterministic so they can be tested, audited, and run without a model provider.

The durable product value is the combination of reusable rules, client policy packs, integrations, evidence-rich reports, and feedback from real QA outcomes.

## Deployment model

An initial deployment can be lightweight and read-only. A production service should add durable background jobs, encrypted credential storage, run history, rule-set versioning, access control, observability, and data-retention controls.

No subscriber data is required for the baseline workflow. Seed profiles used for personalization testing should be synthetic.

## Success measures

- Defects caught before send
- Reduction in repetitive manual review time
- False-positive rate by rule
- Time from QA request to approval
- Recurring failure categories by template or team
- Percentage of findings remediated before launch
