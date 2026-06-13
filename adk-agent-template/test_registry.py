import os
import shutil
import unittest
from registry import AgentConfig, AgentRegistry

class TestAgentRegistry(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_registry_dir")
        os.makedirs(self.test_dir, exist_ok=True)
        self.registry_file = os.path.join(self.test_dir, "registry.json")
        self.registry = AgentRegistry(self.registry_file)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_ensure_registry_exists_creates_empty_file(self):
        self.assertTrue(os.path.exists(self.registry_file))
        self.assertEqual(self.registry.load(), {})

    def test_register_and_get_agent(self):
        config = AgentConfig(
            name="test_agent",
            model="gemini-2.5-flash",
            description="Test description",
            instruction="You are a test agent.",
            tools=["read_file", "write_file"]
        )
        self.registry.register_agent(config)
        
        retrieved = self.registry.get_agent("test_agent")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "test_agent")
        self.assertEqual(retrieved.model, "gemini-2.5-flash")
        self.assertEqual(retrieved.description, "Test description")
        self.assertEqual(retrieved.instruction, "You are a test agent.")
        self.assertEqual(retrieved.tools, ["read_file", "write_file"])

    def test_list_agents(self):
        config1 = AgentConfig(name="agent1", instruction="Instr 1")
        config2 = AgentConfig(name="agent2", instruction="Instr 2")
        self.registry.register_agent(config1)
        self.registry.register_agent(config2)

        agents = self.registry.list_agents()
        self.assertEqual(len(agents), 2)
        names = {a.name for a in agents}
        self.assertEqual(names, {"agent1", "agent2"})

    def test_delete_agent(self):
        config = AgentConfig(name="agent_to_delete", instruction="Delete me")
        self.registry.register_agent(config)
        self.assertTrue(self.registry.delete_agent("agent_to_delete"))
        self.assertIsNone(self.registry.get_agent("agent_to_delete"))
        self.assertFalse(self.registry.delete_agent("agent_to_delete"))

    def test_invalid_identifier_name_raises_error(self):
        with self.assertRaises(ValueError):
            AgentConfig(name="invalid-name", instruction="test")
        with self.assertRaises(ValueError):
            AgentConfig(name="123agent", instruction="test")

if __name__ == "__main__":
    unittest.main()
