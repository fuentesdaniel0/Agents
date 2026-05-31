# Agent Protocols & Contextual Memory

A modular "brain" for AI coding assistants. This repository provides a drop-in directory structure of **rules, skills, workflows, and version-controlled memory templates** designed to give AI agents (like Google Antigravity or GitHub Copilot Workspaces) persistent, highly-optimized context across multiple development sessions.

## The Problem
AI agents operate in isolated sessions. As projects grow, context windows fill up with useless chat history, causing latency, higher API costs, and degraded performance. If you start a fresh session, the AI forgets your architecture, active tasks, and strict coding rules.

## The Solution
This repository establishes a **Developer-Agent Synchronization Protocol**. It provides a structured, version-controlled markdown "memory" system and automated agent scripts.
- **Instant Context**: Agents read a summarized `current.md` file on startup instead of parsing massive chat histories.
- **Automated Checkpoints**: A native skill (`/checkpoint`) automatically compiles tests, summarizes work, and commits state to memory files before closing a session.
- **Strict Guidelines**: Project rules (`startup.md`, `agentic-coding.md`) automatically enforce testing, linting, and architectural alignment.

---

## Repository Structure

### 1. `.agents/` (The AI Engine)
Native configurations, automations, and constraints for the AI agent.
- **`rules/`**: Contextual guidelines that automatically inject into the agent's prompt (e.g., `startup.md` forces the agent to read memory files upon initialization).
- **`skills/`**: Executable macros and custom tools (e.g., the `session-checkpoint` script).
- **`workflows/`**: Interactive step-by-step procedures (e.g., `/intake` to scaffold a new project).
- **`prompts/`**: Modular system prompts for specialized tasks and personas.

### 2. `project_tracking/` (The Project Memory)
Blank templates for version-controlled state retention.
- **`memory/protocol.md`** – The standard operating procedures for the agent lifecycle.
- **`memory/current.md`** – The active state, current code graph, and environmental variables.
- **`memory/history.md`** – A chronological timeline of completed sprints and architectural decisions.
- **`memory/future.md`** – The product backlog, roadmap, and pending tasks.

---

## Quick Start (How to Use)

To apply this intelligence layer to any of your own projects, simply copy these two directories into the root of your new or existing repository:

```bash
# 1. Copy the agent configurations and memory templates to your project
cp -a .agents project_tracking /path/to/your/new/project/

# 2. Open your project in your AI IDE
cd /path/to/your/new/project/
```

### The Standard Workflow
Once installed, follow this development loop:

1. **Initialize the Project**: In a new chat session, type `/intake`. The agent will interview you about your tech stack and goals, automatically populating the blank memory templates for you.
2. **Start a Work Session**: When you start a fresh chat in the future, the `startup.md` rule automatically forces the agent to read `current.md` and `protocol.md`. It syncs with your project in seconds.
3. **Wrap Up**: When you are done coding, type `"let's checkpoint"`. The agent will automatically trigger the `session-checkpoint` skill—running your tests, summarizing the session, updating the memory files, and staging a git commit. 
4. **Reset**: Open a fresh, clean chat window for your next task with zero token bloat!

---

## Customizing
You are highly encouraged to modify these files! 
- Add custom linters or build steps to the `session-checkpoint` skill.
- Add specific architectural rules to the `.agents/rules/` directory (e.g., `tailwind-rules.md`).
- Create new modular prompts under `.agents/prompts/`.
