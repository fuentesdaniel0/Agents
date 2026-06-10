---
trigger: always_on
---

# Core Agentic Directives

When operating within this repository, all AI agents must adhere to these foundational behaviors regardless of the active tech stack:

## 1. Active Exploration
- **Do not guess file structures or hallucinate paths.** Always use `list_dir` or `grep_search` to actively locate the correct modules and configuration files before executing modifications.
- **Context Minimization**: Only use `view_file` on files directly relevant to your immediate subtask to preserve token efficiency.

## 2. Verification-First Development
- **Continuous Validation**: Do not wait for the final `/checkpoint` workflow to verify your code. Run the appropriate build commands, type checkers (e.g., `npx tsc`), or test suites immediately after completing a logical chunk of work.
- **Proof of Success**: Provide the developer with concrete proof (e.g., test output logs or build success messages) before declaring a task completed.

## 3. Atomic Decompositions
- Never attempt to implement large, complex features in a single monolithic edit. Break problems down into small, verifiable steps.
