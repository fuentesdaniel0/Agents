#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

def print_banner():
    print("=" * 60)
    print("          Epoch Agent Project Bootstrapper CLI")
    print("=" * 60)

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("Error: Target project directory path must be provided.")
        print("Usage: python3 .agents/scripts/create-agent.py <target-directory>")
        sys.exit(1)
        
    target_dir = os.path.abspath(sys.argv[1])
    # Resolve root path of the Epoch project
    current_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = None
    while current_dir and current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, "template")) and os.path.exists(os.path.join(current_dir, "adk-agent-template")):
            root_dir = current_dir
            break
        current_dir = os.path.dirname(current_dir)
        
    if not root_dir:
        print("Error: Could not resolve the project root directory.")
        sys.exit(1)
        
    template_dir = os.path.join(root_dir, "adk-agent-template")
    
    if os.path.exists(target_dir):
        if os.listdir(target_dir):
            print(f"Error: Target directory {target_dir} exists and is not empty.")
            sys.exit(1)
    else:
        print(f"Creating directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)

    # 1. Copy template files excluding venv, __pycache__, and test_memory
    print("\nCopying agent template files...")
    ignore_patterns = shutil.ignore_patterns(
        "venv", "__pycache__", ".pytest_cache", "test_memory", "*.pyc"
    )
    
    for item in os.listdir(template_dir):
        s = os.path.join(template_dir, item)
        d = os.path.join(target_dir, item)
        
        # Apply ignores
        ignored = ignore_patterns(template_dir, [item])
        if item in ignored:
            continue
            
        if os.path.isdir(s):
            shutil.copytree(s, d, ignore=ignore_patterns)
        else:
            shutil.copy2(s, d)

    print("Template files copied successfully.")

    # 2. Interactive configuration interview
    print("\n--- Configuration Phase ---")
    
    agent_name = input("Agent Registry Name [epoch_context_agent]: ").strip()
    if not agent_name:
        agent_name = "epoch_context_agent"
        
    gcp_project = input("GCP Project ID (optional): ").strip()
    
    gcp_location = input("GCP Location/Region [us-central1]: ").strip()
    if not gcp_location:
        gcp_location = "us-central1"
        
    agent_model = input("Gemini Model [gemini-2.5-pro]: ").strip()
    if not agent_model:
        agent_model = "gemini-2.5-pro"

    # 3. Create .env configuration file
    env_path = os.path.join(target_dir, ".env")
    print(f"\nWriting environment configuration to {env_path}...")
    with open(env_path, "w", encoding="utf-8") as env_file:
        env_file.write(f"AGENT_NAME={agent_name}\n")
        if gcp_project:
            env_file.write(f"GOOGLE_CLOUD_PROJECT={gcp_project}\n")
        env_file.write(f"LOCATION={gcp_location}\n")
        env_file.write(f"AGENT_MODEL={agent_model}\n")
        env_file.write("EPOCH_MEMORY_DIR=.agents/memory\n")

    # 4. Optional Git initialization
    git_init = input("\nInitialize a new Git repository in the target directory? (y/n) [y]: ").strip().lower()
    if git_init in ["", "y", "yes"]:
        print("Initializing git repository...")
        try:
            subprocess.run(["git", "init"], cwd=target_dir, check=True)
            # Copy root .gitignore to destination
            shutil.copy2(os.path.join(root_dir, ".gitignore"), os.path.join(target_dir, ".gitignore"))
            print("Git repository initialized with default .gitignore.")
        except Exception as e:
            print(f"Warning: Could not initialize Git repository: {str(e)}")

    # 5. Optional Virtual Environment and dependency installation
    setup_venv = input("\nCreate Python virtual environment and install dependencies? (y/n) [y]: ").strip().lower()
    if setup_venv in ["", "y", "yes"]:
        print("Creating virtual environment (this may take a minute)...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=target_dir, check=True)
            print("Virtual environment created.")
            
            # Identify pip path inside target venv
            pip_cmd = os.path.join(target_dir, "venv", "bin", "pip")
            if os.name == "nt": # Windows fallback
                pip_cmd = os.path.join(target_dir, "venv", "Scripts", "pip")
                
            print("Installing dependencies...")
            subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], cwd=target_dir, check=True)
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"Warning: Failed to set up python environment or install packages: {str(e)}")

    # 6. Success and instructions output
    print("\n" + "=" * 60)
    print("          SUCCESS: Agent Project Successfully Created!")
    print("=" * 60)
    print(f"Path: {target_dir}")
    print("\nNext steps to start developing:")
    print(f"  1. cd {sys.argv[1]}")
    print("  2. source venv/bin/activate")
    print("  3. python main.py  # Launches FastAPI agent service")
    print("  4. python chat.py  # Starts interactive chat loop")
    print("=" * 60)

if __name__ == "__main__":
    main()
