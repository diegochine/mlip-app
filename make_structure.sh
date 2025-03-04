#!/bin/bash

# Define the project structure
dirs=(
    "mlip-app/src"
    "mlip-app/src/data"
    "mlip-app/src/model"
    "mlip-app/src/api"
    "mlip-app/src/monitoring"
    "mlip-app/tests"
    "mlip-app/airflow/dags"
    "mlip-app/kubernetes"
    "mlip-app/ci"
    "mlip-app/docker"
    "mlip-app/configs"
    "mlip-app/configs/grafana"
)

files=(
    "mlip-app/src/__init__.py"
    "mlip-app/src/config.py"
    "mlip-app/src/data/__init__.py"
    "mlip-app/src/data/data_loader.py"
    "mlip-app/src/data/data_processor.py"
    "mlip-app/src/model/__init__.py"
    "mlip-app/src/model/model.py"
    "mlip-app/src/model/train.py"
    "mlip-app/src/model/evaluate.py"
    "mlip-app/src/api/__init__.py"
    "mlip-app/src/api/app.py"
    "mlip-app/src/api/routes.py"
    "mlip-app/src/api/middleware.py"
    "mlip-app/src/api/utils.py"
    "mlip-app/src/monitoring/__init__.py"
    "mlip-app/src/monitoring/logging_config.py"
    "mlip-app/src/monitoring/metrics.py"
    "mlip-app/src/monitoring/drift_detector.py"
    "mlip-app/tests/__init__.py"
    "mlip-app/tests/test_data.py"
    "mlip-app/tests/test_model.py"
    "mlip-app/tests/test_api.py"
    "mlip-app/tests/test_monitoring.py"
    "mlip-app/airflow/dags/model_retraining_dag.py"
    "mlip-app/kubernetes/deployment.yaml"
    "mlip-app/kubernetes/service.yaml"
    "mlip-app/kubernetes/ingress.yaml"
    "mlip-app/kubernetes/hpa.yaml"
    "mlip-app/ci/Jenkinsfile"
    "mlip-app/docker/Dockerfile"
    "mlip-app/docker/Dockerfile.airflow"
    "mlip-app/configs/prometheus.yml"
    "mlip-app/configs/grafana/datasource.yml"
    "mlip-app/configs/grafana/dashboard.json"
    "mlip-app/requirements.txt"
    "mlip-app/setup.py"
    "mlip-app/README.md"
    "mlip-app/.env.example"
)

# Create directories
for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
done

# Create files
for file in "${files[@]}"; do
    touch "$file"
done

echo "Project structure created successfully!"

