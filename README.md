# Model Validation and Deployment Pipeline

This repository demonstrates a complete GitHub Actions pipeline for model validation and Docker deployment.

## Overview

The pipeline consists of two main jobs:

### 1. Validation Job (`validate`)
- **Pulls Data**: Uses DVC to retrieve the training dataset
- **Trains**: Runs `train.py` to train a RandomForest classifier
- **Observes**: Logs metrics (accuracy, precision, recall, F1) to MLflow
- **Exports**: Creates `model_info.txt` containing the MLflow Run ID
- **Persists**: Uploads the Run ID as an artifact for the next job

### 2. Deployment Job (`deploy`)
- **Downloads**: Retrieves `model_info.txt` from the validation job
- **Checks**: Runs `check_threshold.py` to validate accuracy >= 0.85
- **Containerizes**: If threshold is met, builds a Docker image with the Run ID
- **Deploys**: Simulates deployment (can be extended for real deployments)

## Files

- `.github/workflows/pipeline.yml` - GitHub Actions workflow definition
- `train.py` - Model training script using scikit-learn
- `check_threshold.py` - Performance validation script
- `Dockerfile` - Docker image definition for model serving
- `data/training_data.csv` - Training dataset (generated automatically)
- `model.pkl` - Trained model artifact

## Setup

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Train model locally
python train.py

# Check threshold
python check_threshold.py
```

### MLflow Tracking Server (Optional)

To use a real MLflow server:

```bash
# Start local MLflow server
mlflow ui

# Set environment variable
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### GitHub Secrets

Configure the following secret in your GitHub repository:

- `MLFLOW_TRACKING_URI` - MLflow Tracking Server URI (e.g., http://localhost:5000)

## Pipeline Triggers

The pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

## Expected Behavior

### Successful Run (Accuracy >= 0.85)
1. Training completes with accuracy logged to MLflow
2. Run ID is extracted and saved to `model_info.txt`
3. Deployment job downloads the Run ID
4. Accuracy check passes (>= 0.85)
5. Docker image is built successfully
6. Job marked as ✅ passed

### Failed Run (Accuracy < 0.85)
1. Training completes with accuracy logged to MLflow
2. Run ID is extracted and saved to `model_info.txt`
3. Deployment job downloads the Run ID
4. Accuracy check fails (< 0.85)
5. Deployment job marked as ❌ failed
6. Pipeline stops (no Docker build)

## Dependencies

- Python 3.10+
- scikit-learn
- mlflow
- dvc
- pandas
- numpy
- Docker (for building images)
- joblib

## Example Metrics

A successful model training produces:
- **Accuracy**: 0.85 - 0.95 (varies based on random data)
- **Precision**: 0.80 - 0.95
- **Recall**: 0.80 - 0.95
- **F1 Score**: 0.82 - 0.95

## Testing Locally

```bash
# Create test data
mkdir -p data
python train.py

# Run threshold check
python check_threshold.py

# Build Docker image
docker build -t model-classifier:test --build-arg RUN_ID=test .
```

## Next Steps

1. Push to GitHub repository
2. Configure MLflow Tracking URI secret
3. Create pull request to test the pipeline
4. Monitor the Actions tab for job status
5. Review artifacts for model_info.txt

---

For more information, see the GitHub Actions documentation: https://docs.github.com/en/actions
