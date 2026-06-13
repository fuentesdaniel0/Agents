---
name: milestone-review
description: Interactive workflow to review milestones, select an active milestone, and populate the session focus from the backlog. Trigger this via `/milestones` or `/review-milestones`.
---

# Milestone Review Workflow

This workflow allows the user and the agent to review high-level project milestones, update their progress, select the active milestone to focus on, and automatically populate the session focus and active backlog tasks.

When the user triggers the `/milestones` or `/review-milestones` command, execute the following steps:

## 1. Backlog Analysis
- Read `.agents/memory/backlog.md`.
- Parse the milestones under the `## High-Level Roadmap` header.
- For each milestone, identify:
  - The milestone title (e.g. `Milestone 1: Template Separation`).
  - Its completion status (e.g. if marked as `Completed`, or if all features listed under it are checked/completed).
  - Its individual features/tasks list.

## 2. Interactive Presentation
- Present a concise, structured list of the parsed milestones to the user.
- Group the milestones into:
  - **Completed Milestones**: Briefly list them.
  - **Active Milestone**: The milestone currently identified in the `Session Focus` or the first incomplete milestone. Show its features and their individual completion status (checked/unchecked).
  - **Upcoming Milestones**: List subsequent incomplete milestones and their features.
- Ask the user:
  1. *"Which milestone should we focus on as the active milestone for this session?"*
  2. *"Are there any status updates (marking features complete, adding/removing tasks) we need to make to the roadmap?"*

*Wait for the user's response before proceeding.*

## 3. Queue Grooming & State Update
- Update `.agents/memory/backlog.md` based on the user's input:
  - If the user selected a new active milestone:
    - Update the **Session Focus** at the top of `.agents/memory/backlog.md` to target the selected milestone and summarize its immediate next steps.
    - Extract all incomplete features/tasks from the selected milestone.
    - Decompose those features into atomic, verifiable subtasks (if they are high-level) and populate them in the **Active Backlog Tasks** list.
  - If the user provided status updates for other milestones:
    - Mark those features/tasks as completed (e.g., using `[x]`) or update the titles (e.g., adding `(Completed)` to the milestone header if all its tasks are done).
- Save the updated `.agents/memory/backlog.md` file.

## 4. Summary & Confirmation
- Present a summary of the changes made to `.agents/memory/backlog.md`:
  - Show the updated **Session Focus**.
  - Show the list of **Active Backlog Tasks** populated for the session.
- Ask the user: *"Are we ready to begin work on the first task in the queue, or do we need to refine the tasks further?"*
