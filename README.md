# Epoch: Contextual Memory for AI Assistants

A drop-in Markdown protocol that gives AI coding assistants (Cursor, GitHub Copilot Workspaces) persistent, stateful memory across sessions—zero databases required.

## The Problem
AI agents lose context between sessions. Dumping raw chat history into context windows causes token bloat, latency, and forgotten architecture.

## The Solution
A version-controlled file structure that synchronizes your agent's state:

- **Instant Context**: Agents read a concise `context.md` on startup instead of parsing chat history.
- **Automated Checkpoints**: Running `/checkpoint` summarizes work and commits state before closing a session.
- **Strict Enforcement**: Rules (`startup.md`) automatically enforce testing, linting, and architectural alignment.

## Repository Structure

### 1. `.agents/` (The Engine)
Configurations, automations, and constraints for the AI agent.

- **`rules/`**: Contextual guidelines automatically injected into prompts.
- **`skills/`**: Executable macros and custom tools.
- **`workflows/`**: Interactive step-by-step procedures (`/plan`, `/checkpoint`).
- **`prompts/`**: Modular system prompts for specialized tasks.

### 2. `.agents/memory/` (The State)
Blank templates for version-controlled state retention.

- **`context.md`**: Active architecture, code graph, and environment state.
- **`changelog.md`**: Chronological sprint history and architectural decisions.
- **`backlog.md`**: Product roadmap and pending tasks.

## Quick Start
Drop the `.agents` directory into the root of any new or existing repository.

```bash
cp -a template/.agents /path/to/your/project/
cd /path/to/your/project/
```

## The Development Loop
- **Initialize**: Type `/plan` in a new chat. The agent interviews you to populate the memory files.
- **Plan Sprint**: Type `/sprint`. The agent reviews `backlog.md` and sets the session focus.
- **Work**: Open a fresh chat. `startup.md` forces the agent to read `context.md` and sync instantly.
- **Wrap Up**: Type `/checkpoint`. The agent runs tests, updates memory files, and commits state.
- **Reset**: Open a clean chat window for the next task with zero token bloat.

## Customization
Modify these files to fit your stack:

- Add custom linters or build steps to the `checkpoint.md` workflow.
- Inject specific architectural rules into `.agents/rules/`.
- Create new modular personas under `.agents/prompts/`.
