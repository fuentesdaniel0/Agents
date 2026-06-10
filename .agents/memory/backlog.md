# Product Backlog & Future Tasks

This file outlines the upcoming milestones, roadmap, and individual feature tasks planned for this repository. When an agent completes a task, it should be removed from this list and documented in `changelog.md`.

---

## Session Focus

*This section dictates the immediate priority for the next AI agent session. It is populated during the `/checkpoint` wrap-up or via `/plan`.*

- [ ] Prepare for v1.0 tag.

---

## High-Level Roadmap

### Milestone 1: Template Separation (Completed)
*   **Feature 1**: Isolate the pristine template into `template/.agents/`.
*   **Feature 2**: Re-initialize the root `.agents/` to track repository development.

### Milestone 2: Publish and Distribute
*   [x] **Feature 1**: Generalize ADK agent template structure and environment configuration (embed `.agents/` memory, externalize metadata/location environment variables).
*   [ ] **Feature 2**: Prepare for v1.0 tag.

### Milestone 3: ADK Agent Template & FastAPI Deployment (Completed)
*   **Feature 1**: Design and scaffold ADK agent template directory with Epoch memory integration.
*   **Feature 2**: Expose agent via standard FastAPI server and endpoints.
*   **Feature 3**: Provide deployment configurations (Dockerfile, Cloud Run deployment commands, and setup guide).

### Milestone 4: Enable A2A Interoperability
*   **Feature 1**: Wrap agent with `to_a2a()` wrapper and resolve `starlette` / `sse-starlette` dependency requirements.
*   **Feature 2**: Configure public Agent Card endpoint at `/.well-known/agent-card.json`.

### Milestone 5: Agent Factory & Calendar Advisor Agent Integration
*   **Feature 1**: Establish an Agent Factory pattern to dynamically define, configure, and instantiate ADK-compatible agents.
*   **Feature 2**: Refactor and integrate the Calendar Advisor UI project logic as an autonomous agent registered with the factory.

### Continuous Milestone: Meta-Planning & Agent Improvement
*   **Feature 1**: Evaluate agent performance across workflows and refine `.agents/` constraints.
*   **Feature 2**: Ideate new skills or interactive slash commands to augment autonomy.


---

## Active Backlog Tasks

- [ ] No active tasks remaining.
