import os
import shutil
import unittest
import tempfile
import sys
import importlib.util

# Resolve spec for security-check.py to load it dynamically
script_path = os.path.join(os.path.dirname(__file__), "security-check.py")
spec = importlib.util.spec_from_file_location("security_check", script_path)
security_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security_check)

class TestSecurityCheck(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def write_test_file(self, content: str, ext: str = ".py") -> str:
        fd, path = tempfile.mkstemp(dir=self.test_dir, suffix=ext)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_clean_file_returns_no_findings(self):
        content = """
def main():
    print("Hello, world!")
    model_name = "gemini-2.5-pro"
    port_number = PORT
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertEqual(findings, [])

    def test_google_api_key_detected(self):
        content = """
API_KEY = "AIzaSyD-1234567890abcdefghijklmnopqrstuvw"
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertTrue(len(findings) >= 1)
        types = {f["type"] for f in findings}
        self.assertIn("Google API Key", types)

    def test_aws_access_key_detected(self):
        content = """
aws_key = "AKIAIOSFODNN7EXAMPLE"
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertTrue(len(findings) >= 1)
        types = {f["type"] for f in findings}
        self.assertIn("AWS Access Key ID", types)

    def test_slack_webhook_detected(self):
        part1 = "https://hooks.slack.com/services/T12345678/B12345678/"
        part2 = "XXXXXXXXXXXXXXXXXXXXXXXX"
        content = f'url = "{part1}{part2}"\n'
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["type"], "Slack Webhook")

    def test_github_token_detected(self):
        content = """
token = "ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD"
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertTrue(len(findings) >= 1)
        types = {f["type"] for f in findings}
        self.assertIn("GitHub Token", types)

    def test_private_key_block_detected(self):
        content = """
key = "-----BEGIN RSA PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3...\\n-----END PRIVATE KEY-----"
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertTrue(len(findings) >= 1)
        types = {f["type"] for f in findings}
        self.assertIn("Private Key Block", types)

    def test_ignored_comments_are_skipped(self):
        content = """
secret_key = "AIzaSyD-1234567890abcdefghijklmnopqrstuvw" # epoch-secret-ignore
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertEqual(findings, [])

    def test_generic_assignment_exclusions(self):
        content = """
# Model and config names should be ignored
model = "gemini-2.5-pro"
provider = "default_session"
env_var = PORT
"""
        path = self.write_test_file(content)
        findings = security_check.scan_file(path)
        self.assertEqual(findings, [])

if __name__ == "__main__":
    unittest.main()
