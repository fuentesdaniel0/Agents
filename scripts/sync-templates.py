#!/usr/bin/env python3
import os
import shutil

def sync_directory(src_dir: str, dest_dir: str):
    """Recursively copies files and folders from src to dest."""
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist. Skipping.")
        return
        
    os.makedirs(dest_dir, exist_ok=True)
    
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        
        if os.path.isdir(s):
            sync_directory(s, d)
        else:
            # For memory files, do not overwrite if they already exist in the destination
            if "memory" in src_dir and os.path.exists(d):
                continue
            shutil.copy2(s, d)

def main():
    # Resolve root path of the Epoch project
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_agents_dir = os.path.join(root_dir, "template", ".agents")
    
    destinations = [
        os.path.join(root_dir, ".agents"),
        os.path.join(root_dir, "adk-agent-template", ".agents")
    ]
    
    print("Starting template synchronization...")
    print(f"Source of truth: {template_agents_dir}")
    
    for dest in destinations:
        print(f"Syncing to: {dest} ...")
        sync_directory(template_agents_dir, dest)
        
    print("Template synchronization complete!")

if __name__ == "__main__":
    main()
