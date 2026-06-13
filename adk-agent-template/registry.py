import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class AgentConfig(BaseModel):
    name: str = Field(..., description="Unique name of the agent")
    model: str = Field(default="gemini-2.5-pro", description="Model name to use")
    description: str = Field(default="", description="A short description of the agent")
    instruction: str = Field(..., description="System instruction for the agent")
    tools: List[str] = Field(default_factory=list, description="Enabled tools for the agent")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("Agent name must be a valid Python identifier (letters, numbers, and underscores, starting with a letter or underscore).")
        return v

class AgentRegistry:
    def __init__(self, registry_file: str):
        self.registry_file = registry_file
        self._ensure_registry_exists()

    def _ensure_registry_exists(self):
        directory = os.path.dirname(self.registry_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load(self) -> dict[str, AgentConfig]:
        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {name: AgentConfig(**cfg) for name, cfg in data.items()}
        except Exception:
            return {}

    def save(self, agents: dict[str, AgentConfig]):
        data = {name: cfg.model_dump() for name, cfg in agents.items()}
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register_agent(self, config: AgentConfig) -> AgentConfig:
        agents = self.load()
        agents[config.name] = config
        self.save(agents)
        return config

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        agents = self.load()
        return agents.get(name)

    def list_agents(self) -> List[AgentConfig]:
        agents = self.load()
        return list(agents.values())

    def delete_agent(self, name: str) -> bool:
        agents = self.load()
        if name in agents:
            del agents[name]
            self.save(agents)
            return True
        return False
