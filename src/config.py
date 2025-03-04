import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present.
load_dotenv()

class Config:
    # Basic configuration settings for reproducibility and security
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    
    # Paths for model and data (computed relative to this file)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "model", "saved_model.pkl")
    DATA_PATH = os.path.join(BASE_DIR, "data", "data.csv")
