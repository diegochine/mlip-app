import os
from sklearn.datasets import make_classification
from src.model import model as smodel

# TODO: improve tests

def test_model_training_and_saving():
    # Create synthetic data for testing
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    simple_model = smodel.SimpleModel()
    simple_model.train(X, y)
    
    # Save the model to a temporary file and check existence
    temp_model_path = "temp_model.pkl"
    simple_model.save(temp_model_path)
    assert os.path.exists(temp_model_path)
    
    # Cleanup
    os.remove(temp_model_path)
