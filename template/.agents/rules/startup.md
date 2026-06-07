---
trigger: always_on
---

# System Initialization & Memory Context

You are operating within a repository equipped with an automated contextual memory system. To maintain a stateless, lightweight chat context, project state is persisted in the `.agents/memory/` directory.

### Memory Directory Structure
- **`context.md`**: The active state, current architecture, code graph, and environmental variables.
- **`backlog.md`**: The product backlog, roadmap, and pending tasks. The "Next Session Focus" at the top dictates immediate priorities.
- **`changelog.md`**: A chronological timeline of completed sprints and architectural decisions.

### Startup Standard Operating Procedure (SOP)

When the user first opens this workspace or starts a new chat session, execute the following **Startup SOP**:

1. Silently read `.agents/memory/context.md` to align with the active state and rules.
2. Silently read the top of `.agents/memory/backlog.md` to check the "Next Session Focus".
3. If the backlog contains tasks, proactively summarize the "Next Session Focus" to the user and ask if they are ready to begin, or if they would prefer to run `/plan` to groom the backlog. Else, propose to run `/plan`.
