# Testing Guide for Epoch ADK Agent Service

This guide outlines how to verify and test the ADK agent template with Epoch memory integration running as a FastAPI service.

## Prerequisites

Ensure you have created and activated your Python virtual environment and installed the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 1. Running Unit Tests

We have provided a unit test script `test_agent.py` to verify the Epoch memory synchronization tools:

```bash
python test_agent.py
```

Expected Output:
```
Ran 3 tests in 0.001s

OK
```

---

## 2. Local Integration Verification

Start the Uvicorn FastAPI server locally:

```bash
python main.py
```

Once running, verify that the health check endpoint is accessible:

```bash
curl http://localhost:8080/
```

Expected Output:
```json
{
  "status": "healthy",
  "agent": "epoch_context_agent",
  "description": "An AI agent with persistent, stateful memory synchronized via the Epoch protocol."
}
```

### Run a Prompt against the Agent

You can trigger the agent execution by POSTing a JSON prompt request:

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Sync memory and list the roadmaps."}'
```

Expected Output:
A JSON object with the agent's textual response:
```json
{
  "response": "<agent output here>"
}
```

### 3. Interactive Chat REPL (Recommended)

You can run our helper client script `chat.py` to start an interactive conversation loop with the deployed Cloud Run agent:

```bash
python chat.py
```

It will automatically obtain your active `gcloud` identity token, authenticate the request, and handle the interactive prompt/response loop for you.

You can also pass a single prompt directly as command line arguments:

```bash
python chat.py "Sync memory and list the roadmaps"
```

