#!/usr/bin/env python3
import os
import shutil

def sync_directory(src_dir: str, dest_dir: str, exclude_dirs=None):
    """Recursively copies files and folders from src to dest, excluding specific directories."""
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist. Skipping.")
        return
        
    os.makedirs(dest_dir, exist_ok=True)
    
    for item in os.listdir(src_dir):
        if exclude_dirs and item in exclude_dirs:
            continue
            
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        
        if os.path.isdir(s):
            sync_directory(s, d, exclude_dirs)
        else:
            # For memory files, do not overwrite if they already exist in the destination
            if "memory" in src_dir and os.path.exists(d):
                continue
            shutil.copy2(s, d)

def main():
    # Resolve root path of the Epoch project by climbing up to the project folder containing 'template'
    current_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = None
    while current_dir and current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, "template")) and os.path.exists(os.path.join(current_dir, "adk-agent-template")):
            root_dir = current_dir
            break
        current_dir = os.path.dirname(current_dir)
        
    if not root_dir:
        print("Error: Could not resolve the project root directory.")
        return
    template_agents_dir = os.path.join(root_dir, "template", ".agents")
    
    print("Starting template synchronization...")
    print(f"Source of truth: {template_agents_dir}")
    
    # 1. Sync to active .agents/ (include scripts for local development convenience)
    active_dest = os.path.join(root_dir, ".agents")
    print(f"Syncing to active workspace: {active_dest} ...")
    sync_directory(template_agents_dir, active_dest)
    
    # 2. Sync to adk-agent-template/.agents/ (exclude scripts/ to prevent template bloat)
    adk_dest = os.path.join(root_dir, "adk-agent-template", ".agents")
    print(f"Syncing to distribution template: {adk_dest} (excluding 'scripts') ...")
    # Clean up scripts directory if it got copied previously
    adk_scripts = os.path.join(adk_dest, "scripts")
    if os.path.exists(adk_scripts):
        print(f"Removing obsolete scripts directory from template: {adk_scripts}")
        shutil.rmtree(adk_scripts)
        
    sync_directory(template_agents_dir, adk_dest, exclude_dirs=["scripts"])
    
    print("Template synchronization complete!")

if __name__ == "__main__":
    main()
