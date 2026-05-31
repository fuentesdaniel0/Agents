# Initialize Workspace

This workflow sets up the workspace environment for development.

1. Run `npm install` to install all dependencies across the monorepo workspaces.
2. Check if `.env.development` or `.env.test` exist. If not, recommend copying from `.env.example`.
3. Inform the user that they can start the dev servers using `npm run dev:portfolio` or `npm run dev:analytics`.
