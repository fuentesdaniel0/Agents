import os
import shutil
import unittest
from fastapi.testclient import TestClient

# Create a test directory first
TEST_DIR = os.path.join(os.path.dirname(__file__), "test_routes_memory")
os.makedirs(TEST_DIR, exist_ok=True)

# Set tools.MEMORY_DIR to TEST_DIR BEFORE importing main!
import tools
tools.MEMORY_DIR = TEST_DIR

# Now import main and app
from main import app, registry

from unittest.mock import patch, MagicMock

class TestFastAPIRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def setUp(self):
        # Clean registry for each test by saving an empty dict
        registry.save({})

    def test_create_and_get_agent(self):
        agent_data = {
            "name": "custom_test_agent",
            "model": "gemini-2.5-flash",
            "description": "Custom agent",
            "instruction": "Explain quantum physics like I'm 5.",
            "tools": ["read_file"]
        }
        # Post request to create
        res = self.client.post("/agents", json=agent_data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["name"], "custom_test_agent")

        # Get request to fetch
        res_get = self.client.get("/agents/custom_test_agent")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["name"], "custom_test_agent")
        self.assertEqual(res_get.json()["tools"], ["read_file"])

    def test_create_agent_invalid_tool(self):
        agent_data = {
            "name": "invalid_tool_agent",
            "instruction": "Test",
            "tools": ["non_existent_tool"]
        }
        res = self.client.post("/agents", json=agent_data)
        self.assertEqual(res.status_code, 400)
        self.assertIn("non_existent_tool", res.json()["detail"])

    def test_create_agent_invalid_name(self):
        agent_data = {
            "name": "invalid-name-agent",
            "instruction": "Test"
        }
        res = self.client.post("/agents", json=agent_data)
        self.assertEqual(res.status_code, 422) # Pydantic validation error

    def test_list_agents(self):
        agent1 = {
            "name": "agent_one",
            "instruction": "Test 1"
        }
        agent2 = {
            "name": "agent_two",
            "instruction": "Test 2"
        }
        self.client.post("/agents", json=agent1)
        self.client.post("/agents", json=agent2)

        res = self.client.get("/agents")
        self.assertEqual(res.status_code, 200)
        agents = res.json()
        self.assertEqual(len(agents), 2)
        names = {a["name"] for a in agents}
        self.assertEqual(names, {"agent_one", "agent_two"})

    def test_delete_agent(self):
        agent_data = {
            "name": "agent_to_delete",
            "instruction": "Delete me"
        }
        self.client.post("/agents", json=agent_data)

        # Delete
        res_del = self.client.delete("/agents/agent_to_delete")
        self.assertEqual(res_del.status_code, 204)

        # Get should now return 404
        res_get = self.client.get("/agents/agent_to_delete")
        self.assertEqual(res_get.status_code, 404)

    def test_get_non_existent_agent(self):
        res = self.client.get("/agents/non_existent")
        self.assertEqual(res.status_code, 404)

    def test_delete_non_existent_agent(self):
        res = self.client.delete("/agents/non_existent")
        self.assertEqual(res.status_code, 404)

    @patch("google.adk.runners.InMemoryRunner.run")
    def test_run_dynamic_agent_via_specific_route(self, mock_run):
        mock_event = MagicMock()
        mock_event.content.parts = [MagicMock(text="Hello from dynamic mock agent!")]
        mock_run.return_value = [mock_event]

        agent_data = {
            "name": "mock_agent",
            "instruction": "Say hello.",
            "tools": []
        }
        self.client.post("/agents", json=agent_data)

        res = self.client.post("/agents/mock_agent/run", json={"prompt": "test prompt"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["response"], "Hello from dynamic mock agent!")

    @patch("google.adk.runners.InMemoryRunner.run")
    def test_run_dynamic_agent_via_generic_route(self, mock_run):
        mock_event = MagicMock()
        mock_event.content.parts = [MagicMock(text="Hello from generic route mock agent!")]
        mock_run.return_value = [mock_event]

        agent_data = {
            "name": "mock_agent_generic",
            "instruction": "Say hello generic.",
            "tools": []
        }
        self.client.post("/agents", json=agent_data)

        res = self.client.post("/run", json={"prompt": "test prompt", "agent": "mock_agent_generic"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["response"], "Hello from generic route mock agent!")

if __name__ == "__main__":
    unittest.main()
