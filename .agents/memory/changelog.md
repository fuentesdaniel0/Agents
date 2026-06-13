# Project History & Milestone Timeline

This file captures the chronological history of milestones, architectural decisions, and tasks completed in the repository.

---

## Sprint Chronology

> [!NOTE]
> Sprints and milestones 1 through 5 (including Core Protocol Setup, Generalization & Directives, Rebranding, ADK Integration, FastAPI Deployment, Automation, and Git-De-coupling) have been archived.
> See the full history in [changelog-v1.md](file:///usr/local/google/home/fuentesdaniel/Dev/Epoch/.agents/memory/archive/changelog-v1.md).

---

### Sprint: Continuous Meta-Evaluation & Constraint Refinement
*   **Accomplishment**: Completed the final milestone "Continuous Milestone: Meta-Planning & Agent Improvement". Conducted baseline evaluation runs using `ci_eval_check.py` and identified key gaps in agent responses (such as failing to explicitly report file listing/exploration and verification execution). Refined the template agent's system instructions in `adk-agent-template/main.py` to mandate explicit confirmation of file listing (Active Exploration) and verification commands (Verification-First), and listed files in `/checkpoint` response, achieving a perfect 5.00/5.00 score across all evaluation scenarios.
*   **Decisions**: Enforce that the agent's natural-language output must confirm protocol steps (listing files, running verification commands, and saving checkpoints) so that the Gen AI Evaluation Service judge can reliably verify protocol adherence.

### Sprint: Slash Command Integration
*   **Accomplishment**: Completed Milestone 10. Designed and implemented the `/evaluate` workflow under `.agents/workflows/evaluate.md` to execute Vertex AI agent evaluation and show structured scorecards. Designed and implemented the `/security` workflow under `.agents/workflows/security.md` to execute local credential scans on-demand. Registered both commands in the `epoch_agent` instructions in `adk-agent-template/main.py` and documented them in `README.md`. Synchronized pristine and active memory configurations.
*   **Decisions**: Expose `/evaluate` and `/security` as standard interactive commands to allow on-demand testing and safety checks directly from the chat interface, and update distribution templates to align active rules and workflows.

### Sprint: Google Cloud Storage MCP Configuration Correction
*   **Accomplishment**: Fixed a connection error ("Bad Request" / "AccessDenied") during client initialization of the `google-cloud-storage` MCP server. Corrected the endpoint URL from `https://storage.googleapis.com/mcp` to `https://storage.googleapis.com/storage/mcp` in both `.agents/mcp_config.json` and `.agents/settings.json`.
*   **Decisions**: Point to the correct service-prefixed path (`/storage/mcp`) for GCS MCP endpoints to prevent the cloud storage API from interpreting the request as bucket-level operations.

### Sprint: Milestone Review Workflow Implementation
*   **Accomplishment**: Designed, implemented, and verified the Milestone Review Workflow (`/milestones` or `/review-milestones`) under `template/.agents/workflows/milestones.md`. Programmatically validated the protocol using a newly created verification script `verify-milestones.py` which parses the backlog template and active meta backlogs to classify active, completed, and upcoming milestones correctly.
*   **Decisions**: Create a dedicated script to verify that roadmap files comply with completion and structure rules, preventing manual parsing issues when agents operate on new projects. Use template sync rules to propagate scripts and workflows cleanly across active development and deployment structures.

### Sprint: Milestone 2 Completion and Roadmap Pruning
*   **Accomplishment**: Completed all remaining features for Milestone 2 (Publish and Distribute) by syncing rules and workflows across template and active locations, verifying roadmap formats using `verify-milestones.py`, and dry-running/validating the agent bootstrapper CLI (`create-agent.py`). Verified that starter template unit tests are 100% green. Removed Milestone 4 (A2A Interoperability) and pruned the Calendar Advisor agent integration from Milestone 4 (Agent Factory) to focus strictly on core repository capabilities.
*   **Decisions**: Exclude the Calendar Advisor UI agent integration from this repo to keep the codebase focused purely on the core Epoch memory protocol and bootstrap templates. Renumber active milestones cleanly to prevent gaps.

### Sprint: Agent Factory Pattern Implementation
*   **Accomplishment**: Implemented the Agent Factory pattern in `adk-agent-template`. Defined the `AgentConfig` schema with a field validator to enforce that agent names must be valid Python identifiers. Developed `AgentRegistry` to manage CRUD operations for dynamic agent configurations and persist them to a JSON file. Developed the `AgentFactory` to instantiate ADK agents and runners with selected tools. Refactored main tools to `tools.py` to prevent circular dependencies. Added FastAPI endpoints for POST, GET, and DELETE operations under `/agents`, and updated `/run` and `/agents/{name}/run` to route execution dynamically. Added comprehensive unit and integration test suites, raising test coverage to 25 passing tests.
*   **Decisions**: Enforce that agent names must be valid Python identifiers to prevent pydantic/ADK validation failures downstream. Store agent configurations in a local JSON registry file (`agents_registry.json`) under the configured memory directory to maintain persistent memory. Separate standard agent tools into `tools.py` to keep the architecture clean and avoid circular import dependencies between the API endpoints, factory, and tests.

### Sprint: Secure Push & Checkpoint Verification
*   **Accomplishment**: Implemented Milestone 7 (Secure Push & Security Evaluation Flow). Developed a local self-contained security scanner script (`security-check.py`) that checks for Google API keys, AWS access keys, Slack webhooks, GitHub tokens, private key blocks, and generic password/key assignments. Added an inline exclusion feature via `# epoch-secret-ignore` to easily mark false positives. Implemented 8 robust unit tests for the scanner (`test_security_check.py`) confirming detection capabilities. Integrated the security scan as a mandatory gatekeeper verification step in `checkpoint.md`, strictly preventing commits if any secrets are detected. Fixed a project root path resolution traversal bug in the template synchronizer script.
*   **Decisions**: Enforce local client-side security checks as a blocking verification step during checkpoints to prevent accidental secret leaks. Allow inline comment suppression (# epoch-secret-ignore) to keep the flow lightweight while maintaining a high degree of security. Exclude the scanner test script from scanning to avoid false positives on mock key definitions.

### Sprint: Continuous Evaluation Flow
*   **Accomplishment**: Completed Milestone 6. Defined a golden evaluation dataset (`dataset.json`) covering 4 key behavioral scenarios (Startup Sync, Create/Verify, Checkpoint, and Safety). Authored the evaluation execution pipeline (`run_eval.py`) that isolates the agent in temporary workspaces, runs the live agent to obtain responses, and calls the Vertex AI Gen AI Evaluation Service to judge Goal Completion, Protocol Adherence, and Safety. Authored `ci_eval_check.py` to enforce a mean evaluation score gate of >= 4.0. Strengthened the template agent's system instructions in `main.py` to mandate active exploration, verification commands, and proper slash command execution, achieving a perfect 5.00/5.00 evaluation check score.
*   **Decisions**: Dynamically instantiate a fresh `VertexGemini` model and `Agent` instance for each evaluation run to avoid closed event loop errors from the underlying `google-genai` client. Enforce strong system instructions mandating specific tool sequences (e.g., listing files before writing, running verification commands after file writes) to guarantee protocol compliance.

### Sprint: Documentation Sync & Template Alignment
*   **Accomplishment**: Audited and fully updated the root `README.md`, root `EVALUATION.md`, `adk-agent-template/README.md`, and `adk-agent-template/TESTING.md`. Documented the new dynamic Agent Factory FastAPI routes/registry, the `/milestones` review workflow, and the pre-push security scanner script. Replaced template memory placeholders in `adk-agent-template/.agents/memory/` with pristine template roadmaps to satisfy milestone verification checks.
*   **Decisions**: Keep documentation in sync with stripped A2A dependency features, replacing them with dynamic Agent Factory instructions. Standardize memory files in distribution templates to prevent parsing failures on milestone verification tools.

### Sprint: Meta-Planning & Rules Audit
*   **Accomplishment**: Audited the ADK agent template evaluation dataset (`dataset.json`) and run-eval configurations. Evaluated the active rules (`core-directives.md` and `securecoder_generation/SKILL.md`) for gaps or over-constraints. Brainstormed new commands (`/evaluate`, `/security`) and helper skills (`python-code-quality`, `dependency-security-checker`) to enhance autonomy.
*   **Decisions**: Create custom workflow commands for evaluating and scanning the repo. Recommend refining the rules to include python style rules and prune web-specific guidelines.

### Sprint: Usability Testing & Context Blot Assessment
*   **Accomplishment**: Completed Milestone 9. Authored a usability test suite (`test_usability.py`) to dry-run bootstrapper and synchronizer templates, discovering and fixing a project root traversal path bug in `create-agent.py`. Implemented memory rotation by archiving sprints for Milestones 1 to 5 into `archive/changelog-v1.md`. Consolidated validation rules in `core-directives.md` to prevent context token blot.
*   **Decisions**: Merge redundant verify-first loop rules. Clean active repository memory files regularly to preserve token window efficiency.



