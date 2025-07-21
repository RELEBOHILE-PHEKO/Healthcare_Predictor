from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
from typing import Literal
import os

# Initialize FastAPI app
app = FastAPI(
    title="Lesotho Healthcare Cost Prediction API",
    description="Predicts healthcare costs for individuals in Lesotho based on demographic and socioeconomic factors",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model and preprocessing components
try:
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler.pkl') 
    feature_names = joblib.load('feature_names.pkl')
    model_type = "Linear Regression"  # Update this based on your best model
except Exception as e:
    print(f"Error loading model: {e}")
    model, scaler, feature_names = None, None, None

# Define input data model with constraints
class PredictionInput(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Age in years (18-100)")
    sex: Literal["male", "female"] = Field(..., description="Gender")
    region: Literal[
        "Quthing", "Thaba-Tseka", "Butha-Buthe", "Mafeteng", 
        "Mohale's Hoek", "Qacha's Nek", "Leribe", "Maseru"
    ] = Field(..., description="Region in Lesotho")
    is_insured: Literal[0, 1] = Field(..., description="Insurance status (0=No, 1=Yes)")
    employment: Literal["employed", "unemployed", "self-employed"] = Field(..., description="Employment status")
    household_size: int = Field(..., ge=1, le=15, description="Number of people in household (1-15)")
    primary_healthcare_access: Literal["easy", "moderate", "difficult"] = Field(..., description="Access to primary healthcare")
    annual_income: float = Field(..., ge=5000.0, le=200000.0, description="Annual income in LSL (5,000 - 200,000)")
    healthcare_type: Literal["public", "private"] = Field(..., description="Type of healthcare facility")

    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "sex": "male",
                "region": "Maseru",
                "is_insured": 1,
                "employment": "employed",
                "household_size": 4,
                "primary_healthcare_access": "easy",
                "annual_income": 50000.0,
                "healthcare_type": "private"
            }
        }

# Define response model
class PredictionOutput(BaseModel):
    predicted_healthcare_cost: float = Field(..., description="Predicted healthcare cost in LSL")
    model_used: str = Field(..., description="Model used for prediction")
    confidence_info: str = Field(..., description="Additional information about the prediction")

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Lesotho Healthcare Cost Prediction API",
        "description": "API for predicting healthcare costs based on demographic and socioeconomic factors",
        "endpoints": {
            "/predict": "POST - Make a healthcare cost prediction",
            "/docs": "GET - API documentation (Swagger UI)",
            "/health": "GET - Health check"
        },
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not_loaded"
    return {
        "status": "healthy",
        "model_status": model_status,
        "features_loaded": len(feature_names) if feature_names else 0
    }

@app.post("/predict", response_model=PredictionOutput)
async def predict_healthcare_cost(input_data: PredictionInput):
    """
    Predict healthcare cost based on input features
    
    This endpoint takes demographic and socioeconomic information 
    and returns a predicted healthcare cost in Lesotho Loti (LSL).
    """
    
    if model is None or scaler is None or feature_names is None:
        raise HTTPException(
            status_code=500, 
            detail="Model not loaded. Please check server configuration."
        )
    
    try:
        # Convert input to DataFrame
        input_dict = input_data.dict()
        input_df = pd.DataFrame([input_dict])
        
        # Apply same categorical encoding as training
        categorical_columns = ['sex', 'region', 'employment', 'primary_healthcare_access', 'healthcare_type']
        input_encoded = pd.get_dummies(input_df, columns=categorical_columns, drop_first=True)
        
        # Ensure all training features are present
        input_encoded = input_encoded.reindex(columns=feature_names, fill_value=0)
        
        # Make prediction
        if model_type == "Linear Regression":
            input_scaled = scaler.transform(input_encoded)
            prediction = model.predict(input_scaled)[0]
        else:
            prediction = model.predict(input_encoded)[0]
        
        # Ensure prediction is positive and reasonable
        prediction = max(100.0, prediction)  # Minimum cost of 100 LSL
        
        # Prepare confidence information
        confidence_info = f"Prediction based on {model_type} trained on Lesotho healthcare data"
        if input_data.is_insured == 1:
            confidence_info += ". Insurance coverage may reduce actual out-of-pocket costs."
        
        return PredictionOutput(
            predicted_healthcare_cost=round(prediction, 2),
            model_used=model_type,
            confidence_info=confidence_info
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Prediction error: {str(e)}"
        )

@app.get("/model-info")
async def get_model_info():
    """Get information about the trained model"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    return {
        "model_type": model_type,
        "features_count": len(feature_names) if feature_names else 0,
        "feature_names": feature_names[:10] if feature_names else [],  # First 10 features
        "training_info": {
            "dataset": "Lesotho Healthcare Cost Dataset",
            "target": "Healthcare Cost (LSL)",
            "preprocessing": "StandardScaler for numerical features, One-hot encoding for categorical"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)