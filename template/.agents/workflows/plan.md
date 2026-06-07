---
name: project-planning
description: Interactive workflow to define a new project or plan the next sprint by reviewing the backlog and migrating tasks. Trigger this via `/plan` or `/sprint`.
---

# Project Planning Workflow

When the user triggers the `/plan` or `/sprint` command, first determine if the project has been initialized by checking if `.agents/memory/context.md` is populated with a tech stack and architecture. 

Depending on the state, execute one of the following paths interactively:

## Path A: New Project Intake (If not initialized)

### 1. Project Discovery Interview
Ask the user the following questions (you can group them or ask conversationally, but ensure you get answers for all):
- **Project Name & Core Goal**: What is the name of this project and its primary objective?
- **Tech Stack**: What programming languages, frameworks, or tools will we be using?
- **Initial Milestones**: What are the first 1-3 major milestones or features we need to build?
- **Constraints**: Are there any specific architectural constraints, testing requirements, deployment targets, or security considerations?

*Wait for the user's responses before proceeding to Step 2.*

### 2. Memory Initialization
Once the user provides the details, synthesize the information and update the project tracking templates:
- **`.agents/memory/context.md`**: Fill out the "Active Stack Details" and basic "Architecture" sections based on the provided tech stack and constraints.
- **`.agents/memory/backlog.md`**: Populate the "High-Level Roadmap" and "Active Backlog Tasks" with the initial milestones discussed.
- **`.agents/memory/changelog.md`**: Add an entry for "Milestone 0: Project Discovery & Intake" summarizing the established goals.

### 3. Confirmation & Handoff
Present a brief summary of the initialized project state to the user. Confirm that the memory tracking system is now fully tailored to their new project and ready for development. Suggest they provide their first engineering task to get started!

---

## Path B: Sprint Planning (If already initialized)

### 1. Backlog Review
- Read `.agents/memory/backlog.md`.
- Present a concise summary of the "Session Focus" (if any) and the top items in the "High-Level Roadmap" to the user.
- Ask the user: *"Which of these roadmap items should we pull into the 'Active Backlog Tasks' for this session? Or is there a new priority not listed here?"*

*Wait for the user's response before proceeding.*

### 2. Queue Grooming & Task Decomposition
Based on the user's response:
- Analyze the selected Roadmap items. If they are large features, **decompose them into atomic, verifiable subtasks**.
- Update `.agents/memory/backlog.md`:
  - Move the selected items (and their subtasks) into the "Active Backlog Tasks".
  - Update the "Session Focus" section to reflect the immediate goal.
- Present the updated "Active Backlog Tasks" queue to the user for confirmation.

### 3. Execution Handoff
- Ask the user: *"Are we ready to begin work on the first task in the queue, or do we need to clarify any architectural details before starting?"*
- Once confirmed, transition smoothly into execution mode, focusing strictly on the first active task.
