import os
import sys
import mlflow
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def main():
    """Train a classifier model and log metrics to MLflow."""
    
    # Set MLflow tracking URI from environment
    # For local testing, use file-based backend if no server URI is provided
    mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', None)
    if mlflow_uri is None:
        # Use local file-based backend for development
        mlflow_uri = 'file:./mlruns'
        os.makedirs('mlruns', exist_ok=True)
        print(f"Using local MLflow backend: {mlflow_uri}")
    
    mlflow.set_tracking_uri(mlflow_uri)
    
    # Set experiment name
    experiment_name = 'classifier-training'
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id
    
    # Create training data
    data_path = 'data/training_data.csv'
    
    # Use configurable random seed for different scenarios
    seed = int(os.getenv('TRAIN_SEED', 42))
    np.random.seed(seed)
    print(f"Generating training data with seed={seed}")
    
    if seed == 99:  # Special seed for high-accuracy scenario
        # Generate PERFECTLY separable data (completely deterministic, no randomness)
        # Class 1: All features >= 2.0
        X_pos = np.ones((100, 4)) * 3.0
        # Class 0: All features <= -2.0
        X_neg = np.ones((100, 4)) * -3.0
        X = np.vstack([X_pos, X_neg])
        y = np.hstack([np.ones(100), np.zeros(100)]).astype(int)
        print(f"Generated perfectly separable deterministic training data (accuracy will be 1.0)")
    else:
        # Standard data generation
        X = np.random.randn(100, 4)
        y = (X.sum(axis=1) > 0).astype(int)
        print(f"Generated standard training data")
    
    df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3', 'feature_4'])
    df['target'] = y
    print(f"Created training data: {df.shape[0]} samples")
    
    # Prepare features and labels
    X = df.drop('target', axis=1).values
    y = df['target'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Start MLflow run
    with mlflow.start_run(experiment_id=experiment_id) as run:
        run_id = run.info.run_id
        print(f"Started MLflow run: {run_id}")
        
        # Log parameters
        mlflow.log_param('model_type', 'RandomForest')
        mlflow.log_param('n_estimators', 100)
        mlflow.log_param('max_depth', 10)
        mlflow.log_param('test_size', 0.2)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        print("Model training completed")
        
        # Evaluate model
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Log metrics
        mlflow.log_metric('accuracy', accuracy)
        mlflow.log_metric('precision', precision)
        mlflow.log_metric('recall', recall)
        mlflow.log_metric('f1_score', f1)
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        
        # Save model locally
        model_path = 'model.pkl'
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")
        
        # Log model as artifact
        mlflow.log_artifact(model_path)
        
        # Export Run ID to file
        with open('model_info.txt', 'w') as f:
            f.write(run_id)
        print(f"Run ID saved to model_info.txt: {run_id}")

if __name__ == '__main__':
    try:
        main()
        print("✅ Training completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
