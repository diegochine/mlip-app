import os
from sklearn.model_selection import train_test_split
from src.model import model as smodel
from src.data import data_loader, data_processor
from src.config import Config

def main():
    # Load and preprocess the data using the configured data path
    data = data_loader.load_data(Config.DATA_PATH)
    data = data_processor.process_data(data)
    
    # Expecting a 'target' column in the data for supervised learning
    if 'target' not in data.columns:
        raise Exception("Data must contain a 'target' column.")
    
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split the data into training and testing sets
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    simple_model = smodel.SimpleModel()
    simple_model.train(X_train, y_train)
    
    # Ensure the directory exists before saving the model
    os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)
    simple_model.save(Config.MODEL_PATH)
    
    print(f"Model trained and saved to {Config.MODEL_PATH}")

if __name__ == "__main__":
    main()
