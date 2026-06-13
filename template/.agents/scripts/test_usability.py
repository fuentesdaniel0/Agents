import os
import shutil
import unittest
import tempfile
import subprocess
import sys

class TestUsability(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Resolve root path of the Epoch project
        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.root_dir = None
        while current_dir and current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, "template")) and os.path.exists(os.path.join(current_dir, "adk-agent-template")):
                self.root_dir = current_dir
                break
            current_dir = os.path.dirname(current_dir)
            
        if not self.root_dir:
            raise RuntimeError("Could not find project root directory")
            
        self.create_agent_path = os.path.join(self.root_dir, ".agents", "scripts", "create-agent.py")
        self.sync_templates_path = os.path.join(self.root_dir, ".agents", "scripts", "sync-templates.py")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_agent_without_venv_and_git(self):
        target_project_dir = os.path.join(self.test_dir, "my-test-agent")
        
        # We simulate stdin:
        # Agent Name: test_agent_run
        # GCP Project ID: my-test-project
        # GCP Location: us-central1
        # Gemini Model: gemini-2.5-flash
        # Git Init: n
        # Venv Setup: n
        inputs = "test_agent_run\nmy-test-project\nus-central1\ngemini-2.5-flash\nn\nn\n"
        
        process = subprocess.Popen(
            [sys.executable, self.create_agent_path, target_project_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=inputs)
        
        self.assertEqual(process.returncode, 0, f"create-agent.py failed:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        
        # Verify copied files
        self.assertTrue(os.path.exists(target_project_dir))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, "main.py")))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, "registry.py")))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, "factory.py")))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, "tools.py")))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, ".env")))
        
        # Verify .env content
        with open(os.path.join(target_project_dir, ".env"), "r", encoding="utf-8") as f:
            env_content = f.read()
            self.assertIn("AGENT_NAME=test_agent_run", env_content)
            self.assertIn("GOOGLE_CLOUD_PROJECT=my-test-project", env_content)
            self.assertIn("LOCATION=us-central1", env_content)
            self.assertIn("AGENT_MODEL=gemini-2.5-flash", env_content)
            self.assertIn("EPOCH_MEMORY_DIR=.agents/memory", env_content)

    def test_create_agent_with_git_no_venv(self):
        target_project_dir = os.path.join(self.test_dir, "my-git-agent")
        
        inputs = "git_agent\n\nus-east4\ngemini-2.5-pro\ny\nn\n"
        
        process = subprocess.Popen(
            [sys.executable, self.create_agent_path, target_project_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=inputs)
        
        self.assertEqual(process.returncode, 0, f"create-agent.py failed:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
        
        # Verify git init and gitignore
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, ".git")))
        self.assertTrue(os.path.exists(os.path.join(target_project_dir, ".gitignore")))

    def test_sync_templates_execution(self):
        # Run sync-templates.py and verify exit code is 0
        result = subprocess.run(
            [sys.executable, self.sync_templates_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"sync-templates.py failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

if __name__ == "__main__":
    unittest.main()
