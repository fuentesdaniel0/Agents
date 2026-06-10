# Epoch ADK Agent Template

This template provides a base python implementation of an **Agent Development Kit (ADK)** agent integrated with the **Epoch Contextual Memory Protocol** and wrapped with **Agent-to-Agent (A2A)** capabilities. It is optimized for deployment to **Google Cloud Agent Engine** or **Cloud Run**.

## Features

- **Epoch Memory Integration**: Exposes tools to read and write Epoch's state tracking files (`context.md`, `backlog.md`, `changelog.md`).
- **A2A Support**: Exposes the agent as an A2A-compliant service using ADK's `to_a2a()` helper, serving an automatic **Agent Card** at `/.well-known/agent-card.json`.
- **Docker Ready**: Includes a production-ready `Dockerfile` for easy deployment to containerized environments.

---

## Getting Started

### 1. Installation

Install the required python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Local Execution

Run the uvicorn ASGI server:

```bash
python main.py
```

By default, the server runs on `http://0.0.0.0:8080`.
You can access the auto-generated A2A Agent Card by visiting:
```
http://localhost:8080/.well-known/agent-card.json
```

### 3. Folder Structure

When deploying or running, the agent will look for the `.agents/memory` folder in its working directory. You can customize this by setting the `EPOCH_MEMORY_DIR` environment variable:

```bash
export EPOCH_MEMORY_DIR="/path/to/your/project/.agents/memory"
```

---

## Deployment

### 1. Local Deployment (FastAPI Dev Server)
For local development, you can run the agent locally and verify its endpoints:
```bash
# Set your active GCP project ID and your Epoch memory directory path
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export EPOCH_MEMORY_DIR="/path/to/your/project/.agents/memory"

# Run the FastAPI server
python main.py
```

### 2. Deploying to Cloud Run (Single-Command Source Deploy)
To build and deploy the containerized agent directly from source to Cloud Run, run:

```bash
gcloud run deploy epoch-adk-agent \
    --source . \
    --platform managed \
    --no-allow-unauthenticated \
    --port 8080
```
*(Note: If prompted to create an Artifact Registry repository for source deploy, select **yes**).*

### Mounting Persistent Volume (Optional)
Since Epoch is a file-based memory system, if you want your agent to modify the code repository's memory files permanently in production, you should mount a persistent storage volume (like Cloud Storage FUSE) to the `/app/.agents/memory` directory or use an API-driven memory integration.
