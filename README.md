# Agent Protocols

This repository contains reusable agent protocols, rules, skills, workflows, and project tracking memory designed for Antigravity-powered agentic coding workspaces.

## Structure

### `.agents/` (Antigravity Customizations)
This directory contains native configurations for the Antigravity Agent. You can copy this into any new repository to inherit these behaviors.
- **`rules/`**: Contextual guidelines and constraints (e.g., `agentic-coding.md`, `react-components.md`, `startup.md`). These ensure the agent operates strictly within the defined architecture and workflows.
- **`skills/`**: Extended capabilities with specific tool conventions (e.g., `react-testing`).
- **`workflows/`**: Automated step-by-step procedures (e.g., `init.md`).

### `project_tracking/` (Contextual Memory)
This directory contains the milestone tracking and state retention memory files.
- **`career_coach_prompt.txt`**: A system prompt for an elite Software Engineering career coach.
- **`memory/`**: Version-controlled project state.
  - `history.md` – Chronological milestones and completed sprints.
  - `current.md` – Current code graph, credentials, validation flags, and active packages.
  - `future.md` – Product backlog, roadmap, and future tasks.
  - `protocol.md` – Synchronization SOPs and context reset parameters.

## How to Reuse

To apply these protocols to a new repository, simply copy the `.agents/` directory into the root of your new project:
```bash
cp -a .agents /path/to/your/new/project/
```
Once copied, Antigravity will automatically detect the rules, skills, and workflows when you open the new project workspace.
