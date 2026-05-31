# Project Tracking Directory

This directory contains resources for tracking the progress of the **antigravity-test** project. It includes tools, documentation, and prompts that help organize milestones, tasks, and career development.

## Structure

- `career_coach_prompt.txt` – System prompt for an elite Software Engineering career coach. Use this prompt to guide an AI assistant in providing high‑impact career advice, interview preparation, and skill‑building recommendations.
- `initialize_agent.txt` – Prompt configuration that instructs incoming agents to sync state from repository memory.
- `memory/` – Version-controlled project state retention:
  - `history.md` – Chronological milestones and completed sprints.
  - `current.md` – Current code graph, credentials, validation flags, and active packages.
  - `future.md` – Product backlog, roadmap, and future tasks.
  - `protocol.md` – Synchronization SOPs and context reset parameters.
- `README.md` – Overview of the tracking system and how to contribute.

---

## 🔁 Agent Workflows

We use native **Antigravity Workflows** for project automation instead of manual prompts. You can find these in `.agents/workflows/` (e.g. `/init`).
