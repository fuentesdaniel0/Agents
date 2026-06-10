import os
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
import uvicorn

# Define the base directory for Epoch memory
MEMORY_DIR = os.environ.get("EPOCH_MEMORY_DIR", ".agents/memory")

def get_memory_path(file_name: str) -> str:
    """Helper to resolve the absolute path to memory files."""
    if file_name not in ["context.md", "backlog.md", "changelog.md"]:
        raise ValueError("Invalid memory file name. Must be context.md, backlog.md, or changelog.md")
    return os.path.join(MEMORY_DIR, file_name)

# Define native tools for Epoch state synchronization
def _read_epoch_memory(file_name: str) -> str:
    path = get_memory_path(file_name)
    if not os.path.exists(path):
        return f"Error: Memory file {file_name} does not exist at {path}."
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_name}: {str(e)}"

def _update_epoch_memory(file_name: str, content: str) -> str:
    path = get_memory_path(file_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully updated {file_name}."
    except Exception as e:
        return f"Error updating file {file_name}: {str(e)}"

def read_context() -> str:
    """Reads the contents of context.md to synchronize current project context and architecture state."""
    return _read_epoch_memory("context.md")

def read_backlog() -> str:
    """Reads the contents of backlog.md to synchronize the product backlog and session focus."""
    return _read_epoch_memory("backlog.md")

def read_changelog() -> str:
    """Reads the contents of changelog.md to synchronize completed sprints and decisions."""
    return _read_epoch_memory("changelog.md")

def update_context(content: str) -> str:
    """Overwrites or updates context.md to persist current project context and architecture changes."""
    return _update_epoch_memory("context.md", content)

def update_backlog(content: str) -> str:
    """Overwrites or updates backlog.md to persist session focus and active tasks."""
    return _update_epoch_memory("backlog.md", content)

def update_changelog(content: str) -> str:
    """Overwrites or updates changelog.md to persist completed sprints and decisions."""
    return _update_epoch_memory("changelog.md", content)

from functools import cached_property
from google.adk.models import Gemini
from google.genai import Client

# Custom model class to override underlying Client for Vertex AI & ADC support
class VertexGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if project:
            # Force Vertex AI backend using the Cloud Run environment PROJECT ID
            return Client(vertexai=True, project=project, location="us-central1")
        # Local fallback using standard Gemini Client (requires GEMINI_API_KEY)
        return Client()

# Create the Epoch ADK Agent using the custom model definition
epoch_agent = Agent(
    name="epoch_context_agent",
    model=VertexGemini(model="gemini-2.5-pro"),
    description="An AI agent with persistent, stateful memory synchronized via the Epoch protocol.",
    instruction=(
        "You are an AI agent operating with persistent memory tracked in .agents/memory/.\n"
        "At the start of any task, use the `read_context` and `read_backlog` tools to read context.md and backlog.md.\n"
        "Align your actions with the Session Focus and Active Backlog Tasks.\n"
        "When you complete a task, update context.md (if architecture/patterns changed) using `update_context`, "
        "move completed tasks to changelog.md using `update_changelog`, and update backlog.md using the `update_backlog` tool."
    ),
    tools=[read_context, read_backlog, read_changelog, update_context, update_backlog, update_changelog]
)

# Initialize standard ADK runner
runner = InMemoryRunner(agent=epoch_agent)
runner.auto_create_session = True

# Initialize FastAPI App
app = FastAPI(title="Epoch ADK Agent Service")

class RunRequest(BaseModel):
    prompt: str

class RunResponse(BaseModel):
    response: str

@app.get("/")
def health_check():
    """Returns the agent health and name."""
    return {
        "status": "healthy",
        "agent": epoch_agent.name,
        "description": epoch_agent.description
    }

@app.post("/run", response_model=RunResponse)
def run_agent(request: RunRequest):
    """Runs the agent with the user-provided prompt."""
    try:
        # Construct GenAI Content message
        message = types.Content(
            role="user",
            parts=[types.Part(text=request.prompt)]
        )

        # Run the agent through ADK Runner
        events = runner.run(
            user_id="default_user",
            session_id="default_session",
            new_message=message
        )

                # Extract text response from generated events
        response_text = ""
        for event in events:
            print(f"DEBUG Event: {event.model_dump_json(exclude_none=True)}")
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text

        return RunResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
