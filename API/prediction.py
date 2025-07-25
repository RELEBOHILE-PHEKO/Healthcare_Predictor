"""
Healthcare Cost Prediction Module
Handles the prediction logic for the Lesotho Healthcare Cost API
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Global variables for model components
model = None
scaler = None
feature_names = None
label_encoders = None
model_type = "Linear Regression"

def load_model_components():
    """Load the trained model and preprocessing components"""
    global model, scaler, feature_names, label_encoders
    
    try:
        # Adjust paths based on your file structure
        model = joblib.load('models/linear_regression_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')
        print("Model components loaded successfully")
    except FileNotFoundError as e:
        print(f"Model files not found: {e}")
        print("Using demo prediction function")
        # Set default feature names for demo
        feature_names = ['age', 'sex', 'region', 'is_insured', 'employment', 
                        'household_size', 'primary_healthcare_access', 
                        'annual_income', 'healthcare_type']

def predict_cost(input_df):
    """
    Main prediction function that handles both real model and demo mode
    
    Args:
        input_df: DataFrame with input features
        
    Returns:
        float: Predicted healthcare cost
    """
    if model is not None and scaler is not None:
        return predict_with_model(input_df)
    else:
        return predict_demo(input_df)

def predict_with_model(input_df):
    """
    Predict using the trained model
    
    Args:
        input_df: DataFrame with input features
        
    Returns:
        float: Predicted healthcare cost
    """
    # Make a copy to avoid modifying original data
    df = input_df.copy()
    
    # Encode categorical variables
    categorical_columns = ['sex', 'region', 'employment', 'primary_healthcare_access', 'healthcare_type']
    
    for col in categorical_columns:
        if col in df.columns and col in label_encoders:
            df[col] = label_encoders[col].transform(df[col])
    
    # Ensure all features are in the correct order
    df = df[feature_names]
    
    # Scale the features
    df_scaled = scaler.transform(df)
    
    # Make prediction
    prediction = model.predict(df_scaled)
    
    return float(prediction[0])

def predict_demo(input_df):
    """
    Demo prediction function with realistic cost calculations
    This ensures different inputs produce different outputs
    
    Args:
        input_df: DataFrame with input features
        
    Returns:
        float: Predicted healthcare cost
    """
    df = input_df.iloc[0]  # Get first row as Series
    
    # Base cost in Lesotho Loti (M)
    base_cost = 5000
    
    # Age factor: older people generally have higher healthcare costs
    age_factor = (df['age'] - 18) * 75
    
    # Insurance factor: insured people have lower out-of-pocket costs
    insurance_factor = -2500 if df['is_insured'] == 1 else 2000
    
    # Income factor: higher income correlates with private healthcare usage
    income_factor = (df['annual_income'] / 60000) * 1500
    
    # Household size factor: larger households may share costs
    household_factor = -(df['household_size'] - 1) * 300
    
    # Healthcare access factor
    access_factors = {
        'easy': -800,      # Easy access = lower costs
        'moderate': 200,   # Moderate access = slightly higher
        'difficult': 1500  # Difficult access = much higher costs
    }
    access_factor = access_factors.get(df['primary_healthcare_access'], 0)
    
    # Healthcare type factor: private is more expensive
    type_factor = 4000 if df['healthcare_type'] == 'private' else 0
    
    # Employment factor
    employment_factors = {
        'employed': 0,        # Baseline
        'unemployed': 1200,   # Higher costs due to delayed care
        'self-employed': 600  # Moderate increase
    }
    employment_factor = employment_factors.get(df['employment'], 0)
    
    # Regional factor: some regions have higher costs
    region_factors = {
        'Maseru': 1500,        # Capital city - highest costs
        'Leribe': 800,         # Urban area
        'Mafeteng': 500,       # Semi-urban
        'Butha-Buthe': 300,    # Rural but accessible
        'Mohale\'s Hoek': 200, # Rural
        'Quthing': 0,          # Baseline rural
        'Qacha\'s Nek': -300,  # Remote, lower facility costs
        'Thaba-Tseka': -500    # Most remote
    }
    region_factor = region_factors.get(df['region'], 0)
    
    # Sex factor: slight difference due to different healthcare needs
    sex_factor = 300 if df['sex'] == 'female' else 0
    
    # Calculate total predicted cost
    total_cost = (base_cost + age_factor + insurance_factor + income_factor + 
                 household_factor + access_factor + type_factor + employment_factor + 
                 region_factor + sex_factor)
    
    # Add small random variation for realism (±5%)
    variation = np.random.uniform(-0.05, 0.05) * total_cost
    total_cost += variation
    
    # Ensure minimum cost
    total_cost = max(total_cost, 1000)
    
    return round(total_cost, 2)

# Load model components when module is imported
load_model_components()
