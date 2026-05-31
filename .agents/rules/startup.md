---
activation: always_on
---
When the user first opens this workspace or starts a new chat session, you MUST immediately perform the following steps before proposing any changes:
1. Proactively check if the project is initialized. You can suggest they run the `/init` workflow to quickly set up their environment (install dependencies, check env files, etc.).
2. Read the Developer-Agent Synchronization Protocol located at `project_tracking/memory/protocol.md`.
3. Load the active state by reading `project_tracking/memory/current.md` to synchronize with the current architecture, environment, and verification guidelines. Do NOT read history.md or future.md unless explicitly required by the user's request.
