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

### Sprint: Tool Simplification & Model Migration
*   **Accomplishment**: Simplified the memory tools signature by decomposing the generic `read_epoch_memory`/`update_epoch_memory` tools into six explicit, parameter-free (read) or single-argument (write) functions (`read_context`, `update_context`, etc.), successfully preventing malformed function call exceptions on Vertex AI. Migrated the default agent model to the stable `gemini-2.5-pro` (Gemini Next) to fix deprecated/unavailable model errors. Verified the local server integration endpoints using curl.
*   **Decisions**: Expose explicit tools for each memory file to avoid passing dynamic string parameters (like filenames) that LLMs might fail to validate or populate correctly. Use `gemini-2.5-pro` as the new default model for ADK agents in this repository.

### Sprint: MCP Server Setup & Agent Engine Deployment
*   **Accomplishment**: Installed and verified 5 Google Cloud MCP servers (`developer-knowledge`, `agent-registry`, `storage`, `run`, and `gemini-cloud-assist`). Configured project-scoped configurations inside `.agents/settings.json` and `.agents/mcp_config.json`. Enabled required API services and IAM policies on the active GCP project. Successfully deployed the ADK agent to **Google Cloud Agent Engine** (Agent Runtime reasoning engine) using a staging directory build context to exclude virtual environment bloat, verifying its successful startup and state synchronization tools.
*   **Decisions**: Exclude Python `venv` from the ADK build context to prevent packaging errors due to broken symlinks. Keep project-specific MCP server settings scoped to `.agents/` rather than global configurations.

### Sprint: Template Generalization & Configuration
*   **Accomplishment**: Generalized the ADK agent template by copying the pristine `.agents/` memory protocol directory directly into the starter kit for an out-of-the-box self-contained experience. Replaced hardcoded values in `main.py` with environment variable overrides (`AGENT_NAME`, `AGENT_MODEL`, `AGENT_DESCRIPTION`, `LOCATION` / `GOOGLE_CLOUD_LOCATION`) to allow easy developer customization. Documented all configuration options in `README.md`, and explicitly added `google-genai` to dependencies.
*   **Decisions**: Include the pristine `.agents/` folder inside `adk-agent-template/` to provide a complete, self-contained starter project. Externalize agent metadata and model/location variables to allow dynamic runtime configuration without changing code.

### Sprint: Instantiation and Drift Automation
*   **Accomplishment**: Created `scripts/sync-templates.py` to recursively sync core memory rules, workflows, and skills from the source of truth (`template/.agents/`) to active configurations, completely eliminating manual synchronization drift. Created `scripts/create-agent.py` as an interactive, one-command project bootstrapper CLI that automatically copies template structures, runs interactive environment configuration interviews, generates local `.env` setups, initializes git, and configures python virtual environments.
*   **Decisions**: Enforce `template/.agents/` as the single source of truth for protocol files. Provide high-quality automation tooling in `scripts/` to maximize convenience and simplify the developer onboarding journey.

### Sprint: Calendar Advisor Agent Integration
*   **Accomplishment**: Created a new autonomous agent project (`CalendarAgent/`) under `Dev` based on `CalendarV2`. Ported the parallel availability query execution from `CalendarV2` into `calendar_tools.py` using `gcloud compute advice calendar-mode`. Registered tools in the ADK agent structure for listing machine types, regions, and executing queries. Hardened type validation and test coverage.
*   **Decisions**: Extracted file editing/creation tools to keep the advisor agent strictly focused on resource availability.



