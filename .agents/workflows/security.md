---
name: security-check
description: Run the local security scanner to inspect the codebase for hardcoded secrets, credentials, or keys on-demand. Trigger this via `/security`.
---

# Security Check Workflow

This workflow executes the local security scanner to scan the workspace for exposed API keys, private keys, tokens, or credentials. It reports any findings to the user and blocks until resolved.

When the user triggers the `/security` command, execute the following steps:

## 1. Run Security Scanner
- Run the local security check command in the terminal:
  ```bash
  python3 .agents/scripts/security-check.py
  ```
- Capture the stdout, stderr, and exit code of the execution.

## 2. Parse and Analyze Findings
- **If the script exits with code 0**:
  - Report a success message to the user: "🟢 **SUCCESS**: Security check completed. No secrets or credentials detected."
- **If the script exits with code 1**:
  - Report a warning message to the user: "🔴 **WARNING**: Hardcoded secrets or credentials detected in the codebase."
  - Parse the output and present the findings structured by file and line number:
    - **File Name & Line Number** (with a clickable link, e.g., `[filename.py:L45](file:///path/to/filename.py#L45)`)
    - **Type of Secret** (e.g., Google API Key, Private Key Block, etc.)
    - **Masked Secret** value
    - **Line Context**
  - **Resolution Guidance**:
    - Remind the developer that these credentials must be removed before staging/committing.
    - If a finding is a false positive (such as test keys, dummy credentials, or documentation placeholders), instruct the user that they can suppress the warning by adding `# epoch-secret-ignore` as an inline comment at the end of the flagged line.
    - Suggest running `/security` again after updating the files to verify the fix.
