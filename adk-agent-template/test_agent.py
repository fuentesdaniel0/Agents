import os
import shutil
import unittest
from main import (
    read_context, update_context,
    read_backlog, update_backlog,
    read_changelog, update_changelog,
    read_file, write_file, list_project_files, run_verification_command,
    MEMORY_DIR
)

class TestEpochAgentTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup temporary test memory folder
        cls.test_dir = os.path.join(os.path.dirname(__file__), "test_memory")
        os.makedirs(cls.test_dir, exist_ok=True)
        # Override the global MEMORY_DIR dynamically for the test run
        import tools
        tools.MEMORY_DIR = cls.test_dir

    @classmethod
    def tearDownClass(cls):
        # Clean up temporary test folder
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_read_non_existent_files(self):
        self.assertIn("does not exist", read_context())
        self.assertIn("does not exist", read_backlog())
        self.assertIn("does not exist", read_changelog())

    def test_write_and_read_context(self):
        test_content = "# Test Active State\nFramework: Python"
        update_result = update_context(test_content)
        self.assertEqual(update_result, "Successfully updated context.md.")
        self.assertEqual(read_context(), test_content)

    def test_write_and_read_backlog(self):
        test_content = "- [ ] Task 1\n- [ ] Task 2"
        update_result = update_backlog(test_content)
        self.assertEqual(update_result, "Successfully updated backlog.md.")
        self.assertEqual(read_backlog(), test_content)

    def test_write_and_read_changelog(self):
        test_content = "## Sprint 1\nDone everything."
        update_result = update_changelog(test_content)
        self.assertEqual(update_result, "Successfully updated changelog.md.")
        self.assertEqual(read_changelog(), test_content)

    def test_filesystem_path_traversal_protection(self):
        # Verify read_file blocks traversal
        self.assertIn("Access denied", read_file("../README.md"))
        self.assertIn("Access denied", read_file("/etc/passwd"))

        # Verify write_file blocks traversal
        self.assertIn("Access denied", write_file("../malicious.py", "print('bad')"))

    def test_write_and_read_file_within_workspace(self):
        filename = "test_temp_file.txt"
        content = "Hello from unit tests!"
        
        # Clean up if exists
        if os.path.exists(filename):
            os.remove(filename)
            
        try:
            write_res = write_file(filename, content)
            self.assertIn("Successfully wrote file", write_res)
            self.assertEqual(read_file(filename), content)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_list_project_files(self):
        files = list_project_files()
        self.assertIn("main.py", files)
        self.assertNotIn("venv", files)

    def test_run_verification_command(self):
        # Valid execution command
        res = run_verification_command("python3 --version")
        self.assertIn("Python", res)

        # Unauthorized command
        res = run_verification_command("cat /etc/passwd")
        self.assertIn("is not in the allowed list", res)

# Import other test classes to consolidate test runner
from test_registry import TestAgentRegistry
from test_factory import TestAgentFactory
from test_routes import TestFastAPIRoutes

if __name__ == "__main__":
    unittest.main()
