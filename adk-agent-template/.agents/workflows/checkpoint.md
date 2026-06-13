---
name: session-checkpoint
description: Interactive workflow to execute the project checkpoint protocol and wrap up a session. Trigger this via `/checkpoint`.
---

# Session Checkpoint Workflow

When the user triggers the `/checkpoint` command or asks to prepare to close the session, you must execute the following protocol in exactly this order:

## 1. Status Check
- Review your recent tool calls, actions, and modified files to summarize what you accomplished. If the workspace is a Git repository, you may run `git status` to help identify modified files, but do not rely on it as the only method.

## 2. Memory & Tracker Updates
- **Update Active State**: Update `.agents/memory/context.md` to reflect any new architectural changes, active state, or newly established patterns.
- **Task Migration**: Move completed tasks from `.agents/memory/backlog.md` (Active Backlog Tasks) into `.agents/memory/changelog.md`.
- **Chronological History**: Append a brief narrative summary of the session's completed milestones to `.agents/memory/changelog.md`.
- **Memory Rotation & Archiving**: Check the size of `.agents/memory/changelog.md`. If it is growing too long (e.g., tracking more than the last 3 major milestones), automatically move the oldest entries into an archive file (e.g., `.agents/memory/archive/changelog-v1.md`) to preserve context window tokens.

## 3. Next Session Planning
- Interactively ask the user: *"What should our primary focus be for the next session?"*
- Inject their response into the "Session Focus" section at the top of `.agents/memory/backlog.md`.

## 4. Verification
- **Mandatory Security Scan**: Run the local security scanner: `python3 .agents/scripts/security-check.py`.
  - **CRITICAL**: If the security check fails (exit code is non-zero, detecting hardcoded secrets/keys), you **MUST** abort the checkpoint protocol immediately, print the findings, and request the developer to resolve them (or mark false positives with `# epoch-secret-ignore`). Do **NOT** commit or push any changes.
- Run the project's native build, lint, and test commands to ensure the codebase is clean before closing. (e.g., `make test`, `npm test`, `pytest`, or `cargo test` depending on the tech stack).
- If any tests or compiler checks fail, attempt to fix the issues or notify the user and ask if they still want to commit.

## 5. Source Control Checkpoint (Optional)
- Check if the workspace is initialized as a git repository (e.g., verify if a `.git` directory exists or run `git rev-parse --is-inside-work-tree`).
- If it **is** a git repository:
  - Stage all changes using `git add .` and attempt to commit them with a clear, descriptive message: `git commit -m "chore(checkpoint): <brief summary of work>"`
  - If the commit fails (e.g., due to missing git configuration, author details, or hooks), report the warning/error but **do not block the checkpoint**. Proceed with the wrap-up.
  - Do not push unless explicitly requested by the user.
- If it **is not** a git repository:
  - Skip git staging and committing. Ensure all local memory files in `.agents/memory/` are saved.

## 6. Session Wrap-Up
- Respond to the user with a concise summary of what was accomplished, the verification results, and confirm that the state is committed and the session is ready to be closed. Provide a brief preview of the "Session Focus" that was just established.

## 7. Context Window Reset Reminder
- In your final response, remind the developer about the **Context Window Reset Protocol**:
  - Suggest that if the milestone is fully complete, or if they notice the chat response times slowing down due to a long transcript, they can safely start a fresh chat session.
  - Advise them to begin the new session by simply asking the new agent to: `"Please read the memory files under .agents/memory/ to synchronize state and check current backlog priorities."`
