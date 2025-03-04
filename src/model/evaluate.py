import pickle
from sklearn.metrics import accuracy_score
from src.config import Config

def evaluate_model(X_test, y_test):
    # Load the saved model
    with open(Config.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

if __name__ == "__main__":
    # Evaluate the model on test data (assuming similar preprocessing as training)
    from sklearn.model_selection import train_test_split
    from src.data import data_loader, data_processor
    
    data = data_loader.load_data(Config.DATA_PATH)
    data = data_processor.process_data(data)
    
    if 'target' not in data.columns:
        raise Exception("Data must contain a 'target' column.")
        
    X = data.drop('target', axis=1)
    y = data['target']
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    acc = evaluate_model(X_test, y_test)
    print(f"Model accuracy: {acc}")
