import os
import subprocess

# Define the base directory for Epoch memory
MEMORY_DIR = os.environ.get("EPOCH_MEMORY_DIR", ".agents/memory")

def get_memory_path(file_name: str) -> str:
    """Helper to resolve the absolute path to memory files."""
    if file_name not in ["context.md", "backlog.md", "changelog.md"]:
        raise ValueError("Invalid memory file name. Must be context.md, backlog.md, or changelog.md")
    return os.path.join(MEMORY_DIR, file_name)

# Define native tools for Epoch state synchronization
def _read_epoch_memory(file_name: str) -> str:
    path = get_memory_path(file_name)
    if not os.path.exists(path):
        return f"Error: Memory file {file_name} does not exist at {path}."
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_name}: {str(e)}"

def _update_epoch_memory(file_name: str, content: str) -> str:
    path = get_memory_path(file_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully updated {file_name}."
    except Exception as e:
        return f"Error updating file {file_name}: {str(e)}"

def read_context() -> str:
    """Reads the contents of context.md to synchronize current project context and architecture state."""
    return _read_epoch_memory("context.md")

def read_backlog() -> str:
    """Reads the contents of backlog.md to synchronize the product backlog and session focus."""
    return _read_epoch_memory("backlog.md")

def read_changelog() -> str:
    """Reads the contents of changelog.md to synchronize completed sprints and decisions."""
    return _read_epoch_memory("changelog.md")

def update_context(content: str) -> str:
    """Overwrites or updates context.md to persist current project context and architecture changes."""
    return _update_epoch_memory("context.md", content)

def update_backlog(content: str) -> str:
    """Overwrites or updates backlog.md to persist session focus and active tasks."""
    return _update_epoch_memory("backlog.md", content)

def update_changelog(content: str) -> str:
    """Overwrites or updates changelog.md to persist completed sprints and decisions."""
    return _update_epoch_memory("changelog.md", content)

# Define native tools for project filesystem access and execution
def read_file(file_path: str) -> str:
    """Reads the content of any file within the project workspace directory."""
    resolved_path = os.path.abspath(file_path)
    # Prevent path traversal outside the workspace
    if not resolved_path.startswith(os.getcwd()):
        return "Error: Access denied. Paths must be within the workspace directory."
    if not os.path.exists(resolved_path):
        return f"Error: File {file_path} does not exist."
    try:
        with open(resolved_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Writes or overwrites a file within the project workspace directory."""
    resolved_path = os.path.abspath(file_path)
    # Prevent path traversal outside the workspace
    if not resolved_path.startswith(os.getcwd()):
        return "Error: Access denied. Paths must be within the workspace directory."
    try:
        os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
        with open(resolved_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote file: {file_path}"
    except Exception as e:
        return f"Error writing file {file_path}: {str(e)}"

def list_project_files() -> str:
    """Lists all files and directories in the workspace recursively, excluding venv and cache folders."""
    try:
        files_list = []
        for root, dirs, files in os.walk(os.getcwd()):
            # Prune directories we don't want to traverse
            dirs[:] = [d for d in dirs if d not in ["venv", ".git", "__pycache__"]]
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                files_list.append(rel_path)
        return "\n".join(files_list) if files_list else "No files found."
    except Exception as e:
        return f"Error listing workspace: {str(e)}"

def run_verification_command(command: str) -> str:
    """Runs a verification command (e.g. test, lint, or type check) in the workspace shell."""
    allowed_commands = ["pytest", "python", "python3", "pip", "uvicorn", "black", "flake8", "mypy", "npm test", "npm run"]
    parts = command.split()
    if not parts or parts[0] not in allowed_commands:
        return f"Error: Command prefix '{parts[0]}' is not in the allowed list of verification commands."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error running command: {str(e)}"
