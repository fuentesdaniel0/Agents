# Future Backlog & Technical Roadmap

This file defines upcoming feature releases, pipeline integrations, and strategic milestones for the resume application.

---

## 🚀 Upcoming Milestones

### Milestone A: Deployment & Serverless CI/CD Gates ✅
*   ~~**Continuous Integration Gates**: Add pipeline workflows in `.github/workflows/ci.yml` to automatically trigger:
    `Checkout` ➔ `TSC Type Check` ➔ `Linting` ➔ `Vitest Suite` ➔ `Vite Build`
    on every pull request or commit to the `main` branch.~~
*   ~~**Live Cloud Run Deployments**: Connect Google Cloud Build triggers to your repository, allowing Cloud Run to automatically redeploy new revisions when commits are pushed.~~
*   **Status**: Fully operational. GitHub Actions triggers Cloud Build on push to `master`, which builds/pushes the Docker image and deploys to Cloud Run with proper IAM permissions.

### Milestone B: Telemetry & Recruiter Interaction Logs
*   **Interaction Telemetry**: Log click actions (Print triggers, Direct PDF downloads, and SVG milestone map hover nodes) to track recruiter engagement.
*   **Analytics Analytics**: Bind Google Analytics or local analytics APIs to track recruiter session times and screen widths.

### Milestone C: Interactive AI Career Coach (Premium Expansion)
*   **AI Coach Sidebar**: Build a custom glassmorphic conversational chat sidebar.
*   **System Prompts**: Utilize the elite Software Engineering career coach prompt configured in [career_coach_prompt.txt](file:///home/daniel/Dev/antigravity-test/project_tracking/career_coach_prompt.txt) to ground an LLM, allowing recruiters to ask questions about Daniel's career path, GCP projects, or technical proficiency.
*   **Semantic RAG Integration**: Retrieve relevant bullet points dynamically to back up the coach's answers with factual evidence from Daniel's resume dataset.

### Milestone D: Security Adaptations
- [x] **Passcode Customization**: Refactor passcode storage to fetch custom cryptographic validation targets from secure environment variables during compilation or runtime.
- [x] **JSON Config Gates**: Allow passcodes to be securely updated through developer console panels or encrypted configuration files (Using Vite's `.env` setup).

### Milestone E: Application Decoupling & Workspaces Monorepo
- [x] **Application Decoupling**: Fully decouple analytics gating/visuals from public portfolio resume views.
- [x] **Isolated Workspaces Test Suite**: Remove central workspaces configuration so that tests run independently per workspace.

---

## 🚀 Future Technical Backlog & Next Steps

### 1. Isolated Deployment Architectures
*   **Public Portfolio Website (Completed)**:
    *   Successfully built the portfolio monorepo workspace and deployed it to Google Cloud Run regional serverless service `resume-app` under the custom domain **`fooentes.org`** and **`www.fooentes.org`** with automatic SSL provisioning!
*   **Private Analytics Service**:
    *   Deploy `apps/analytics` using custom multi-stage Docker build to **Google Cloud Run** to keep dashboard servers dynamic and secure, protected by custom domain routing (e.g. `analytics.fooentes.org`).
*   **Decoupled Cloud Build Configurations**:
    *   Separate Cloud Build triggers so that a commit under `apps/portfolio/*` only builds and publishes the public portfolio, and a commit under `apps/analytics/*` triggers the analytics build.


### 2. Interaction Telemetry Sync
*   **Secure Webhook Logging**:
    *   Build a secure REST logging endpoint under Cloud Run that processes recruiter engagement telemetry (PDF print clicks, CV node navigation, session length) and stores it in Firestore.
    *   Connect the portfolio app to send events to this endpoint securely without exposing keys.

### 3. AI Career Coach Integration
*   **Retrieval Augmented Generation (RAG)**:
    *   Embed a custom glassmorphic conversational chat sidebar in the portfolio app that queries a Gemini model powered by a vector database of Daniel's structured project details and achievements.
    *   Provide inline reference citations to recruiters to verify facts against the public resume dataset.
