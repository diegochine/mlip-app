import os
import mlflow
from sklearn.model_selection import train_test_split
from src.model import model as smodel
from src.data import data_loader, data_processor
from src.config import Config
from sklearn.metrics import accuracy_score

def main():
    # Load and preprocess the data using the configured data path
    data = data_loader.load_data(Config.DATA_PATH)
    data = data_processor.process_data(data)
    
    # Ensure the 'target' column is present for supervised learning
    if 'target' not in data.columns:
        raise Exception("Data must contain a 'target' column.")
    
    # Separate features and target
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Set the MLflow experiment
    mlflow.set_experiment("MLIP_Production_Deployment")
    with mlflow.start_run():
        # Log basic parameters
        mlflow.log_param("num_samples", len(X_train))
        mlflow.log_param("num_features", X_train.shape[1])
        
        # Initialize and train the model
        simple_model = smodel.SimpleModel()
        simple_model.train(X_train, y_train)
        
        # Evaluate the model on the validation set
        val_preds = simple_model.predict(X_val)
        accuracy = accuracy_score(y_val, val_preds)
        mlflow.log_metric("validation_accuracy", accuracy)
        
        # Ensure the directory exists before saving the model
        os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)
        simple_model.save(Config.MODEL_PATH)
        
        # Log the model artifact
        mlflow.log_artifact(Config.MODEL_PATH, artifact_path="model")
        
        print(f"Model trained with validation accuracy: {accuracy:.4f} and saved to {Config.MODEL_PATH}")

if __name__ == "__main__":
    main()
