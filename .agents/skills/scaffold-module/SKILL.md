---
name: scaffold-module
description: A generic script for generating boilerplate and folder structures for a new module or feature. Trigger this when asked to create a new module, feature, or component.
---

# Scaffold Module Workflow

When the user requests to create a new module, component, or feature, execute the following steps:

## 1. Requirement Gathering
- Determine the name of the new module and its primary responsibility.
- Clarify if there are any specific design patterns (e.g., MVC, Repository Pattern, Atomic Design) that the module must adhere to.

## 2. Directory Creation
- Use `run_command` (e.g., `mkdir -p path/to/module`) to create the necessary directory structure. A standard module might require:
  - `src/modules/<module-name>/`
  - `src/modules/<module-name>/__tests__/`

## 3. Boilerplate Generation
- Create the core files with foundational boilerplate code (e.g., interfaces, classes, or base components).
- Create an empty test file in the `__tests__` directory.
- Update the necessary routing, indexing, or global registration files to expose the new module.

## 4. Documentation & Verification
- Update `.agents/memory/context.md` to reflect the newly created module in the Architecture / Code Graph section.
- Compile or lint the newly created files to ensure they are structurally sound.
- Confirm with the user that the module has been scaffolded and is ready for detailed implementation.
