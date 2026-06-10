# Active State & Current Architecture

This file documents the active state, current configurations, code graph, and verification status of the current project.

> [!IMPORTANT]
> **Concision Constraint**: Keep all entries in this file extremely concise. Prune deprecated modules or obsolete state immediately to preserve token space.

---

## Active Stack Details

| Layer | Technology | Key Details |
| :--- | :--- | :--- |
| **Framework** | FastAPI / google-adk | ASGI agent microservice |
| **Language/Typing** | Python | Type-annotated modules, Pydantic validation |
| **Testing** | Unittest / pytest | Local unit tests and manual endpoint QA |
| **Deployment** | Docker / Cloud Run | Source deployable to managed GCP environments |

---

## Architecture / Code Graph

*Describe the high-level architecture or monorepo structure here.*

```mermaid
graph TD
    Root["/"]
    Template["template/.agents/"]
    RootAgents[".agents/"]
    Eval["EVALUATION.md"]
    ADKTemplate["adk-agent-template/"]
    Root --> Template
    Root --> RootAgents
    Root --> Eval
    Root --> ADKTemplate
```

### Module Descriptions:
- **`template/.agents/`**: The pristine distribution folder containing rules, skills, and blank memory templates.
- **`.agents/`**: The active memory system tracking the development of *this* repository itself.
- **`EVALUATION.md`**: Behavioral test script for verifying AI agent compliance.
- **`adk-agent-template/`**: An Agent Development Kit (ADK) template configured for hosting Epoch-compliant agents on Google Cloud Agent Engine, complete with Agent-to-Agent (A2A) integration.

---

## Environment / Security Notes

* None.

---

## Verification Compliance Status

We enforce strict validation criteria. The current status is:

1.  **Type Checks**: N/A
2.  **Linting**: Clean Markdown.
3.  **Test Suites**: Evaluated via QA script.
4.  **Production Builds**: N/A
