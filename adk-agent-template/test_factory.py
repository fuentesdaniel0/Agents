import unittest
from registry import AgentConfig
from factory import AgentFactory
from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner

class TestAgentFactory(unittest.TestCase):
    def test_create_agent_with_valid_tools(self):
        config = AgentConfig(
            name="valid_agent",
            model="gemini-2.5-flash",
            description="A valid test agent",
            instruction="Be helpful.",
            tools=["read_file", "write_file"]
        )
        agent = AgentFactory.create_agent(config)
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.name, "valid_agent")
        self.assertEqual(agent.description, "A valid test agent")
        self.assertEqual(agent.instruction, "Be helpful.")
        # Verify that the actual callable functions are populated
        self.assertEqual(len(agent.tools), 2)
        tool_names = {t.__name__ for t in agent.tools}
        self.assertEqual(tool_names, {"read_file", "write_file"})

    def test_create_agent_with_invalid_tool_raises_error(self):
        config = AgentConfig(
            name="invalid_agent",
            instruction="Be helpful.",
            tools=["non_existent_tool"]
        )
        with self.assertRaises(ValueError) as context:
            AgentFactory.create_agent(config)
        self.assertIn("non_existent_tool", str(context.exception))

    def test_create_runner(self):
        config = AgentConfig(
            name="runner_agent",
            instruction="Run."
        )
        agent = AgentFactory.create_agent(config)
        runner = AgentFactory.create_runner(agent)
        self.assertIsInstance(runner, InMemoryRunner)
        self.assertEqual(runner.agent.name, "runner_agent")
        self.assertTrue(runner.auto_create_session)

if __name__ == "__main__":
    unittest.main()
