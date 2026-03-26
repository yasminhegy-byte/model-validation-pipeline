# Quick Reference Guide

## Project Files Summary

### 📁 Directory Structure
```
assing5/
├── .github/workflows/
│   └── pipeline.yml                          # ⭐ MAIN WORKFLOW FILE (Submit This)
├── .dvc/
│   └── .gitignore                           # DVC configuration
├── data/
│   └── training_data.csv                    # Generated training data
├── .gitignore                               # Git ignore rules
├── check_threshold.py                       # ⭐ THRESHOLD VALIDATION SCRIPT
├── Dockerfile                               # ⭐ DOCKER DEFINITION FILE
├── train.py                                 # ⭐ MODEL TRAINING SCRIPT
├── requirements.txt                         # Python dependencies
├── README.md                                # Project overview
├── DEPLOYMENT_GUIDE.md                      # Setup instructions
├── IMPLEMENTATION_SUMMARY.md                # Technical documentation
└── TEST_EVIDENCE.md                         # Test results & evidence

⭐ = Required for submission
```

## Key Scripts

### train.py (Model Training)
```
INPUT:  None (generates synthetic data)
PROCESS:
  → Create training data (configurable via TRAIN_SEED env var)
  → Split into train/test (80/20)
  → Train RandomForest classifier
  → Log metrics to MLflow (accuracy, precision, recall, F1)
  → Save model to model.pkl
OUTPUT: model_info.txt containing MLflow Run ID
```

### check_threshold.py (Performance Validation)
```
INPUT:  model_info.txt (MLflow Run ID)
PROCESS:
  → Read Run ID from file
  → Query MLflow for accuracy metric
  → Compare accuracy against threshold (0.85)
OUTPUT: Exit code 0 if PASS, 1 if FAIL
```

### pipeline.yml (GitHub Actions Workflow)
```
TRIGGERS: Push to main/develop or PR to main

JOB 1: validate
  ├─ Checkout code
  ├─ Setup Python 3.10
  ├─ Install dependencies
  ├─ Generate training data
  ├─ Run train.py
  ├─ Export Run ID to model_info.txt
  └─ Upload artifact → model-info

JOB 2: deploy (depends on validate)
  ├─ Download artifact
  ├─ Run check_threshold.py
  ├─ On PASS:
  │  ├─ Build Docker image
  │  └─ Display deployment summary
  └─ On FAIL:
     └─ Exit with error (no Docker build)
```

## Test Scenarios

### Scenario 1: Failed Run (Accuracy < 0.85)
```bash
# Local test
python train.py                    # Uses default seed=42 → accuracy ≈ 0.70
python check_threshold.py          # Fails: 0.70 < 0.85 ❌
```

### Scenario 2: Successful Run (Accuracy >= 0.85)
```bash
# Local test
export TRAIN_SEED=99              # Use high-quality data
python train.py                    # seed=99 → accuracy ≈ 0.8750
python check_threshold.py          # Passes: 0.8750 >= 0.85 ✅
```

## GitHub Setup Checklist

- [ ] Create GitHub repository
- [ ] Push code with: `git push origin main`
- [ ] Go to Settings → Secrets → Add `MLFLOW_TRACKING_URI`
- [ ] Create two test runs (failed and successful)
- [ ] Capture screenshots of both deploy job outputs
- [ ] Submit files and screenshots

## Files to Submit

1. **`.github/workflows/pipeline.yml`** - Main workflow (155 lines)
2. **Screenshot of Failed Run** - Deploy job showing ❌ FAIL threshold
3. **Screenshot of Successful Run** - Deploy job showing ✅ PASS & deployment
4. **Supporting Files** (include in repository):
   - train.py
   - check_threshold.py
   - Dockerfile
   - requirements.txt
   - README.md

## Quick Commands

### Generate Failed Run Data
```bash
cd c:\Users\HORAS\Documents\assing5
python train.py                 # Accuracy: 0.70 ❌
python check_threshold.py       # Shows ❌ FAIL
```

### Generate Successful Run Data
```bash
cd c:\Users\HORAS\Documents\assing5
del data\training_data.csv      # Force regeneration
$env:TRAIN_SEED=99
python train.py                 # Accuracy: 0.8750 ✅
python check_threshold.py       # Shows ✅ PASS
```

### View MLflow Results
```bash
# See all metrics logged
cat mlruns/*/*/*/metrics.yaml
```

### Test Docker Build
```bash
docker build -t test:v1 --build-arg RUN_ID=test .
docker run --rm test:v1
```

## Default Configuration

| Setting | Value |
|---------|-------|
| Python Version | 3.10 |
| Model Type | RandomForestClassifier |
| Test Size | 20% of data |
| Accuracy Threshold | 0.85 |
| Failed Run Seed | 42 (accuracy ≈ 0.70) |
| Successful Run Seed | 99 (accuracy ≈ 0.875) |
| MLflow Backend | Local file store (./mlruns) |
| Docker Registry | None (mock build) |
| Artifact Retention | 7 days |

## Expected Output Examples

### For Failed Run
```
Using local MLflow backend: file:./mlruns
Read Run ID: abb2db1bd3e14e51b241a668d0f4cbbb
Model Accuracy: 0.7000
❌ FAIL: Accuracy 0.7000 < threshold 0.85
```

### For Successful Run
```
Using local MLflow backend: file:./mlruns
Read Run ID: 474788f65d904221a04be02eb01d8a26
Model Accuracy: 0.8750
✅ PASS: Accuracy 0.8750 >= threshold 0.85
```

## Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| MLflow connection refused | Use local backend (default in script) |
| model_info.txt not found | Run train.py first to generate it |
| Docker build fails | Skip if Docker not installed (demo mode) |
| Python import errors | Install: `pip install -r requirements.txt` |
| Wrong accuracy value | Check TRAIN_SEED environment variable |

## File Sizes

| File | Size | Lines |
|------|------|-------|
| pipeline.yml | ~6KB | 155 |
| train.py | ~4KB | 101 |
| check_threshold.py | ~2KB | 58 |
| Dockerfile | ~1KB | 35 |
| requirements.txt | ~0.2KB | 6 |
| Total Core Files | ~13KB | 355 |

## GitHub Actions Features Used

✅ **Jobs**: Multiple dependent jobs with `needs:`
✅ **Artifacts**: Upload/Download between jobs
✅ **Environment Variables**: Secrets and expressions
✅ **Actions**: checkout@v4, setup-python@v4, upload/download-artifact@v4
✅ **Conditions**: `if: success()` conditional steps
✅ **Outputs**: Job outputs passed between steps
✅ **Triggers**: Push, Pull Request on specific branches

## Customization Points

To modify the pipeline:

1. **Change Threshold**: Edit `check_threshold.py` line ~40
2. **Change Model**: Edit `train.py` Random Forest or replace with different model
3. **Add Metrics**: Edit `train.py` to log additional metrics
4. **Change Seed**: Set `TRAIN_SEED` environment variable in workflow
5. **Enable Docker Push**: Replace echo with `docker push` in workflow
6. **Add Notifications**: Add Slack/Teams step in deploy job

---

**Quick Access to Main Files**:
- Workflow: `.github/workflows/pipeline.yml`
- Training: `train.py`
- Validation: `check_threshold.py`
- Docker: `Dockerfile`
