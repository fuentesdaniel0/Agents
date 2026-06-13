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

We have provided a comprehensive unit and integration test suite in `test_agent.py` which discovers tests for the Epoch memory tools, agent registry, agent factory, and FastAPI endpoints:

```bash
python test_agent.py
```

Expected Output:
```
Ran 42 tests in 0.26s

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

### Run a Prompt against the Default Agent

You can trigger the agent execution by POSTing a JSON prompt request:

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the current state of our project?"}'
```

---

## 3. Testing the Dynamic Agent Factory

You can verify the dynamic Agent Factory endpoints using `curl` while the local server is running:

### A. Register a Custom Agent
```bash
curl -X POST http://localhost:8080/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "math_tutor",
    "model": "gemini-2.5-flash",
    "description": "A friendly math tutor",
    "instruction": "Explain math concepts simply using examples.",
    "tools": ["read_file"]
  }'
```

### B. List Registered Agents
```bash
curl http://localhost:8080/agents
```

### C. Run a Dynamic Agent
You can run the custom agent either by POSTing to the generic `/run` endpoint with the `"agent"` parameter:
```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain addition",
    "agent": "math_tutor"
  }'
```
Or by POSTing directly to the agent-specific route:
```bash
curl -X POST http://localhost:8080/agents/math_tutor/run \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain subtraction"}'
```

### D. Delete the Agent
```bash
curl -X DELETE http://localhost:8080/agents/math_tutor
```

---

## 4. Running Automated Evaluations

The template includes an automated evaluation pipeline that tests agent protocol adherence, goal completion, and filesystem safety using the Vertex AI Gen AI Evaluation Service.

### Run the Evaluation Pipeline
```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
python evaluation/run_eval.py
```

### Run the CI Score Check
```bash
python evaluation/ci_eval_check.py
```
This script will verify if the mean score of the scenarios is above the required threshold of `4.0`.

---

## 5. Interactive Chat REPL (Recommended)

You can run our helper client script `chat.py` to start an interactive conversation loop with the deployed Cloud Run agent:

```bash
python chat.py
```

It will automatically obtain your active `gcloud` identity token, authenticate the request, and handle the interactive prompt/response loop for you.

You can also pass a single prompt directly as command line arguments:

```bash
python chat.py "Sync memory and list the roadmaps"
```


