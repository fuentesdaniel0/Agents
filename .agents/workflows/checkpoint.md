---
name: session-checkpoint
description: Interactive workflow to execute the project checkpoint protocol and wrap up a session. Trigger this via `/checkpoint`.
---

# Session Checkpoint Workflow

When the user triggers the `/checkpoint` command or asks to prepare to close the session, you must execute the following protocol in exactly this order:

## 1. Status Check
- Run `git status` to see what files have been modified or created during the session.
- Review your recent tool calls and actions to summarize what you accomplished.

## 2. Memory & Tracker Updates
- **Update Active State**: Update `.agents/memory/context.md` to reflect any new architectural changes, active state, or newly established patterns.
- **Task Migration**: Move completed tasks from `.agents/memory/backlog.md` (Active Backlog Tasks) into `.agents/memory/changelog.md`.
- **Chronological History**: Append a brief narrative summary of the session's completed milestones to `.agents/memory/changelog.md`.
- **Memory Rotation & Archiving**: Check the size of `.agents/memory/changelog.md`. If it is growing too long (e.g., tracking more than the last 3 major milestones), automatically move the oldest entries into an archive file (e.g., `.agents/memory/archive/changelog-v1.md`) to preserve context window tokens.

## 3. Next Session Planning
- Interactively ask the user: *"What should our primary focus be for the next session?"*
- Inject their response into the "Next Session Focus" section at the top of `.agents/memory/backlog.md`.

## 4. Verification
- Run the project's native build, lint, and test commands to ensure the codebase is clean before closing. (e.g., `make test`, `npm test`, `pytest`, or `cargo test` depending on the tech stack).
- If any commands fail, attempt to fix the issues, or notify the user and ask if they still want to commit.

## 5. Source Control Checkpoint
- Check if the workspace is initialized as a git repository by executing `git rev-parse --is-inside-work-tree` or verifying if a `.git` directory exists.
- If it **is** a git repository:
  - Stage all changes using `git add .`.
  - Commit the changes with a clear, descriptive message summarizing the session's work: `git commit -m "chore(checkpoint): <brief summary of work>"`
  - Do not push unless explicitly requested by the user.
- If it **is not** a git repository:
  - Skip git staging and committing.
  - Advise the user that the workspace is not currently a git repository, and suggest initiating one (`git init`) if they wish to establish version-controlled session states.

## 6. Session Wrap-Up
- Respond to the user with a concise summary of what was accomplished, the verification results, and confirm that the state is committed and the session is ready to be closed. Provide a brief preview of the "Next Session Focus" that was just established.

## 7. Context Window Reset Reminder
- In your final response, remind the developer about the **Context Window Reset Protocol**:
  - Suggest that if the milestone is fully complete, or if they notice the chat response times slowing down due to a long transcript, they can safely start a fresh chat session.
  - Advise them to begin the new session by simply asking the new agent to: `"Please read the memory files under .agents/memory/ to synchronize state and check current backlog priorities."`
