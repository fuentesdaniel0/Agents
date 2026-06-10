import os
import shutil
import unittest
from main import (
    read_context, update_context,
    read_backlog, update_backlog,
    read_changelog, update_changelog,
    MEMORY_DIR
)

class TestEpochAgentTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup temporary test memory folder
        cls.test_dir = os.path.join(os.path.dirname(__file__), "test_memory")
        os.makedirs(cls.test_dir, exist_ok=True)
        # Override the global MEMORY_DIR dynamically for the test run
        import main
        main.MEMORY_DIR = cls.test_dir

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

if __name__ == "__main__":
    unittest.main()
