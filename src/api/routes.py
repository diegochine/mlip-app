from flask import Blueprint, request, jsonify
import os
import pickle
from src.config import Config

api_bp = Blueprint('api', __name__)

def load_model():
    model_path = Config.MODEL_PATH
    if not os.path.exists(model_path):
        raise Exception("Model not found. Please train the model first.")
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
