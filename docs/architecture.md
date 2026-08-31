# Architecture

## Core contracts

### Canonical campaign

Every source adapter should produce the same conceptual object:

```json
{
  "campaign": {"id": "...", "name": "...", "kind": "broadcast"},
  "message": {
    "subject": "...",
    "preheader": "...",
    "from_name": "...",
    "from_email": "...",
    "reply_to": "...",
    "html": "...",
    "plain_text": "..."
  },
  "metadata": {"source": "file", "template_language": "none"}
}
```

Vendor-native responses should not be passed directly into validators.

### Finding

Validators return a common result:

```json
{
  "rule_id": "tracking.required_parameters",
  "status": "fail",
  "severity": "high",
  "title": "Required tracking parameters",
  "detail": "Two destination links are missing utm_campaign.",
  "recommendation": "Add the configured parameter before launch.",
  "evidence": ["https://example.test/shop"]
}
```

### Rule pack

A rule pack supplies values and enables rules without embedding company policy in Python. It should be versioned with every run so historical reports remain explainable.

## Extension points

| Boundary | Responsibility | Examples |
|---|---|---|
| Source adapter | Fetch and normalize campaign data | Iterable, Braze, file upload |
| Validator | Inspect canonical data | UTM, accessibility, compliance |
| Policy pack | Configure organization rules | approved senders, thresholds |
| Assisted reviewer | Apply model-based judgment | tone, brief alignment |
| Brief adapter | Retrieve approved requirements | Notion, Asana, Airtable |
| Output adapter | Distribute the report | HTML, Slack, Teams, webhook |
| Run store | Persist status and evidence | PostgreSQL, object storage |

## Suggested production topology

```text
Webhook / command / UI
          |
          v
      API service -----> Run store
          |
          v
       Job queue
          |
          v
       QA worker ------> ESP / brief / rendering APIs
          |
          v
     Report artifact --> collaboration adapter
```

The included reference implementation keeps this deliberately small: JSON input, a synchronous runner, and HTML output. The contracts are designed so those edges can be replaced without rewriting validators.
