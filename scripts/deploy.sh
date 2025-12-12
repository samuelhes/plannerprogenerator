#!/bin/bash
set -e

# Configuration
SERVICE_NAME="planner-pro-generator"
REGION="us-central1"
PROJECT_ID=$(gcloud config get-value project)

# Color Codes
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[1/4] Checking Dependencies...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud SDK is not installed."
    exit 1
fi

echo -e "${GREEN}[2/4] Building Container...${NC}"
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

echo -e "${GREEN}[3/4] Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10

echo -e "${GREEN}[4/4] Deployment Complete!${NC}"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo -e "Your World-Class App is live at: ${GREEN}$SERVICE_URL${NC}"
