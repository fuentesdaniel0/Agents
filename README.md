# Epoch: Contextual Memory for AI Assistants

A drop-in Markdown protocol that gives AI coding assistants (Cursor, GitHub Copilot Workspaces) persistent, stateful memory across sessions—zero databases required.

## Problem

AI agents lose context between sessions. Dumping raw chat history into context windows causes token bloat, latency, and forgotten architecture.

## Solution

A version-controlled file structure that synchronizes your agent's state:

- **Instant Context**: Agents read a concise `context.md` on startup instead of parsing chat history.
- **Automated Checkpoints**: Running `/checkpoint` summarizes work and commits state before closing a session.
- **Strict Enforcement**: Rules (`startup.md`) automatically enforce testing, linting, and architectural alignment.

## Repository Structure

This repository uses **Epoch to develop and improve Epoch itself** (dogfooding). The active configuration and memory files are kept at the root of the repository.

### 1. `.agents/` (Active Meta-Memory)
Tracks the development of *this* repository itself.
- **`memory/`**: Active state trackers ([context.md](file:///usr/local/google/home/fuentesdaniel/Dev/Epoch/.agents/memory/context.md), [backlog.md](file:///usr/local/google/home/fuentesdaniel/Dev/Epoch/.agents/memory/backlog.md), [changelog.md](file:///usr/local/google/home/fuentesdaniel/Dev/Epoch/.agents/memory/changelog.md)) documenting our current milestones and rules.
- **`rules/`**, **`skills/`**, **`workflows/`**: Active instructions governing the assistant operating in this workspace.

### 2. `template/.agents/` (Pristine Starter Kit)
Contains the **fresh, ready-to-use project structure** and blank templates. Copy this directory to any project repository to initialize the Epoch memory protocol.
- **`memory/`**: Blank Markdown files (`context.md`, `backlog.md`, `changelog.md`) ready for project discovery and planning.
- **`rules/`**, **`workflows/`**: Standard rule-sets, startup SOPs, and commands (`/plan`, `/checkpoint`).
- **`scripts/`**: Setup and synchronization CLI utilities.

### 3. `adk-agent-template/` (FastAPI / Agent Engine Deployment)
An out-of-the-box **ADK implementation of Epoch**. It wraps the Epoch memory protocol in a Python microservice using Google's Agent Development Kit (ADK), ready for deployment to **Vertex AI Agent Engine** or **Google Cloud Run**.


## Quick Start

Depending on your requirements, choose one of the following setup paths:

### Path A: Create a Complete Python ADK Agent (FastAPI/Vertex AI)
To scaffold a new Python microservice agent project complete with local memory, virtual environment, and deployment configurations:

```bash
# Run the bootstrapper CLI
python3 template/.agents/scripts/create-agent.py /path/to/your/new-project

```
This utility will guide you through config setups and create a self-contained project workspace at `/path/to/your/new-project`.

### Path B: Add Memory Protocol to an Existing Project (Any Language)
To drop Epoch's contextual memory tracking protocol into an existing repository of any tech stack:

```bash
# Copy the pristine memory protocol structure
cp -a template/.agents /path/to/your/existing-project/
```
Once copied, open your IDE AI assistant in `/path/to/your/existing-project/` and type `/plan` to begin.

- **Initialize**: Type `/plan` in a new chat. The agent interviews you to populate the memory files.
- **Review Milestones**: Type `/milestones` (or `/review-milestones`). The agent parses and groups project milestones from `backlog.md` into Completed, Active, and Upcoming, prompting you to set the current session focus milestone.
- **Plan Sprint**: Type `/sprint`. The agent reviews `backlog.md` and sets the session focus.
- **Work**: Open a fresh chat. `startup.md` forces the agent to read `context.md` and sync instantly.
- **Evaluate**: Type `/evaluate`. The agent triggers the Vertex AI Gen AI evaluation pipeline on-demand, parses results, and presents a scorecard.
- **Security Check**: Type `/security`. The agent runs the local security scanner to inspect the codebase for secrets or credentials.
- **Wrap Up**: Type `/checkpoint`. The agent runs the local security scanner, executes tests, updates memory files, and commits state.
- **Reset**: Open a clean chat window for the next task with zero token bloat.

## Helper Scripts

Epoch comes with a set of developer automation scripts located in `template/.agents/scripts/`:

- **`create-agent.py`**: An interactive bootstrapping CLI tool. Pass a target directory path (e.g., `python3 template/.agents/scripts/create-agent.py /path/to/project`) to copy the pristine template structure, guide you through config, generate local `.env` setups, setup virtual environments, and configure git.
- **`sync-templates.py`**: A synchronization script that recursively syncs rules, workflows, and skills from the source of truth (`template/.agents/`) to active setups, preventing drift.
- **`security-check.py`**: A standalone pre-push credential and secret scanner. It checks for Google API keys, AWS keys, GitHub tokens, private keys, and passwords. Use `# epoch-secret-ignore` to suppress false positives on any line.
- **`verify-milestones.py`**: A validation script that programmatically parses backlog roadmaps (both pristine templates and active backlogs) to verify their format, milestone groups, and completion states.

## Customization

Modify these files to fit your stack:

- Add custom linters or build steps to the `checkpoint.md` workflow.
- Inject specific architectural rules into `.agents/rules/`.
- Customize the automated evaluation scenarios in `adk-agent-template/evaluation/dataset.json`.

