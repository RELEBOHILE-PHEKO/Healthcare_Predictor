from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd

from API.prediction import predict_cost, model, scaler, feature_names, model_type

app = FastAPI(
    title="Lesotho Healthcare Cost Prediction API",
    description="Predicts healthcare costs for individuals in Lesotho based on demographic and socioeconomic factors",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    sex: Literal["male", "female"]
    region: Literal["Quthing", "Thaba-Tseka", "Butha-Buthe", "Mafeteng", 
                    "Mohale's Hoek", "Qacha's Nek", "Leribe", "Maseru"]
    is_insured: Literal[0, 1]
    employment: Literal["employed", "unemployed", "self-employed"]
    household_size: int = Field(..., ge=1, le=15)
    primary_healthcare_access: Literal["easy", "moderate", "difficult"]
    annual_income: float = Field(..., ge=5000.0, le=200000.0)
    healthcare_type: Literal["public", "private"]

class PredictionOutput(BaseModel):
    predicted_healthcare_cost: float
    model_used: str
    confidence_info: str

@app.get("/")
def root():
    return {
        "message": "Lesotho Healthcare Cost Prediction API",
        "endpoints": {
            "/predict": "POST - Make a prediction",
            "/docs": "GET - Swagger UI",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model else "model_not_loaded",
        "model_status": "loaded" if model else "not_loaded",
        "features_loaded": len(feature_names) if feature_names else 0
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    if model is None or scaler is None or feature_names is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        input_df = pd.DataFrame([input_data.dict()])
        prediction = predict_cost(input_df)

        confidence_info = f"Prediction based on {model_type} trained on Lesotho healthcare data"
        if input_data.is_insured == 1:
            confidence_info += ". Insurance coverage may reduce actual out-of-pocket costs."

        return PredictionOutput(
            predicted_healthcare_cost=round(prediction, 2),
            model_used=model_type,
            confidence_info=confidence_info
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

@app.get("/model-info")
def model_info():
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {
        "model_type": model_type,
        "features_count": len(feature_names),
        "feature_names": feature_names[:10] if hasattr(feature_names, '__len__') else [],
    }