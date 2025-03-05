import os
import base64
from flask import Blueprint, request, jsonify
import requests
from src.config import Config

api_bp = Blueprint('api', __name__)

def load_model():
    model_path = Config.MODEL_PATH
    if not os.path.exists(model_path):
        raise Exception("Model not found. Please train the model first.")
    import pickle
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Expecting input features under the key 'features'
        features = data.get("features")
        if features is None:
            return jsonify({"error": "Missing 'features' key in input data"}), 400
        
        # Wrap single prediction input into a list if needed
        if not isinstance(features[0], list):
            features = [features]
        
        model = load_model()
        predictions = model.predict(features)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/retrain', methods=['POST'])
def retrain():
    try:
        # Airflow REST API endpoint for triggering a DAG run
        airflow_url = "http://airflow-webserver:8080/api/v1/dags/retraining_pipeline/dagRuns"
        
        # Retrieve Airflow credentials from environment variables
        username = os.environ.get("AIRFLOW_USERNAME", "airflow")
        password = os.environ.get("AIRFLOW_PASSWORD", "airflow")
        
        # Create a Basic Auth header
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        # Payload for the DAG run, adjust if necessary
        payload = {"conf": {}}
        
        response = requests.post(airflow_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return jsonify({"message": "Retraining pipeline triggered successfully via Airflow API."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

