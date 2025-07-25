<<<<<<< HEAD

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
        "feature_names": feature_names[:10] if hasattr(feature_names, '__len__') else []}
=======
"""
Lesotho Healthcare Cost Prediction API
FastAPI application for predicting healthcare costs based on demographic data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Literal
import pandas as pd
from datetime import datetime

# Import prediction functions
from prediction import predict_cost, model, scaler, feature_names, model_type

# Create FastAPI app
app = FastAPI(
    title="Lesotho Healthcare Cost Prediction API",
    description="Predicts healthcare costs for individuals in Lesotho based on demographic and socioeconomic factors",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PredictionInput(BaseModel):
    """Input model for healthcare cost prediction"""
    age: int = Field(..., ge=18, le=100, description="Age of the individual (18-100)")
    sex: Literal["male", "female"] = Field(..., description="Gender of the individual")
    region: Literal[
        "Quthing", "Thaba-Tseka", "Butha-Buthe", "Mafeteng", 
        "Mohale's Hoek", "Qacha's Nek", "Leribe", "Maseru"
    ] = Field(..., description="Region in Lesotho")
    is_insured: Literal[0, 1] = Field(..., description="Insurance status (0=No, 1=Yes)")
    employment: Literal["employed", "unemployed", "self-employed"] = Field(
        ..., description="Employment status"
    )
    household_size: int = Field(..., ge=1, le=15, description="Number of people in household")
    primary_healthcare_access: Literal["easy", "moderate", "difficult"] = Field(
        ..., description="Level of healthcare access difficulty"
    )
    annual_income: float = Field(
        ..., ge=5000.0, le=200000.0, description="Annual income in Lesotho Loti"
    )
    healthcare_type: Literal["public", "private"] = Field(
        ..., description="Type of healthcare system used"
    )
    
    @validator('annual_income')
    def validate_income(cls, v):
        """Ensure income is reasonable"""
        if v < 5000:
            raise ValueError('Annual income must be at least M5,000')
        if v > 200000:
            raise ValueError('Annual income cannot exceed M200,000')
        return v

class PredictionOutput(BaseModel):
    """Output model for healthcare cost prediction"""
    predicted_healthcare_cost: float = Field(..., description="Predicted cost in Lesotho Loti")
    model_used: str = Field(..., description="Type of model used for prediction")
    confidence_info: str = Field(..., description="Additional information about the prediction")
    timestamp: str = Field(..., description="Timestamp of prediction")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    model_status: str
    features_loaded: int
    timestamp: str

# API Endpoints
@app.get("/", tags=["General"])
def root():
    """Root endpoint with API information"""
    return {
        "message": "Lesotho Healthcare Cost Prediction API",
        "version": "1.0.0",
        "description": "Predict healthcare costs based on demographic and socioeconomic factors",
        "endpoints": {
            "/predict": "POST - Make a healthcare cost prediction",
            "/health": "GET - Check API and model health",
            "/model-info": "GET - Get information about the prediction model",
            "/docs": "GET - Swagger UI documentation",
            "/redoc": "GET - ReDoc documentation"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Check the health status of the API and model"""
    return HealthResponse(
        status="healthy" if model else "model_not_loaded",
        model_status="loaded" if model else "demo_mode",
        features_loaded=len(feature_names) if feature_names else 0,
        timestamp=datetime.now().isoformat()
    )

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict_healthcare_cost(input_data: PredictionInput):
    """
    Predict healthcare cost for an individual
    
    This endpoint takes demographic and socioeconomic information about an individual
    and returns a predicted healthcare cost in Lesotho Loti (M).
    """
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data.dict()])
        
        # Make prediction
        prediction = predict_cost(input_df)
        
        # Create confidence information
        confidence_info = f"Prediction based on {model_type}"
        if model is None:
            confidence_info += " (demo mode with realistic cost factors)"
        else:
            confidence_info += " trained on Lesotho healthcare data"
        
        # Add insurance note
        if input_data.is_insured == 1:
            confidence_info += ". Note: Insurance coverage may reduce actual out-of-pocket costs."
        
        # Add healthcare type note
        if input_data.healthcare_type == "private":
            confidence_info += " Private healthcare costs included."
        
        return PredictionOutput(
            predicted_healthcare_cost=round(float(prediction), 2),
            model_used=model_type if model else f"{model_type} (Demo Mode)",
            confidence_info=confidence_info,
            timestamp=datetime.now().isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info", tags=["Model"])
def get_model_info():
    """Get information about the prediction model"""
    return {
        "model_type": model_type,
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "features_count": len(feature_names) if feature_names else 0,
        "expected_features": [
            "age", "sex", "region", "is_insured", "employment",
            "household_size", "primary_healthcare_access", 
            "annual_income", "healthcare_type"
        ],
        "supported_regions": [
            "Quthing", "Thaba-Tseka", "Butha-Buthe", "Mafeteng",
            "Mohale's Hoek", "Qacha's Nek", "Leribe", "Maseru"
        ],
        "currency": "Lesotho Loti (M)",
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(404)
def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "available_endpoints": ["/", "/predict", "/health", "/model-info", "/docs"]}

@app.exception_handler(500)
def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "Please contact API administrator"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000, reload=True)
>>>>>>> 9a0b529987b4c48b33cccbc25ef423620ef58514
