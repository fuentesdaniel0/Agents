# Product Backlog & Future Tasks

This file outlines the upcoming milestones, roadmap, and individual feature tasks planned for this repository. When an agent completes a task, it should be removed from this list and documented in `changelog.md`.

---

## Session Focus

*This section dictates the immediate priority for the next AI agent session. It is populated during the `/checkpoint` wrap-up or via `/plan`.*

- [ ] TBD - Run `/plan` to groom new features and backlog items.

---

## High-Level Roadmap

### Milestone 1: Template Separation (Completed)
*   **Feature 1**: Isolate the pristine template into `template/.agents/`.
*   **Feature 2**: Re-initialize the root `.agents/` to track repository development.

### Milestone 2: Publish and Distribute (Completed)
*   [x] **Feature 1**: Generalize ADK agent template structure and environment configuration (embed `.agents/` memory, externalize metadata/location environment variables).
*   [x] **Feature 2**: Implement template sync tool (`scripts/sync-templates.py`) to prevent rule/workflow drift.
*   [x] **Feature 3**: Implement interactive agent bootstrapper CLI (`scripts/create-agent.py`) to automate project instantiation.
*   [x] **Feature 4**: Prepare for v1.0 tag.

### Milestone 3: ADK Agent Template & FastAPI Deployment (Completed)
*   **Feature 1**: Design and scaffold ADK agent template directory with Epoch memory integration.
*   **Feature 2**: Expose agent via standard FastAPI server and endpoints.
*   **Feature 3**: Provide deployment configurations (Dockerfile, Cloud Run deployment commands, and setup guide).

### Milestone 4: Agent Factory (Completed)
*   [x] **Feature 1**: Establish an Agent Factory pattern to dynamically define, configure, and instantiate ADK-compatible agents.

### Continuous Milestone: Meta-Planning & Agent Improvement (Completed)
*   [x] **Feature 1**: Evaluate agent performance across workflows and refine `.agents/` constraints.
*   [x] **Feature 2**: Ideate new skills or interactive slash commands to augment autonomy.

### Milestone 10: Slash Command Integration (Completed)
*   [x] **Feature 1**: Design and implement the `/evaluate` workflow to run Vertex AI evaluations and display scorecards.
*   [x] **Feature 2**: Design and implement the `/security` workflow to run local credential scans on-demand.
*   [x] **Feature 3**: Register the new slash commands in the default ADK agent configuration and developer documentation.


### Milestone 5: Non-Git Centric Epoch (Completed)
*   [x] **Feature 1**: Create a branch for a version of Epoch that is not git centric (goal: maximize efficacy and track iterative project development).

### Milestone 6: Continuous Evaluation Flow (Completed)
*   [x] **Feature 1**: Define a golden dataset of agent workflow scenarios for regression testing.
*   [x] **Feature 2**: Script the Vertex AI Gen AI Evaluation Service pipeline for ADK agent runs.
*   [x] **Feature 3**: Configure automated CI/CD evaluation checks on rule/workflow template modifications.

### Milestone 7: Secure Push & Security Evaluation Flow (Completed)
*   [x] **Feature 1**: Design a pre-push validation workflow/step that runs security scanning (secrets, vulnerability scanners) before pushes.
*   [x] **Feature 2**: Integrate security verification into `checkpoint.md` to ensure any push command runs the scanner first.

### Milestone 8: Milestone Review Workflow (Completed)
*   [x] **Feature 1**: Design and implement a milestone review workflow (e.g., `/milestones` or `/review-milestones`) under `.agents/workflows/`.
*   [x] **Feature 2**: Parse `.agents/memory/backlog.md` to dynamically display the available high-level milestones.
*   [x] **Feature 3**: Prompt the user to select the current active milestone to work on.
*   [x] **Feature 4**: Automatically update the `Session Focus` or `Active Backlog Tasks` based on the user's selection.

### Milestone 9: Usability Testing & Context Blot Assessment (Completed)
*   [x] **Feature 1**: Develop and run a usability integration test script to dry-run template creation and synchronization.
*   [x] **Feature 2**: Implement the "Memory Rotation & Archiving" protocol for `changelog.md` to prune older sprints into an archive folder.
*   [x] **Feature 3**: Audit active rules (`core-directives.md`, `startup.md`) and workflows to minimize token overhead/context blot.

---

## Active Backlog Tasks

- [x] Run initial baseline evaluation check (`ci_eval_check.py`) to verify current performance.
- [x] Inspect evaluation output, logs, and scorecards for any rule deviations or inefficiencies.
- [x] Review active constraints (e.g., `core-directives.md`, `startup.md`) and refine them for brevity and adherence.
- [x] Run verification tests and evaluations to validate changes.

