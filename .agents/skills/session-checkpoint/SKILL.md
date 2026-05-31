---
name: session-checkpoint
description: Executes the project checkpoint protocol to wrap up a session. Trigger this skill whenever the user says "let's checkpoint" or asks to close the session.
---

# Session Checkpoint Protocol

When the user gives the instruction "let's checkpoint" or asks to prepare to close the session, you must execute the following protocol in exactly this order:

## 1. Status Check
- Run `git status` to see what files have been modified or created during the session.
- Review your recent tool calls and actions to summarize what you accomplished.

## 2. Memory & Tracker Updates
- Update `project_tracking/memory/current.md` to reflect any new architectural changes, active state, or newly established patterns.
- Append a summary of the session's completed tasks and milestones to `project_tracking/memory/history.md`.
- Update `project_tracking/memory/future.md` to remove completed items and add any newly identified next steps or future milestones.

## 3. Verification
- Run the project's verification commands to ensure the codebase is clean before closing:
  - Run `npm run build --workspaces --if-present`
  - Run `npm run lint --workspaces --if-present`
  - Run `npm run test:run --workspaces --if-present`
- If any commands fail, attempt to fix the issues, or notify the user and ask if they still want to commit.

## 4. Source Control Checkpoint
- Check if the workspace is initialized as a git repository by executing `git rev-parse --is-inside-work-tree` or verifying if a `.git` directory exists.
- If it **is** a git repository:
  - Stage all changes using `git add .`.
  - Commit the changes with a clear, descriptive message summarizing the session's work: `git commit -m "chore(checkpoint): <brief summary of work>"`
  - Do not push unless explicitly requested by the user.
- If it **is not** a git repository:
  - Skip git staging and committing.
  - Advise the user that the workspace is not currently a git repository, and suggest initiating one (`git init`) if they wish to establish version-controlled session states.

## 5. Session Wrap-Up
- Respond to the user with a concise summary of what was accomplished, the verification results, and confirm that the state is committed and the session is ready to be closed. Provide a brief preview of what the next steps are for the next session.
