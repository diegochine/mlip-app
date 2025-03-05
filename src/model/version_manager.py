# Used in Course 3
# This module gets deprecated in Course 4, once we introduce MLFlow

import os
import shutil
from datetime import datetime
from src.config import Config

def version_model():
    """
    Versions the current model by copying it to a versions directory with a timestamp.
    
    Returns:
        The path to the versioned model file.
    """
    model_path = Config.MODEL_PATH
    if not os.path.exists(model_path):
        raise Exception("No trained model found to version.")
    version_dir = os.path.join(os.path.dirname(model_path), "versions")
    os.makedirs(version_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_model_path = os.path.join(version_dir, f"model_{timestamp}.pkl")
    shutil.copy(model_path, new_model_path)
    return new_model_path
