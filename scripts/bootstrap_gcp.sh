#!/bin/bash
set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=========================================================${NC}"
echo -e "${BLUE}   Planner Pro: Automated Google Cloud Initializer 🚀    ${NC}"
echo -e "${BLUE}=========================================================${NC}"
echo ""
echo "This script will create a new Google Cloud Project and deploy the app."
echo "Prerequisite: You must have an active Billing Account in Google Cloud."
echo ""

# 1. Project Creation
read -p "Enter a NEW Project ID (e.g., planner-pro-v3-prod): " PROJECT_ID
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Project ID is required.${NC}"
    exit 1
fi

echo -e "${YELLOW}Creating project '$PROJECT_ID'...${NC}"
gcloud projects create $PROJECT_ID --name="Planner Pro V3" || echo "Project might already exist, continuing..."
gcloud config set project $PROJECT_ID

# 2. Billing Linkage
echo ""
echo -e "${BLUE}--- Billing Configuration ---${NC}"
echo "List of available billing accounts:"
gcloud beta billing accounts list --format="table(displayName, name, open)"

echo ""
echo -e "${YELLOW}Copy the 'ACCOUNT_ID' (format: XXXXXX-XXXXXX-XXXXXX) from above.${NC}"
read -p "Paste Billing Account ID: " BILLING_ID

if [ -z "$BILLING_ID" ]; then
    echo -e "${RED}Billing ID is required to enable Cloud Services.${NC}"
    exit 1
fi

echo "Linking billing account..."
gcloud beta billing projects link $PROJECT_ID --billing-account=$BILLING_ID

# 3. Enable APIs
echo ""
echo -e "${BLUE}--- Enabling Cloud APIs (Run, Build, Container) ---${NC}"
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       containerregistry.googleapis.com \
                       artifactregistry.googleapis.com

# 4. Deploy
echo ""
echo -e "${BLUE}--- Starting Deployment ---${NC}"
chmod +x ./scripts/deploy.sh
./scripts/deploy.sh

echo ""
echo -e "${GREEN}SUCCESS! System fully provisioned and deployed.${NC}"
echo -e "Manage your project at: https://console.cloud.google.com/home/dashboard?project=$PROJECT_ID"
