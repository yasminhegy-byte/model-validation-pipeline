# Deployment Guide

## Setting Up the GitHub Actions Pipeline

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `model-validation-pipeline`)
3. Initialize with a README

### Step 2: Push Local Code to GitHub

```bash
# In your local repository directory
git remote add origin https://github.com/YOUR_USERNAME/model-validation-pipeline.git
git branch -M main
git push -u origin main
```

### Step 3: Configure GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add the secret:
   - **Name**: `MLFLOW_TRACKING_URI`
   - **Value**: `http://your-mlflow-server:5000` (or leave as default for local testing)

### Step 4: Test the Pipeline

1. Create a new branch for testing:
   ```bash
   git checkout -b test-pipeline
   ```

2. Make a small change (e.g., update README)

3. Commit and push:
   ```bash
   git add .
   git commit -m "Test pipeline run"
   git push origin test-pipeline
   ```

4. Create a Pull Request to `main`

5. Go to the **Actions** tab and watch the workflow execute

### Step 5: Generate Test Runs

#### For a Failed Run (Accuracy < 0.85):
- The default data generation produces 0.70 accuracy
- Simply run the workflow (no special configuration needed)

#### For a Successful Run (Accuracy > 0.85):
- Modify `.github/workflows/pipeline.yml` to add environment variable:
  ```yaml
  - name: Train model
    id: train
    env:
      MLFLOW_TRACKING_URI: ${{ env.MLFLOW_TRACKING_URI }}
      TRAIN_SEED: 99  # Add this line for high accuracy
    run: |
      python train.py
  ```

## Expected Pipeline Behavior

### On Failed Run (Accuracy < 0.85):
```
✅ validate job completes
   - Trains model (accuracy: 0.70)
   - Creates model_info.txt
   - Uploads artifact

❌ deploy job FAILS
   - Downloads model_info.txt
   - check_threshold.py fails: "Accuracy 0.70 < threshold 0.85"
   - Pipeline stops (no Docker build)
```

### On Successful Run (Accuracy >= 0.85):
```
✅ validate job completes
   - Trains model (accuracy: >= 0.85)
   - Creates model_info.txt
   - Uploads artifact

✅ deploy job SUCCEEDS
   - Downloads model_info.txt
   - check_threshold.py passes: "Accuracy >= 0.85"
   - Builds Docker image
   - Deployment summary displayed
```

## MLflow Tracking

### Local MLflow Server Setup (Optional)

```bash
# Install MLflow
pip install mlflow

# Start MLflow UI
mlflow ui

# Access at http://localhost:5000
```

### Using External MLflow Server

Set the secret in GitHub:
```
MLFLOW_TRACKING_URI=https://your-mlflow-server.com
```

## Troubleshooting

### Pipeline Not Running
- Check that at least one file is modified on push/PR
- Verify branch name matches workflow trigger (main/develop)

### Threshold Check Fails
- Confirm check_threshold.py is properly reading model_info.txt
- Verify MLflow metrics are being logged correctly
- Check threshold value (0.85) in check_threshold.py

### Docker Build Fails
- Ensure Docker is available in the runner
- Check Dockerfile syntax
- Verify ARG RUN_ID is correctly passed

## Screenshots to Capture

### Failed Run:
1. Go to Actions tab
2. Click on the failed workflow run
3. Expand the "deploy" job
4. Scroll to "Check performance threshold" step
5. Screenshot showing: "❌ FAIL: Accuracy X.XX < threshold 0.85"

### Successful Run:
1. Go to Actions tab
2. Click on the successful workflow run
3. Expand the "deploy" job
4. Scroll to "Deployment Summary" step
5. Screenshot showing: "✅ Deployment successful!" and Run ID

## Key Files

- `.github/workflows/pipeline.yml` - Main workflow definition
- `train.py` - Model training script
- `check_threshold.py` - Performance validation script
- `Dockerfile` - Container image definition
- `requirements.txt` - Python dependencies

## Notes

- The pipeline uses RandomForest classifier for model training
- MLflow tracks accuracy, precision, recall, and F1 score
- Default threshold for deployment: 0.85 accuracy
- Docker build is simulated (echo command) in demo mode
- For production, replace echo with actual `docker build` and `docker push` commands
