import pandas as pd
import os

def load_data(file_path=None):
    """
    Loads data from a CSV file.
    If no file_path is provided, uses a default path relative to this module.
    """
    if file_path is None:
        # Default file path for sample data (ensure you provide 'sample_data.csv' in the same folder)
        file_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    try:
        data = pd.read_csv(file_path, delimiter=';')
    except Exception as e:
        raise Exception(f"Failed to load data from {file_path}: {e}")
    return data
