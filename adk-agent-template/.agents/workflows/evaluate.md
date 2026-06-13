---
name: evaluate
description: Trigger the Vertex AI Gen AI evaluation pipeline on-demand, parse the results, and present a structured scorecard. Trigger this via `/evaluate`.
---

# Agent Evaluation Workflow

This workflow executes the automated evaluation pipeline to test the agent's goal completion, protocol adherence, and safety across various test scenarios, presenting a detailed scorecard of the results.

When the user triggers the `/evaluate` command, execute the following steps:

## 1. Environment Verification
- Check if the `GOOGLE_CLOUD_PROJECT` environment variable is defined.
- If it is not defined:
  - Explain to the user that Vertex AI Gen AI Evaluation requires Google Cloud access.
  - Prompt the user to provide their GCP Project ID or run the command manually after setting the environment variable:
    ```bash
    export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    ```
  - Halt the workflow and wait for the user to provide the project ID or configure the environment.

## 2. Execute Evaluation Pipeline
- Run the evaluation check command in the terminal:
  ```bash
  python3 adk-agent-template/evaluation/ci_eval_check.py
  ```
  *(Note: This command runs the evaluation runner `run_eval.py` internally, outputs results to `adk-agent-template/evaluation/eval_results.json`, and verifies the threshold).*
- Monitor the execution of the command. If the script fails due to authentication or missing packages, report the error details to the user and ask for assistance.

## 3. Parse and Format Results
- Read the generated results file at `adk-agent-template/evaluation/eval_results.json`.
- Parse the JSON array of scenario results. For each scenario:
  - Parse the `prompt`.
  - Parse the `reference` (ground truth).
  - Parse the `response` (agent response).
  - Parse the score from the key `epoch_agent_protocol_metric/score`.
  - Parse the explanation from the key `epoch_agent_protocol_metric/explanation`.
- Compute the overall mean score of the scenarios.

## 4. Scorecard Presentation
- Present a structured scorecard to the user containing:
  - **Overall Status**: **PASS** (Mean Score >= 4.0) or **FAIL** (Mean Score < 4.0).
  - **Summary Statistics**: The mean score and total scenarios evaluated.
  - **Scenario Breakdown**: A detailed table or collapsible sections (using HTML `<details>` and `<summary>`) for each scenario showing:
    - **Prompt**
    - **Score** (highlighted with visual indicators, e.g. 🟢 for 4-5, 🟡 for 3, 🔴 for 1-2)
    - **Explanation / Rationale** behind the score.
- If any scenario scored below 4.0, highlight it as a recommendation for improvement and ask the user if they would like to address it.
