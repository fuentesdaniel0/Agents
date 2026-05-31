# Developer-Agent Synchronization Protocol

This document establishes the Standard Operating Procedures (SOP) for maintaining repository-based project memory. By adhering to this protocol, any future AI agent can instantly synchronize with the current codebase, allowing developers to reset chat contexts periodically to optimize token utilization and maximize processing performance.

---

## 🔁 The Synchronization Loop

```
  [ New Agent Session Starts ]
               │
               ▼
   Read project_tracking/memory/ (current.md, history.md, future.md)
               │
               ▼
   [ Execute Engineering Work & Sprint Checklist ]
               │
               ▼
   Run Verifications (Tests, Linters, TSC, Vite Builds)
               │
               ▼
   Update project_tracking/memory/ with Fresh State
               │
               ▼
  [ Recommend Context Reset to Developer ]
```

---

## 📋 1. Startup Standard Operating Procedure (SOP)
Whenever a new AI agent initializes in this repository, it **MUST** perform the following tasks before proposing any changes:
1.  **Read Active State ONLY**: Load `project_tracking/memory/current.md` to synchronize with active frameworks, ports, credential passcode hashes, and verification guidelines.
2.  **Lazy Load Context**: Do NOT automatically read `history.md` or `future.md`. Only load these files if the developer's request explicitly requires knowledge of past sprints or the future backlog.
3.  **Agentic Exploration**: Use `grep_search`, `list_dir`, and other tools to actively discover where code lives rather than relying on assumed knowledge or monolithic context files.
4.  **Confirm Alignment**: Present a brief, concise alignment summary to the user before starting work.

---

## 📋 2. Checkpoint & Sprint Wrap-Up SOP
Before closing out a major milestone or completing a work session, the agent **MUST** synchronize state to the repository. *Note: Do not run heavy production builds on every minor code change. Reserve this for the checkpoint.*
1.  **Run Code Verification**: Validate standard type consistency (`npx tsc --noEmit`), code styles (`npm run lint`), and ensure tests are 100% green (`npm run test:run`).
2.  **Run Compilation Checks**: Verify standard builds succeed via `npm run build` ONLY at the end of the sprint.
3.  **Update Memory Files**: Modulate `current.md`, `history.md`, and `future.md` to reflect newly completed features, security variables, and revised roadmap goals.
4.  **Version Control & Branching**: Advise the developer to commit these changes to a **feature branch** (e.g., `feature/new-analytics-ui`) rather than `main`. This prevents triggering heavy CI/CD pipelines on every small commit and keeps your development loop blazing fast. Only merge to `main` when the milestone is fully complete.

---

## 🗑️ 3. Context Window Reset Protocol

> [!IMPORTANT]
> **Token & Latency Optimizations**:
> Because the absolute state is fully preserved within the repository markdown memory files, **AI agents are completely stateless**. Long chat transcripts build up token volume, slowing down response times and increasing resource overhead.
> 
> **When to Reset**:
> - Whenever a sprint milestone is fully verified, completed, and synced to `project_tracking/memory/`.
> - If you notice latency or sluggish responses during your chat session.
> 
> **How to Reset**:
> 1. Complete the Turn Wrap-Up SOP (ensuring memory files are completely updated).
> 2. Create a **fresh, clean chat session** in your Antigravity IDE.
> 3. Start the session by simply asking the agent to: `"Please read the memory files under project_tracking/memory/ to synchronize state and check current backlog priorities."`
> 4. The incoming agent will instantly parse the files, restore full context, and align with your project goals in seconds, with a completely clean context window!

---

## 🤖 4. Agentic Execution Best Practices

To maximize the effectiveness of AI agents within this repository, adhere to the following execution principles:

1. **Verification-First Development**:
   - **Self-Correction**: Agents MUST run the appropriate testing (`npm run test:run`) and linting (`npm run lint`) suites after modifying code. Do not wait for the developer to ask.
   - **Rely on the Compiler**: Trust TypeScript (`npx tsc --noEmit`) to catch type errors immediately.

2. **Decompose Problems**:
   - **Atomic Tasks**: Break down complex features into smaller, verifiable units (e.g., build the shared data structure first, verify it, then build the UI).
   - **Modular Isolation**: Keep changes scoped to specific modules (`@antigravity/shared`, `@antigravity/portfolio`) to prevent unintended side effects.

3. **Strict "Definition of Done"**:
   - Do not consider a task complete until it passes compilation, linting, and tests.
   - Provide concrete proof (e.g., test output logs) to the developer before calling a task "done".

4. **Framework Alignment**:
   - Adhere to the established patterns in the repository (React 19, Vite 8, TypeScript). Do not introduce bespoke or non-standard architectural patterns unless explicitly requested.
