from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator  # For the no-drift branch and joining
from airflow.utils.dates import days_ago
import logging
import random

# Import training and evaluation routines
from src.model import train, evaluate
from src.data import data_loader, data_processor
from sklearn.model_selection import train_test_split

default_args = {
    'owner': 'mlip_app',
    'retries': 1,
}

def check_drift_signal() -> str:
    """
    Simulates a drift signal with a random chance.
    Branches the DAG execution based on the drift signal.
    Returns the task_id to proceed with.
    """
    drift_detected = random.random() < 0.2  # 20% probability
    if drift_detected:
        logging.info("Drift detected. Proceeding with retraining.")
        return "retrain_model"
    else:
        logging.info("No drift detected. Skipping retraining for this cycle.")
        return "no_drift"

def retrain_model():
    logging.info("Starting model retraining.")
    train.main()  # Train and save the new model
    logging.info("Model retraining completed.")

def evaluate_new_model():
    logging.info("Evaluating new model.")
    # Load and process the data (using the same logic as training)
    data = data_loader.load_data()
    data = data_processor.process_data(data)
    
    if 'target' not in data.columns:
        raise Exception("Data must contain a 'target' column for evaluation.")
    
    X = data.drop('target', axis=1)
    y = data['target']
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    accuracy = evaluate.evaluate_model(X_test, y_test)
    logging.info(f"New model evaluation accuracy: {accuracy:.4f}")
    
    # For demonstration, enforce a minimal accuracy threshold.
    if accuracy < 0.5:
        raise Exception("New model accuracy below threshold. Rolling back deployment.")
    return accuracy

def deploy_model():
    # In production, this step would update the running service.
    logging.info("Deploying new model.")
    logging.info("Model deployed successfully.")

with DAG(
    dag_id='model_retraining_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    description='Automated retraining pipeline for the MLIP App with conditional retraining based on drift detection',
) as dag:

    # Branch based on drift detection
    check_drift = BranchPythonOperator(
        task_id='check_drift_signal',
        python_callable=check_drift_signal
    )

    # Task to retrain the model if drift is detected
    task_retrain_model = PythonOperator(
        task_id='retrain_model',
        python_callable=retrain_model
    )

    # Task to evaluate the retrained model
    task_evaluate_model = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_new_model
    )

    # Task to deploy the new model
    task_deploy_model = PythonOperator(
        task_id='deploy_model',
        python_callable=deploy_model
    )

    # Dummy operator to act as the no-drift branch
    no_drift = DummyOperator(
        task_id='no_drift'
    )

    # Join branch to mark the end of the DAG run
    join = DummyOperator(
        task_id='join',
        trigger_rule='none_failed_min_one_success'
    )

    # Define the branching flow:
    # If drift is detected: retrain -> evaluate -> deploy -> join
    # If no drift: skip to join
    check_drift_signal >> [task_retrain_model, no_drift]
    task_retrain_model >> task_evaluate_model >> task_deploy_model >> join
    no_drift >> join
