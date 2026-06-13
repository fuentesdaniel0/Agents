#!/usr/bin/env python3
import os
import re
import sys

def parse_backlog(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: Backlog file not found at {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the roadmap section
    roadmap_match = re.search(r"## High-Level Roadmap\s*\n(.*?)(?:\n##\s|\n---|$)", content, re.DOTALL)
    if not roadmap_match:
        print("Error: '## High-Level Roadmap' section not found.")
        return None

    roadmap_text = roadmap_match.group(1)

    # Find the Session Focus
    focus_match = re.search(r"## Session Focus\s*\n(.*?)(?:\n##\s|\n---|$)", content, re.DOTALL)
    session_focus = ""
    if focus_match:
        session_focus_lines = [l.strip() for l in focus_match.group(1).strip().split("\n") if l.strip()]
        session_focus = " ".join(session_focus_lines)

    milestones = []
    current_milestone = None

    # Parse lines of the roadmap
    lines = roadmap_text.split("\n")
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        if line_stripped.startswith("### "):
            title = line_stripped[4:].strip()
            current_milestone = {
                "title": title,
                "features": [],
                "completed": "completed" in title.lower() or False
            }
            milestones.append(current_milestone)
        elif line_stripped.startswith("*") or line_stripped.startswith("-"):
            if current_milestone is not None:
                # Parse feature
                # e.g., "*   [x] **Feature 1**: ..." or "*   **Feature 1**: ..."
                feature_text = re.sub(r"^[*\-\s]+", "", line_stripped)
                checked = None
                if feature_text.startswith("[x]") or feature_text.startswith("[X]"):
                    checked = True
                    feature_text = feature_text[3:].strip()
                elif feature_text.startswith("[ ]"):
                    checked = False
                    feature_text = feature_text[3:].strip()
                
                feature_text = feature_text.replace("**", "").strip()
                
                current_milestone["features"].append({
                    "text": feature_text,
                    "checked": checked
                })

    for m in milestones:
        if not m["completed"]:
            if m["features"]:
                m["completed"] = all(f["checked"] is True for f in m["features"])
            else:
                m["completed"] = False

    # Determine active milestone
    active_milestone = None
    for m in milestones:
        m_name_clean = re.sub(r"\s*\(Completed\)", "", m["title"], flags=re.IGNORECASE)
        if session_focus and (m_name_clean.lower() in session_focus.lower()):
            active_milestone = m
            break

    if not active_milestone:
        for m in milestones:
            if not m["completed"]:
                active_milestone = m
                break

    return {
        "milestones": milestones,
        "active": active_milestone,
        "session_focus": session_focus
    }

def print_report(data, label: str):
    print("=" * 60)
    print(f" REPORT: {label}")
    print("=" * 60)
    if not data:
        print("No data parsed.")
        return

    print(f"Session Focus: {data['session_focus']}\n")
    
    completed = [m for m in data["milestones"] if m["completed"]]
    active = data["active"]
    upcoming = [m for m in data["milestones"] if not m["completed"] and m != active]

    print("Completed Milestones:")
    if completed:
        for m in completed:
            print(f"  [✓] {m['title']}")
    else:
        print("  (None)")

    print("\nActive Milestone:")
    if active:
        print(f"  [*] {active['title']}")
        for f in active["features"]:
            status = "[x]" if f["checked"] is True else ("[ ]" if f["checked"] is False else "[-]")
            print(f"      {status} {f['text']}")
    else:
        print("  (None)")

    print("\nUpcoming Milestones:")
    if upcoming:
        for m in upcoming:
            print(f"  [ ] {m['title']}")
            for f in m["features"]:
                status = "[x]" if f["checked"] is True else ("[ ]" if f["checked"] is False else "[-]")
                print(f"      {status} {f['text']}")
    else:
        print("  (None)")
    print("=" * 60 + "\n")

def main():
    if len(sys.argv) > 1:
        files_to_check = [(sys.argv[1], sys.argv[1])]
    else:
        # Default to checking pristine and meta
        current_dir = os.path.abspath(os.path.dirname(__file__))
        root_dir = current_dir
        while root_dir != os.path.dirname(root_dir):
            if os.path.exists(os.path.join(root_dir, "README.md")) and os.path.exists(os.path.join(root_dir, "adk-agent-template")):
                break
            root_dir = os.path.dirname(root_dir)

        files_to_check = [
            ("Pristine Backlog Template", os.path.join(root_dir, "template", ".agents", "memory", "backlog.md")),
            ("Active (Meta) Backlog", os.path.join(root_dir, ".agents", "memory", "backlog.md")),
            ("ADK Backlog Template", os.path.join(root_dir, "adk-agent-template", ".agents", "memory", "backlog.md"))
        ]

    success = True
    for label, path in files_to_check:
        print(f"Parsing: {path}")
        data = parse_backlog(path)
        if data is None:
            success = False
        else:
            print_report(data, label)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
