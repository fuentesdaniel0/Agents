# Project History & Milestone Timeline

This file captures the chronological history of milestones, architectural decisions, and tasks completed in the **Daniel A. Fuentes Interactive Resume & Analytics Dashboard** repository.

---

## 📅 Sprint Chronology

### Milestone 1: Baseline Architecture & Testing Suite
*   **Accomplishment**: Created the core React 19 + Vite 8 + TypeScript 6 Single Page Application (SPA).
*   **Data Structures**: Established `src/data/resumeData.ts` to strongly type professional records and technical schema.
*   **Analytics Engine**: Created `src/utils/resumeAnalyzer.ts` to calculate recruiter scan scores, metrics densities, unique action verbs, and linguistic heuristics.
*   **Test Suite**: Configured Vitest + JSDOM in `src/setupTests.ts` and created initial unit tests covering the parser math and page toggle selectors.

### Milestone 2: Deployment & Serverless Dockerization (Milestone A)
*   **Accomplishment**: Configured a containerized production pipeline for serverless scale.
*   **Containerization**: Engineered a multi-stage [Dockerfile](file:///home/daniel/Dev/antigravity-test/Dockerfile):
    - *Stage 1 (Build)*: Uses `node:20-alpine` for secure dependency installation (`npm ci`) and compiler bundler runs (`npm run build`).
    - *Stage 2 (Serve)*: Uses `nginx:alpine` to host static assets (`dist/`) on port `8080`.
*   **Server Config**: Created [nginx.conf](file:///home/daniel/Dev/antigravity-test/nginx.conf) to manage port `8080` listeners, SPA client routing fallbacks (`try_files`), gzip text compression optimizations, and one-year cache controls for static resources.
*   **CI/CD Configurations**: Created [cloudbuild.yaml](file:///home/daniel/Dev/antigravity-test/cloudbuild.yaml) to compile, tag (`$COMMIT_SHA` & `latest`), and upload container images to Google Container Registry (GCR) before deploying serverless revisions onto Google Cloud Run in the `us-central1` region with unauthenticated access.

### Milestone 3: Interactive Features & Security Gating (Milestone B)
*   **Accomplishment**: Enhanced recruiter workflows and gated confidential analytics:
*   **Secure Analytics Gateway**:
    - Gated the "Resume Analytics" tab behind a glassmorphic password overlay.
    - Uses the browser's native Web Crypto API (`SHA-256`) to hash entries and verify them against the target hash: `dd28983000ecc2945137788ee290d2f18cb12c0ef9e7d9b5999ac6dcbd874ed4` (corresponding to the passcode `"daniel2026"`).
    - Prevents plain-text passcode exposure in client-side bundles and maintains login states across tab lifetimes via `sessionStorage`.
*   **Print-to-PDF Formatting**:
    - Embedded a "Print Resume" utility.
    - Integrated `@media print` rules in `src/App.css` to hide headers, glows, tabs, utility bars, maps, and footers, re-formatting the interactive CV page into a clean, standard 1-page paper-ready layout.
*   **Direct PDF Download**: Copied the pre-compiled professional resume PDF to [public/Daniel_Fuentes_Resume.pdf](file:///home/daniel/Dev/antigravity-test/public/Daniel_Fuentes_Resume.pdf), making it immediately downloadable.
*   **Interactive Career SVG Map**:
    - Built a horizontal, responsive SVG roadmap trace mapping Daniel's pivots (Houston ➔ Austin, SWE Intern ➔ Solutions ➔ Customer Engineer).
    - Connected nodes with active hovers to highlight corresponding job blocks in the main CV list and smooth-scroll the view directly on node clicks.

### Milestone 4: Polish, SEO & OpenGraph Preview (Milestone C)
*   **Accomplishment**: Optimized search engine footprints and social card previews.
*   **Metadata SEO Injections**: Standardized `index.html` headers with unique page titles, authors, semantic descriptions, and keyword index targets.
*   **Social Preview Cards**: Configured OpenGraph (`og:title`, `og:image`, `og:description`) and Twitter Cards.
*   **OpenGraph Asset Generation**: Generated a dark-neon, glassmorphic 1200x630px social card preview [opengraph_preview.png](file:///home/daniel/Dev/antigravity-test/public/opengraph_preview.png) highlighting React, GCP, and Docker credentials.

### Milestone 5: Application Decoupling & Workspaces Monorepo
*   **Accomplishment**: Decoupled the public-facing Interactive Resume from the private, secure Resume Analytics Dashboard.
*   **Monorepo Restructuring**: Restructured the single-app repository into an npm workspaces monorepo containing:
    - `packages/shared`: For shared data structures and analytics parser logic.
    - `apps/portfolio`: Genuooled static portfolio build completely omitting all passcode and analytics scripts.
    - `apps/analytics`: Separate app holding only the passcode gate and analytics dashboards.
*   **Test Suite Decoupling**: Disintegrated the central `vitest.workspace.ts` configuration, enabling each workspace to execute completely isolated tests sequentially or independently.
*   **Local Session Checkpoint SOP**: Introduced a highly automated checkpoint and wrap-up agent skill triggerable via `"let's checkpoint"`.

### Aesthetic & Accessibility Revisions (Completed)
*   **Accomplishment**: Enhanced website aesthetics, contrast compliance, and responsive alignments.
*   **Design Polish**:
    - Left-justified all bullet points across professional roles and custom projects.
    - Added bottom margin separations between cv sections, maximizing page breathing room.
    - Streamlined resume actions by removing the redundant actions bar and relocating the "Download PDF" action directly into the header contact grid for a cleaner layout.
    - Corrected the GitHub username to `fuentesdaniel0` in the shared database schema and application headers.
*   **Accessibility & Responsiveness**:
    - Fixed high-contrast soft grey variables under light/dark preferences, satisfying WCAG AA rules.
    - Scaled header typography fluidly using CSS `clamp()` and integrated clean stacking grid layouts for mobile/tablet screen widths.

### Cloud Run Custom Domain Alignment (Completed)
*   **Accomplishment**: Prepared the decoupled monorepo codebase for containerized serverless scale and mapped out custom domain routing.
*   **Monorepo Docker Alignment**: Adjusted the root `Dockerfile` to target `/app/apps/portfolio/dist` under Nginx, restoring compilation continuity for the decoupled public resume site.
*   **Domain Configuration Map**: Documented actionable CLI domain-mapping commands and exact DNS mapping matrices (A, AAAA, CNAME records) to securely map `fuentesdaniel.com` and its `www` subdomain to the regional Cloud Run service instance.

### CI/CD Pipeline IAM Hardening (Completed — 2026-05-30)
*   **Accomplishment**: Diagnosed and resolved two cascading `PERMISSION_DENIED` errors blocking the end-to-end GitHub Actions → Cloud Build → Cloud Run deployment pipeline.
*   **Root Cause Analysis**:
    - Cloud Build executes Step #3 (`gcloud run deploy`) as the **default Compute Engine SA** (`849688752380-compute@developer.gserviceaccount.com`), not as the GitHub Actions service account.
    - The compute SA was missing two critical IAM permissions.
*   **Fix 1 — `run.services.get` denied**: Granted `roles/run.admin` to the Cloud Build compute SA at the project level, enabling it to create and update Cloud Run services.
*   **Fix 2 — `iam.serviceaccounts.actAs` denied**: Granted `roles/iam.serviceAccountUser` on the compute SA to itself, allowing Cloud Run to assign that SA as the runtime identity for new service revisions.
*   **Result**: Full end-to-end pipeline now succeeds: GitHub Actions → Cloud Build (docker build + push) → `gcloud run deploy` → live Cloud Run revision.

### Milestone 6: Floating Top Navigation & Interactive Scrolled Name Header (Completed — 2026-05-30)
*   **Accomplishment**: Redesigned portfolio layout for perfect visual symmetry, created a sticky top docked navbar, and added fluid scroll-reveal animations.
*   **Top Docked Status Header**: Converted the floating navbar into an ultra-premium top docked header (`top-navbar` at `top: 0` with flat top corners and rounded bottom corners) to prevent scroll text bleed while keeping glassmorphic design and subtle slide-up hovers for contact icons.
*   **Dynamic Name-Reveal Scroll Observer**: Added a highly optimized `IntersectionObserver` in React (`App.tsx`) with a `-65px` rootMargin offset to dynamically slide-in and fade-in the user's name and title in the navigation bar the exact moment they scroll under it.
*   **Visual Layout Symmetry**: Relocated the profile header containing name and role to a centered position right above the main columns, vertically aligning both CV columns (Experience and Skills) at the exact same coordinate for optimal balance.


