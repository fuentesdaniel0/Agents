#!/usr/bin/env bash

# ==============================================================================
# 🤖 GCP SERVICE ACCOUNT CONFIGURATION FOR GITHUB ACTIONS DEPLOYMENTS
# ==============================================================================
# This script automates the creation of a dedicated Google Cloud Service Account,
# grants it the necessary minimal IAM permissions, and exports the JSON credentials
# key required for GitHub Actions to trigger automated pushes.
#
# RUN THIS SCRIPT LOCALLY ON YOUR DEVELOPER STATION.
# ==============================================================================

set -eo pipefail

# 1. Configuration variables
SA_NAME="github-actions-deployer"
SA_DISPLAY_NAME="GitHub Actions CD Deployer"
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "dev-station-0")
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
KEY_FILE="github-actions-key.json"

echo "----------------------------------------------------"
echo "🌐 Configuring GCP Service Account for GitHub Actions"
echo "Project Target: $PROJECT_ID"
echo "Service Account Email: $SA_EMAIL"
echo "----------------------------------------------------"

# 2. Create the Service Account if it does not exist
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" &>/dev/null; then
  echo "🚀 Creating Service Account [$SA_NAME]..."
  gcloud iam service-accounts create "$SA_NAME" \
    --description="Service account used by GitHub Actions to deploy portfolio updates to Cloud Run" \
    --display-name="$SA_DISPLAY_NAME" \
    --project="$PROJECT_ID"
  # Pause for replication
  sleep 3
else
  echo "✔ Service Account [$SA_NAME] already exists."
fi

# 3. Add precise minimal IAM Role Bindings
ROLES=(
  "roles/run.admin"                   # Ability to deploy and manage Cloud Run revisions
  "roles/storage.admin"               # Ability to upload source tarballs to Cloud Build storage buckets
  "roles/cloudbuild.builds.editor"    # Ability to submit builds using Cloud Build
  "roles/iam.serviceAccountUser"      # Ability to act as the Cloud Run runtime identity
)

echo "🔒 Assigning security roles to service account..."
for ROLE in "${ROLES[@]}"; do
  echo "  └─ Binding role [$ROLE]..."
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="$ROLE" \
    --quiet &>/dev/null
done

# 4. Generate the Credentials Key file
echo "🔑 Generating private JSON key..."
if [ -f "$KEY_FILE" ]; then
  rm -f "$KEY_FILE"
fi

gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="$SA_EMAIL" \
  --project="$PROJECT_ID"

echo "----------------------------------------------------"
echo "🎉 SUCCESS: Service Account and IAM Roles Configured!"
echo "----------------------------------------------------"
echo "👉 WHAT TO DO NEXT:"
echo "1. Open your GitHub Repository in your web browser."
echo "2. Navigate to: Settings ➔ Secrets and variables ➔ Actions."
echo "3. Click [New repository secret]."
echo "4. Name the secret: GCP_SA_KEY"
echo "5. Copy the ENTIRE contents of the newly created local file:"
echo "   [$(pwd)/$KEY_FILE]"
echo "   and paste it as the secret value. Save the secret."
echo "6. IMPORTANT: For safety, delete the local key file after copying:"
echo "   $ rm $(pwd)/$KEY_FILE"
echo "----------------------------------------------------"
