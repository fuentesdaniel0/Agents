# Agent Protocol Evaluation Script

This document provides a manual QA testing script to verify if your AI coding assistant (e.g., Google Antigravity, Copilot Workspace) correctly adheres to the `.agents/` protocol architecture.

Since AI agents are non-deterministic, you must test them behaviorally using the prompts below. 

## Prerequisites
1. Ensure you have copied the `template/.agents/` directory into your workspace root as `.agents/`.
2. Open a **brand new chat session** in your AI IDE. Do not use an existing chat history.

---

## Phase 1: Initialization Test (`startup.md`)

This tests whether the agent correctly executes its Startup SOP without being explicitly asked to read files.

**Your Prompt:**
> "What is the current state of our project and what is my next task?"

**Expected Agent Behavior:**
- The agent should **not** hallucinate an answer.
- It should automatically read `.agents/memory/context.md` and `.agents/memory/backlog.md` (specifically looking for the "Next Session Focus").
- It should respond by either quoting the placeholders in the memory files or accurately summarizing the current tracked state.

---

## Phase 2: Workflow Intake Test (`/plan`)

This tests if the agent correctly triggers an interactive, multi-step workflow without rushing.

**Your Prompt:**
> "/plan"

**Expected Agent Behavior:**
- The agent should determine if the project is initialized.
- It should ask you a series of questions (Project Name, Tech Stack, Milestones, Constraints) or ask you which roadmap items to pull into the active backlog.
- **Crucial Verification**: The agent must *stop and wait* for your response before proceeding to update the memory files. It should not answer its own questions.

---

## Phase 3: Operational Discipline Test (`core-directives.md`)

This tests if the agent honors ambient constraints regarding active exploration and verification.

**Your Prompt:**
> (Provide dummy answers to the `/plan` interview if it asks). Then say: "Okay, let's create a new math utilities module."

**Expected Agent Behavior:**
- The agent should **not** instantly write a random file in a hallucinated directory.
- It should use a tool like `list_dir` or `grep_search` to verify the repository structure first.
- It should optionally invoke the `scaffold-module` skill.
- After generating the boilerplate, it should attempt to run a build, lint, or test command (as mandated by the `Verification-First Development` directive) before declaring the task complete.

---

## Phase 4: State Commitment Test (`/checkpoint`)

This tests the session wrap-up and memory rotation protocols.

**Your Prompt:**
> "/checkpoint"

**Expected Agent Behavior:**
- The agent should run `git status`.
- It should update `context.md` and append to `changelog.md`.
- It should execute the project's native build/test commands.
- It should propose a `git commit` with a summarized message.
- It should ask you what the focus should be for the *next* session so it can populate `backlog.md`.

---

### Test Results
If your agent successfully executes all four phases, your memory system and protocol rules are correctly synchronized with the AI engine!
