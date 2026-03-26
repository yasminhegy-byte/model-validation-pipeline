FROM python:3.10-slim

# Accept build argument for Run ID
ARG RUN_ID
ENV RUN_ID=${RUN_ID}

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    mlflow \
    scikit-learn \
    joblib \
    pandas \
    numpy

# Copy model artifacts (in a real scenario, these would be downloaded from MLflow)
COPY model.pkl /app/model.pkl || true

# Copy application code
COPY . /app/

# Create a script to demonstrate model usage
RUN echo '#!/usr/bin/env python\n\
import os\n\
import sys\n\
print("=" * 60)\n\
print("Model Deployment Container")\n\
print("=" * 60)\n\
print(f"Run ID: {os.environ.get(\"RUN_ID\", \"unknown\")}")\n\
print("Status: Model ready for inference")\n\
print("=" * 60)\n\
' > /app/serve.py

# Default command
CMD ["python", "-c", "import os; print(f\"Container started with Run ID: {os.environ.get(\\\"RUN_ID\\\")}\"); print(\"Model is ready to serve predictions.\")"]
