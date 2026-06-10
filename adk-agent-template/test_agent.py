import os
import shutil
import unittest
from main import read_epoch_memory, update_epoch_memory, MEMORY_DIR

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

    def test_read_non_existent_file(self):
        result = read_epoch_memory("context.md")
        self.assertIn("does not exist", result)

    def test_write_and_read_file(self):
        test_content = "# Test Active State\nFramework: Python"
        
        # Test updating memory file
        update_result = update_epoch_memory("context.md", test_content)
        self.assertEqual(update_result, "Successfully updated context.md.")

        # Test reading memory file back
        read_result = read_epoch_memory("context.md")
        self.assertEqual(read_result, test_content)

    def test_invalid_file_name(self):
        with self.assertRaises(ValueError):
            read_epoch_memory("invalid_file.txt")  # type: ignore

        with self.assertRaises(ValueError):
            update_epoch_memory("invalid_file.txt", "content")  # type: ignore

if __name__ == "__main__":
    unittest.main()
