import joblib
import pandas as pd
import numpy as np

# Load model components
try:
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl') 
    feature_names = joblib.load('feature_names.pkl')
    model_type = "Linear Regression"
except Exception as e:
    print(f"Error loading model: {e}")
    model, scaler, feature_names = None, None, None

def predict_cost(input_df):
    # Categorical encoding
    categorical_columns = ['sex', 'region', 'employment', 'primary_healthcare_access', 'healthcare_type']
    input_encoded = pd.get_dummies(input_df, columns=categorical_columns, drop_first=True)
    
    # Align with training features
    input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)

    # Predict
    if model_type == "Linear Regression":
        input_scaled = scaler.transform(input_encoded)
        prediction = model.predict(input_scaled)[0]
    else:
        prediction = model.predict(input_encoded)[0]

    return max(100.0, prediction)  # Ensure minimum cost
