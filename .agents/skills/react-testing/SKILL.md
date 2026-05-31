---
name: react-testing
description: Generates and modifies unit tests for React components using Vitest and React Testing Library conventions. Use whenever writing or modifying tests for the frontend apps or packages.
---

# React Testing Conventions

When writing tests in this monorepo, follow these steps and guidelines:

## Core Libraries
- Use `vitest` as the primary test runner.
- Use `@testing-library/react` for component rendering, querying, and interaction.
- Use `@testing-library/user-event` for simulating realistic user actions.
- Use `@testing-library/jest-dom` for robust DOM assertions.

## Checklist & Best Practices
1. **File Placement**: Test files should be named `[name].test.tsx` or `[name].test.ts` and placed in the same directory as the module they test.
2. **Test Structure**: Use `describe` blocks to group related tests, and `it` or `test` for individual test cases.
3. **Querying**: Prioritize queries accessible to all users (e.g., `getByRole`, `getByText`) over implementation-specific queries (e.g., `getByTestId`).
4. **Assertions**: Use `expect(element).toBeInTheDocument()` and similar DOM-specific matchers.
5. **Events**: Always prefer `userEvent.setup()` and its methods over `fireEvent` to accurately simulate user behavior in the browser.

## How to use it
When asked to write a test, first analyze the component's props and interactive elements. Then construct test cases covering default rendering, user interactions, and edge cases utilizing the libraries above.
