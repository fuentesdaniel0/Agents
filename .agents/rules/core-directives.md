---
trigger: always_on
---

# Core Agentic Directives

When operating within this repository, all AI agents must adhere to these foundational behaviors regardless of the active tech stack:

## 1. Active Exploration
- **Do not guess file structures or hallucinate paths.** Always use `list_dir` or `grep_search` to actively locate the correct modules and configuration files before executing modifications.
- **Context Minimization**: Only use `view_file` on files directly relevant to your immediate subtask to preserve token efficiency.

## 2. Verify-First Loop
- **Immediate Validation**: Run appropriate verification commands (compilers, linters, test suites) *immediately* after editing any file, before modifying other files or declaring a task complete.
- **Proof of Success**: Provide the developer with concrete proof (e.g., test output logs or build success messages) before declaring a task completed. If an edit breaks tests, resolve the failure (or revert) before proceeding.

## 3. Atomic Decompositions
- Never attempt to implement large, complex features in a single monolithic edit. Break problems down into small, verifiable steps.

## 4. Git De-coupling
- **No Git commands during development**: Do not run Git commands (such as `git add`, `git diff`, `git status`, or `git checkout`) during active coding and debugging. Git operations are handled exclusively at the end of a session by the `/checkpoint` workflow or by the user. Focus entirely on code changes and verification tools.


