#!/usr/bin/env python3
import os
import re
import sys

# Regex definitions for secrets detection
PATTERNS = {
    "Google API Key": re.compile(r"AIzaSy[A-Za-z0-9_\-]{35}"),
    "AWS Access Key ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "AWS Secret Access Key": re.compile(r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z\/+]{40}['\"]"),
    "Slack Webhook": re.compile(r"https://hooks.slack.com/services/T[A-Z0-9_]{8}/B[A-Z0-9_]{8}/[A-Za-z0-9_]{24}"),
    "GitHub Token": re.compile(r"\bgh[oprs]_[A-Za-z0-9_]{36,251}\b"),
    "Private Key Block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Generic Assignment Secret": re.compile(
        r"(?i)(?:key|secret|password|passwd|token)\b[^a-zA-Z0-9]*[:=]\s*['\"]([^'\"]{8,})['\"]"
    )
}

EXCLUDED_VALUES = {
    "gemini-2.5-pro", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash",
    "default_user", "default_session", "epoch_context_agent", "epoch_agent"
}

IGNORED_DIRS = {
    ".git", "venv", "node_modules", "__pycache__", ".pytest_cache",
    "test_memory", "test_registry_dir", "test_routes_memory"
}

IGNORED_FILES = {
    "agents_registry.json", "package-lock.json", "poetry.lock"
}

def is_secret_leak(pattern_name: str, match_text: str, line: str) -> bool:
    # 1. Check for manual inline suppression comment
    if "epoch-secret-ignore" in line:
        return False
        
    # 2. Check for generic assignment exclusions
    if pattern_name == "Generic Assignment Secret":
        # Extract the value from the matched pattern
        val = match_text
        if val in EXCLUDED_VALUES:
            return False
        # If the value is a python variable reference or path or env variable name
        if re.match(r"^[A-Z0-9_]+$", val):
            return False
        if "/" in val or "\\" in val: # file paths
            return False
            
    return True

def scan_file(file_path: str) -> list[dict]:
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, 1):
                for name, pattern in PATTERNS.items():
                    matches = pattern.findall(line)
                    for m in matches:
                        match_text = m if isinstance(m, str) else m[0]
                        if is_secret_leak(name, match_text, line):
                            # Mask secret for display safety
                            masked = match_text[:4] + "..." + match_text[-4:] if len(match_text) > 8 else "..."
                            findings.append({
                                "file": file_path,
                                "line_number": line_no,
                                "type": name,
                                "masked_secret": masked,
                                "line_content": line.strip()
                            })
    except Exception as e:
        # If file cannot be read, ignore it
        pass
    return findings

def main():
    workspace_dir = os.getcwd()
    all_findings = []

    for root, dirs, files in os.walk(workspace_dir):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            if file in IGNORED_FILES:
                continue
            
            # Construct absolute file path
            file_path = os.path.join(root, file)
            # Make path relative to workspace root for cleaner output
            rel_path = os.path.relpath(file_path, workspace_dir)
            
            # Skip checking the security scanner script itself and its tests
            if "security-check.py" in rel_path or "test_security_check.py" in rel_path:
                continue
                
            findings = scan_file(file_path)
            all_findings.extend(findings)

    if all_findings:
        print(" [WARNING] Security scan failed. Hardcoded secrets or credentials detected:")
        for f in all_findings:
            print(f"  - {f['file']}:{f['line_number']} [{f['type']}] (masked: {f['masked_secret']})")
            print(f"    Line: {f['line_content']}")
        print(f"\nTotal findings: {len(all_findings)}. Please resolve these before pushing.")
        sys.exit(1)
        
    print(" [SUCCESS] Security check completed. No secrets detected.")
    sys.exit(0)

if __name__ == "__main__":
    main()
