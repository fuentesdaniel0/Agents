#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

ENDPOINT = os.environ.get("EPOCH_AGENT_URL", "http://localhost:8080/run")

def get_auth_token() -> str:
    """Retrieves the active gcloud identity token for authentication."""
    # Skip token retrieval for local endpoints
    if "localhost" in ENDPOINT or "127.0.0.1" in ENDPOINT:
        return ""
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-identity-token"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return token
    except Exception:
        print("Error: Could not retrieve gcloud authentication token. Ensure 'gcloud' is authenticated.")
        sys.exit(1)

def send_prompt(prompt: str, token: str):
    """Sends the prompt to the Cloud Run agent and prints the response."""
    data = json.dumps({"prompt": prompt}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            print("\nAgent Response:")
            print(res_data.get("response", "No response content found."))
            print("-" * 50)
    except urllib.error.HTTPError as e:
        print(f"\nError ({e.code}): {e.reason}")
        try:
            err_body = e.read().decode("utf-8")
            print("Detail:", err_body)
        except Exception:
            pass
    except Exception as e:
        print(f"\nError connecting to service: {str(e)}")

def interactive_chat():
    """Starts an interactive REPL chat session with the agent."""
    print("Starting interactive chat with Epoch Agent...")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    token = get_auth_token()
    
    while True:
        try:
            prompt = input("You > ").strip()
            if not prompt:
                continue
            if prompt.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Refresh token periodically if needed (done per call here for safety)
            token = get_auth_token()
            send_prompt(prompt, token)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

def main():
    # If arguments are passed, treat them as a single prompt
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        token = get_auth_token()
        send_prompt(prompt, token)
    else:
        interactive_chat()

if __name__ == "__main__":
    main()
