import os
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
import uvicorn

from tools import (
    MEMORY_DIR,
    get_memory_path,
    read_context,
    read_backlog,
    read_changelog,
    update_context,
    update_backlog,
    update_changelog,
    read_file,
    write_file,
    list_project_files,
    run_verification_command
)
from registry import AgentRegistry, AgentConfig
from factory import AgentFactory

REGISTRY_FILE = os.path.join(MEMORY_DIR, "agents_registry.json")
registry = AgentRegistry(REGISTRY_FILE)

from functools import cached_property
from google.adk.models import Gemini
from google.genai import Client

# Custom model class to override underlying Client for Vertex AI & ADC support
class VertexGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("LOCATION", "us-central1")
        if project:
            # Force Vertex AI backend using the Cloud Run environment PROJECT ID and configured location
            return Client(vertexai=True, project=project, location=location)
        # Local fallback using standard Gemini Client (requires GEMINI_API_KEY)
        return Client()

# Get agent configuration from environment variables with defaults
AGENT_NAME = os.environ.get("AGENT_NAME", "epoch_context_agent")
AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-2.5-pro")
AGENT_DESCRIPTION = os.environ.get("AGENT_DESCRIPTION", "An AI agent with persistent, stateful memory synchronized via the Epoch protocol.")

# Create the Epoch ADK Agent using the custom model definition
epoch_agent = Agent(
    name=AGENT_NAME,
    model=VertexGemini(model=AGENT_MODEL),
    description=AGENT_DESCRIPTION,
    instruction=(
        "You are an AI agent operating with persistent memory tracked in .agents/memory/.\n"
        "At the start of any task, you MUST use `read_context` and `read_backlog` to synchronize current state.\n"
        "Align all actions with the Session Focus and Active Backlog Tasks.\n\n"
        "Follow these strict operational rules:\n"
        "1. Active Exploration: Before reading or writing any files, you MUST use `list_project_files` to verify the codebase layout. You MUST explicitly confirm in your final response that you verified the workspace layout (by listing files) before editing.\n"
        "2. Verification-First: Immediately after writing or modifying any file, you MUST run a verification command (using `run_verification_command`, e.g., 'python3 -m unittest' or 'python3 <filename>') to verify correctness before proceeding. You MUST explicitly confirm in your final response that the code has been successfully verified (including the command run).\n"
        "3. Session Commit: When a task is complete, update `context.md` (via `update_context`), move completed tasks to `changelog.md` (via `update_changelog`), and update `backlog.md` (via `update_backlog`).\n\n"
        "If you receive a slash command in the prompt:\n"
        "- `/plan`: Review the backlog and propose updates to the session focus and active tasks.\n"
        "- `/checkpoint`: Execute the wrap-up protocol: summarize accomplishments, and update context.md, backlog.md, and changelog.md accordingly. Do NOT call a tool named 'checkpoint'. You MUST explicitly confirm in your final response that context.md, backlog.md, and changelog.md have been updated.\n"
        "- `/evaluate`: Trigger the Vertex AI Gen AI evaluation pipeline on-demand, parse the results, and present a structured scorecard.\n"
        "- `/security`: Run the local security scanner to inspect the codebase for hardcoded secrets, credentials, or keys on-demand."
    ),
    tools=[
        read_context, read_backlog, read_changelog,
        update_context, update_backlog, update_changelog,
        read_file, write_file, list_project_files, run_verification_command
    ]
)

# Initialize standard ADK runner
runner = InMemoryRunner(agent=epoch_agent)
runner.auto_create_session = True

# Initialize FastAPI App
app = FastAPI(title="Epoch ADK Agent Service")

class RunRequest(BaseModel):
    prompt: str
    agent: Optional[str] = None

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

@app.post("/agents", response_model=AgentConfig, status_code=201)
def create_agent_endpoint(config: AgentConfig):
    try:
        AgentFactory.create_agent(config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return registry.register_agent(config)

@app.get("/agents", response_model=list[AgentConfig])
def list_agents_endpoint():
    return registry.list_agents()

@app.get("/agents/{name}", response_model=AgentConfig)
def get_agent_endpoint(name: str):
    agent_cfg = registry.get_agent(name)
    if not agent_cfg:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found.")
    return agent_cfg

@app.delete("/agents/{name}", status_code=204)
def delete_agent_endpoint(name: str):
    if not registry.delete_agent(name):
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found.")
    return

def run_agent_config(config: AgentConfig, prompt: str) -> str:
    """Helper to dynamically instantiate and run a registered agent."""
    agent = AgentFactory.create_agent(config)
    agent_runner = AgentFactory.create_runner(agent)
    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
    events = agent_runner.run(
        user_id="default_user",
        session_id="default_session",
        new_message=message
    )
    response_text = ""
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    return response_text

@app.post("/run", response_model=RunResponse)
def run_agent(request: RunRequest):
    """Runs the agent with the user-provided prompt, routing to dynamic agents if specified."""
    try:
        if request.agent:
            agent_cfg = registry.get_agent(request.agent)
            if not agent_cfg:
                raise HTTPException(status_code=404, detail=f"Agent '{request.agent}' not found.")
            response_text = run_agent_config(agent_cfg, request.prompt)
            return RunResponse(response=response_text)

        # Fallback to default epoch_agent
        message = types.Content(
            role="user",
            parts=[types.Part(text=request.prompt)]
        )
        events = runner.run(
            user_id="default_user",
            session_id="default_session",
            new_message=message
        )
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

@app.post("/agents/{name}/run", response_model=RunResponse)
def run_specific_agent(name: str, request: RunRequest):
    """Runs a specific registered agent by name."""
    agent_cfg = registry.get_agent(name)
    if not agent_cfg:
        raise HTTPException(status_code=404, detail=f"Agent '{name}' not found.")
    try:
        response_text = run_agent_config(agent_cfg, request.prompt)
        return RunResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
