# Project History & Milestone Timeline

This file captures the chronological history of milestones, architectural decisions, and tasks completed in the repository.

---

## Sprint Chronology

### Milestone 1: Core Protocol Setup
*   **Accomplishment**: Created symmetric `/plan` and `/checkpoint` workflows. Renamed memory files to standard Agile nomenclature (`context.md`, `backlog.md`, `changelog.md`).
*   **Decisions**: Shifted to a stateless file-based memory system to completely eliminate token-bloat.

### Milestone 2: Generalization & Directives
*   **Accomplishment**: Stripped all React/Node coupling. Created `core-directives.md` and `EVALUATION.md`.
*   **Decisions**: Mandated that the active `.agents/` brain is separated from the distribution templates in `template/.agents/`.

---

### Sprint: Framework Rebranding and Meta-Planning
*   **Accomplishment**: Researched AI agent contextual memory frameworks. Brainstormed new names and rebranded the project from "Agent Protocols" to **Epoch**. Drafted a low-maintenance organic promotional strategy.
*   **Decisions**: Established the "Continuous Milestone: Meta-Planning & Agent Improvement" for infinite refinement of agent constraints. Changed generic "Next Session Focus" terminology to "Session Focus" across all templates.

### Sprint: Documentation Audit and v1.0 Readiness
*   **Accomplishment**: Audited project repository, rules, templates, and documentation for v1.0 release. Corrected discrepancies in `README.md` by removing references to a non-existent `.agents/prompts/` directory to align with the actual template folder structure.
*   **Decisions**: Keep templates clean by matching the documented structure precisely to the provided files.

### Sprint: ADK Integration & FastAPI Deployment
*   **Accomplishment**: Created the ADK agent template (`adk-agent-template/`) with custom Epoch memory synchronization tools (`read_epoch_memory`, `update_epoch_memory`). Simplified deployment by building a standard FastAPI server (removing experimental A2A dependencies) to guarantee container startup. Built and deployed the container to Google Cloud Run, serving a healthy live endpoint. Hardened deployment security by revoking the `allUsers` role, blocking public unauthenticated internet access.
*   **Decisions**: Defer experimental A2A protocol integration to a separate milestone (Milestone 4) to prioritize a working production deployment first. Require authenticated requests for Cloud Run invoker access in production.

*(Append new sprint accomplishments below)*
