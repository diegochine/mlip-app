import os
import pickle
from src.config import Config

def load_model():
    model_path = Config.MODEL_PATH
    if not os.path.exists(model_path):
        raise Exception("Model file not found.")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model
