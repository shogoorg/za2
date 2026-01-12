#!/bin/bash

PROJECT_ID=$(gcloud config get-value project)
DATASET_NAME="za2"  #  [YOUR-DATASET-NAME]

LOCATION="US"

# Generate bucket name if not provided
if [ -z "$1" ]; then
    BUCKET_NAME="gs://za2-data-$PROJECT_ID" #  [YOUR-BUCKET-NAME]
    echo "No bucket provided. Using default: $BUCKET_NAME"
else
    BUCKET_NAME=$1
fi

echo "----------------------------------------------------------------"
echo "Setup Climate Scorecard Data"
echo "Project: $PROJECT_ID"
echo "Dataset: $DATASET_NAME"
echo "Bucket:  $BUCKET_NAME"
echo "----------------------------------------------------------------"

# 1. Create Bucket if it doesn't exist
echo "Checking bucket $BUCKET_NAME..."
if gcloud storage buckets describe $BUCKET_NAME >/dev/null 2>&1; then
    echo "      Bucket already exists."
else
    echo "      Creating bucket $BUCKET_NAME..."
    gcloud storage buckets create $BUCKET_NAME --location=$LOCATION
fi

# 2. Upload Data
echo "Uploading cleansed data to $BUCKET_NAME..."
gcloud storage cp data/*.csv $BUCKET_NAME


# 3. Create Dataset
echo "Creating Dataset '$DATASET_NAME'..."
if bq show "$PROJECT_ID:$DATASET_NAME" >/dev/null 2>&1; then
    echo "      Dataset already exists. Skipping creation."
else    
    bq mk --location=$LOCATION --dataset \
        "$PROJECT_ID:$DATASET_NAME"
    echo "      Dataset created."
fi

# 4. Create user_request Table
echo "Setting up Table: user_request..."
bq load --source_format=CSV --autodetect --skip_leading_rows=1 --replace \
    --allow_quoted_newlines \
    "$PROJECT_ID:$DATASET_NAME.user_request" "$BUCKET_NAME/user_request.csv"
echo "      Table user_request loaded."

# 5. Create context_document Table
echo "Setting up Table: context_document..."
bq load --source_format=CSV --autodetect --skip_leading_rows=1 --replace \
    --allow_quoted_newlines \
    "$PROJECT_ID:$DATASET_NAME.context_document" "$BUCKET_NAME/context_document.csv"
echo "      Table context_document loaded."

echo "----------------------------------------------------------------"
echo "Setup Complete!"
echo "----------------------------------------------------------------"