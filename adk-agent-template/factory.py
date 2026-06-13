import os
from functools import cached_property
from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import Client
from registry import AgentConfig
import tools

class VertexGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("LOCATION", "us-central1")
        if project:
            return Client(vertexai=True, project=project, location=location)
        return Client()

AVAILABLE_TOOLS = {
    "read_context": tools.read_context,
    "read_backlog": tools.read_backlog,
    "read_changelog": tools.read_changelog,
    "update_context": tools.update_context,
    "update_backlog": tools.update_backlog,
    "update_changelog": tools.update_changelog,
    "read_file": tools.read_file,
    "write_file": tools.write_file,
    "list_project_files": tools.list_project_files,
    "run_verification_command": tools.run_verification_command,
}

class AgentFactory:
    @staticmethod
    def create_agent(config: AgentConfig) -> Agent:
        agent_tools = []
        for t_name in config.tools:
            if t_name in AVAILABLE_TOOLS:
                agent_tools.append(AVAILABLE_TOOLS[t_name])
            else:
                raise ValueError(f"Tool '{t_name}' is not registered or supported in the Factory.")
        
        return Agent(
            name=config.name,
            model=VertexGemini(model=config.model),
            description=config.description,
            instruction=config.instruction,
            tools=agent_tools
        )

    @staticmethod
    def create_runner(agent: Agent) -> InMemoryRunner:
        runner = InMemoryRunner(agent=agent)
        runner.auto_create_session = True
        return runner
