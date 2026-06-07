# Epoch: Contextual Memory for AI Assistants

Give your AI coding assistant persistent memory with zero databases. A drop-in Markdown protocol for stateful, multi-session development. This repository provides a simple directory structure of **rules, skills, workflows, and version-controlled memory templates** designed to give AI agents (like Cursor, Google Antigravity, or GitHub Copilot Workspaces) persistent, highly-optimized context across multiple development sessions.

## The Problem
AI agents operate in isolated sessions. As projects grow, context windows fill up with useless chat history, causing latency, higher API costs, and degraded performance. If you start a fresh session, the AI forgets your architecture, active tasks, and strict coding rules.

## The Solution
This repository establishes a **Developer-Agent Synchronization Protocol**. It provides a structured, version-controlled markdown "memory" system and automated agent scripts.
- **Instant Context**: Agents read a summarized `context.md` file on startup instead of parsing massive chat histories.
- **Automated Checkpoints**: A native workflow (`/checkpoint`) automatically compiles tests, summarizes work, and commits state to memory files before closing a session.
- **Strict Guidelines**: Project rules (`startup.md`, `core-directives.md`) automatically enforce testing, linting, and architectural alignment.

---

## Repository Structure

### 1. `.agents/` (The AI Engine)
Native configurations, automations, and constraints for the AI agent.
- **`rules/`**: Contextual guidelines that automatically inject into the agent's prompt (e.g., `startup.md` forces the agent to read memory files upon initialization).
- **`skills/`**: Optional executable macros and custom tools (e.g., an `automated-deployment` script).
- **`workflows/`**: Interactive step-by-step procedures (e.g., `/plan` to scaffold or groom a project, `/checkpoint` to wrap up a session).
- **`prompts/`**: Modular system prompts for specialized tasks and personas.

### 2. `.agents/memory/` (The Project Memory)
Blank templates for version-controlled state retention.
- **`context.md`** – The active state, current architecture, code graph, and environmental variables.
- **`changelog.md`** – A chronological timeline of completed sprints and architectural decisions.
- **`backlog.md`** – The product backlog, roadmap, and pending tasks.

---

## Quick Start (How to Use)

To apply this intelligence layer to any of your own projects, simply copy these two directories into the root of your new or existing repository:

```bash
# 1. Copy the agent configurations and memory templates to your project
cp -a template/.agents /path/to/your/new/project/

# 2. Open your project in your AI IDE
cd /path/to/your/new/project/
```

### The Continuous Development Loop
Once installed, follow this "Plan-Do-Check-Act" development loop:

1. **Initialize the Project**: In a new chat session, type `/plan`. The agent will interview you about your tech stack and goals, automatically populating the blank memory templates for you.
2. **Sprint Planning**: At the start of a session, if the project is already initialized, type `/plan` or `/sprint`. The agent will review `backlog.md`, groom the queue with you, and set the immediate "Session Focus".
3. **Start a Work Session**: When you start a fresh chat in the future, the `startup.md` rule automatically forces the agent to read `context.md` and the "Session Focus" from `backlog.md`. It syncs with your project in seconds.
4. **Wrap Up**: When you are done coding, type `/checkpoint`. The agent will run the checkpoint workflow—running your tests, summarizing the session, updating the memory files, committing state, and asking you what the focus should be for the *next* session. 
5. **Reset**: Open a fresh, clean chat window for your next task with zero token bloat!

---

## Customizing
You are highly encouraged to modify these files! 
- Add custom linters or build steps to the `checkpoint.md` workflow.
- Add specific architectural rules to the `.agents/rules/` directory (e.g., `tailwind-rules.md`).
- Create new modular prompts under `.agents/prompts/`.
