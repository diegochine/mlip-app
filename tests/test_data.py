import os
import pandas as pd
import tempfile
from src.data import data_loader

def test_load_data_success():
    # Create a temporary CSV file with sample data
    sample_data = "feature1,feature2,target\n1,2,0\n3,4,1"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".csv") as temp_csv:
        temp_csv.write(sample_data)
        temp_csv_path = temp_csv.name

    try:
        data = data_loader.load_data(temp_csv_path)
        # Check that the DataFrame is not empty and has the correct columns
        assert not data.empty
        assert set(data.columns) == {"feature1", "feature2", "target"}
    finally:
        os.remove(temp_csv_path)
