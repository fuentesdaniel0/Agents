# Epoch ADK Agent Template

This template provides a base python implementation of an **Agent Development Kit (ADK)** agent integrated with the **Epoch Contextual Memory Protocol** and wrapped with **Agent-to-Agent (A2A)** capabilities. It is optimized for deployment to **Google Cloud Agent Engine** or **Cloud Run**.

## Features

- **Epoch Memory Integration**: Exposes tools to read and write Epoch's state tracking files (`context.md`, `backlog.md`, `changelog.md`).
- **Agent Factory Pattern**: Dynamically registers, configures, and instantiates ADK-compatible agents with selected tools via API endpoints.
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

### Agent Factory API Endpoints

The FastAPI server exposes endpoints to dynamically manage and run custom agents:

- **`POST /agents`**: Register a new agent configuration.
  ```json
  {
    "name": "custom_agent",
    "model": "gemini-2.5-flash",
    "description": "Dynamic custom agent",
    "instruction": "Answer questions briefly.",
    "tools": ["read_file"]
  }
  ```
- **`GET /agents`**: List all dynamically registered agent configurations.
- **`GET /agents/{name}`**: Retrieve configuration details for a specific agent.
- **`DELETE /agents/{name}`**: Delete a registered agent configuration.
- **`POST /run`**: Run a prompt. Optionally specify the dynamic `"agent"` name to execute that custom agent:
  ```json
  {
    "prompt": "Sync memory and list the backlog.",
    "agent": "custom_agent"
  }
  ```
- **`POST /agents/{name}/run`**: Directly run the named custom agent.


### 3. Folder Structure & Configuration

When deploying or running, the agent will look for the `.agents/memory` folder in its working directory. You can customize the folder path and agent metadata using the following environment variables:

| Environment Variable | Description | Default Value |
| :--- | :--- | :--- |
| `EPOCH_MEMORY_DIR` | Directory path containing context.md, backlog.md, and changelog.md. | `.agents/memory` |
| `AGENT_NAME` | The registry and display name of the agent. | `epoch_context_agent` |
| `AGENT_MODEL` | Gemini LLM model identifier. | `gemini-2.5-pro` |
| `AGENT_DESCRIPTION` | The purpose/description of the agent. | `An AI agent with persistent, stateful memory synchronized via the Epoch protocol.` |
| `LOCATION` / `GOOGLE_CLOUD_LOCATION` | Vertex AI client location/region. | `us-central1` |

Example of setting configuration variables:

```bash
export AGENT_NAME="custom_development_agent"
export AGENT_MODEL="gemini-2.5-flash"
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
