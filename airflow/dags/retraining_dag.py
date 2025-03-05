from datetime import datetime, timedelta
import logging

from airflow.decorators import dag, task

# Import pipeline functions
from src.model import pipeline, version_manager

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2025, 3, 1),
    catchup=False,
    tags=["retraining"],
)
def retraining_pipeline():
    
    @task
    def load_and_split_data():
        X_train, X_test, y_train, y_test = pipeline.load_and_split_data()
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

    @task
    def train_model(data: dict):
        model_path = pipeline.train_model_pipeline(data["X_train"], data["y_train"])
        logging.info(f"Model trained and saved to {model_path}.")
        return model_path

    @task
    def evaluate_model(data: dict) -> float:
        accuracy = pipeline.evaluate_model_pipeline(data["X_test"], data["y_test"])
        logging.info(f"Model evaluation accuracy: {accuracy}.")
        return accuracy

    @task
    def validate_and_version(accuracy: float):
        threshold = 0.7  # Example threshold for production readiness
        if accuracy >= threshold:
            new_model_path = version_manager.version_model()
            logging.info(f"Model passed validation and versioned: {new_model_path}.")
            return new_model_path
        else:
            logging.warning(f"Model accuracy {accuracy} did not meet threshold for versioning.")
            return None

    # Orchestrate the pipeline
    data = load_and_split_data()
    _ = train_model(data)
    accuracy = evaluate_model(data)
    versioned_model_path = validate_and_version(accuracy)
    return versioned_model_path

dag = retraining_pipeline()
