from sklearn.model_selection import train_test_split
from src.data import data_loader, data_processor
from src.model import model as smodel
from src.model import evaluate
from src.config import Config

def load_and_split_data(test_size=0.2, random_state=42):
    """
    Loads data, preprocesses it, and splits it into training and testing sets.
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    data = data_loader.load_data(Config.DATA_PATH)
    data = data_processor.process_data(data)
    if 'target' not in data.columns:
        raise Exception("Data must contain a 'target' column.")
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def train_model_pipeline(X_train, y_train):
    """
    Trains the model using the provided training data and saves it.
    
    Returns:
        The path to the saved model.
    """
    model = smodel.SimpleModel()
    model.train(X_train, y_train)
    import os
    os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)
    model.save(Config.MODEL_PATH)
    return Config.MODEL_PATH

def evaluate_model_pipeline(X_test, y_test):
    """
    Evaluates the saved model on the test data.
    
    Returns:
        Accuracy score.
    """
    accuracy = evaluate.evaluate_model(X_test, y_test)
    return accuracy
