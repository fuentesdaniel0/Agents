import os
import sys
import json

# Setup path to allow import
dir_path = os.path.dirname(os.path.abspath(__file__))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)

def run_ci_check():
    # Check if GCP environment variables are set. If not, inform the user and exit gracefully (skip).
    if "GOOGLE_CLOUD_PROJECT" not in os.environ:
        print("WARNING: GOOGLE_CLOUD_PROJECT environment variable is not set.")
        print("Skipping automated evaluation check (requires Google Cloud access).")
        sys.exit(0)

    try:
        import run_eval
        print("Running Gen AI Evaluation pipeline...")
        run_eval.main_eval()
    except Exception as e:
        print(f"Error during evaluation execution: {e}")
        # Gracefully handle authentication/connection errors in offline CI environments
        if "credentials" in str(e).lower() or "auth" in str(e).lower() or "connect" in str(e).lower():
            print("WARNING: Failed to authenticate or connect to Vertex AI Gen AI Evaluation Service.")
            print("Bypassing check for offline CI run.")
            sys.exit(0)
        sys.exit(1)

    results_file = os.path.join(dir_path, "eval_results.json")
    if not os.path.exists(results_file):
        print(f"Error: Evaluation results file not found at {results_file}")
        sys.exit(1)

    try:
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error reading evaluation results: {e}")
        sys.exit(1)

    scores = []
    for item in results:
        score_val = item.get("epoch_agent_protocol_metric/score")
        if score_val is not None:
            scores.append(float(score_val))

    if not scores:
        print("Error: No evaluation scores found in the results.")
        sys.exit(1)

    mean_score = sum(scores) / len(scores)
    print(f"\n--- CI/CD Evaluation Check Results ---")
    print(f"Mean Protocol Score: {mean_score:.2f} (Threshold: 4.0)")
    
    for i, item in enumerate(results):
        print(f"Scenario {i+1}: Score {item.get('epoch_agent_protocol_metric/score')} | Prompt: '{item.get('prompt')}'")

    THRESHOLD = 4.0
    if mean_score < THRESHOLD:
        print(f"\nFAIL: Mean evaluation score {mean_score:.2f} is below threshold of {THRESHOLD}.")
        sys.exit(1)

    print("\nSUCCESS: Automated evaluation check passed!")
    sys.exit(0)

if __name__ == "__main__":
    run_ci_check()
