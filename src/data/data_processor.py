import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def process_data(data):
    """
    Preprocesses the Telco Customer Churn dataset.
    
    Steps:
    - Drop columns that are not predictive.
    - Rename 'Churn Value' to 'target' for supervised learning.
    - One-hot encode categorical variables.
    - Scale numeric features.
    """
    # Drop columns that are not useful for training
    drop_cols = ["CustomerID", "Count", "Lat Long", "Latitude", "Longitude", "Churn Label", "Churn Reason"]
    data = data.drop(columns=[col for col in drop_cols if col in data.columns])
    
    # Rename target column if it exists
    if "Churn Value" in data.columns:
        data = data.rename(columns={"Churn Value": "target"})

    # Convert numeric columns to float and drop missing columns
    data['Monthly Charges'] = data['Monthly Charges'].apply(lambda s: s.replace(',', '.')).astype(np.float64)
    data['Total Charges'] = data['Total Charges'].apply(lambda s: s.replace(',', '.'))
    data = data[data['Total Charges'] != ' ']
    data['Total Charges'] = data['Total Charges'].astype(np.float64)
    
    # Separate features and target if available
    target = data["target"]
    X = data.drop(columns=["target"])

    # One-hot encode categorical variables (all non-numeric columns)
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_encoded)
    X_scaled = pd.DataFrame(X_scaled, columns=X_encoded.columns)
    
    # Reattach target column without scaling
    X_scaled["target"] = target.values
    return X_scaled
