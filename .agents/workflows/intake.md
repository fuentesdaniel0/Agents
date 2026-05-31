---
name: project-intake
description: Interactive workflow to define a new project's scope, tech stack, and initial milestones. Trigger this via `/intake` when starting a brand new project.
---

# Project Intake Workflow

When the user triggers the `/intake` command or asks to set up a new project, execute the following steps interactively:

## 1. Project Discovery Interview
Ask the user the following questions (you can group them or ask conversationally, but ensure you get answers for all):
- **Project Name & Core Goal**: What is the name of this project and its primary objective?
- **Tech Stack**: What programming languages, frameworks, or tools will we be using?
- **Initial Milestones**: What are the first 1-3 major milestones or features we need to build?
- **Constraints**: Are there any specific architectural constraints, testing requirements, deployment targets, or security considerations?

*Wait for the user's responses before proceeding to Step 2.*

## 2. Memory Initialization
Once the user provides the details, synthesize the information and update the project tracking templates:
- **`project_tracking/memory/current.md`**: Fill out the "Active Stack Details" and basic "Architecture" sections based on the provided tech stack and constraints.
- **`project_tracking/memory/future.md`**: Populate the "High-Level Roadmap" and "Active Backlog Tasks" with the initial milestones discussed.
- **`project_tracking/memory/history.md`**: Add an entry for "Milestone 0: Project Discovery & Intake" summarizing the established goals.

## 3. Confirmation & Handoff
Present a brief summary of the initialized project state to the user. Confirm that the memory tracking system is now fully tailored to their new project and ready for development. Suggest they provide their first engineering task to get started!
