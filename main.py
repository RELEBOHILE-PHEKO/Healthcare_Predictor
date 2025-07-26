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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import prediction functions - adjust path based on your file structure
try:
    from API.prediction import predict_cost, model, scaler, feature_names, model_type
    logger.info("Successfully imported from API.prediction")
except ImportError:
    try:
        from prediction import predict_cost, model, scaler, feature_names, model_type
        logger.info("Successfully imported from prediction")
    except ImportError as e:
        logger.error(f"Failed to import prediction module: {e}")
        # Set default values for demo mode
        predict_cost = None
        model = None
        scaler = None
        feature_names = []
        model_type = "Random Forest (Demo Mode)"

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
    allow_methods=["GET", "POST"],
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

# Demo prediction function (fallback if model not loaded)
def demo_predict_cost(input_df):
    """Demo prediction function using realistic healthcare cost factors"""
    row = input_df.iloc[0]
    
    # Base cost factors
    base_cost = 2000
    age_factor = (row['age'] - 18) * 15
    income_factor = row['annual_income'] * 0.05
    
    # Regional factors
    regional_multipliers = {
        "Maseru": 1.3, "Leribe": 1.1, "Mafeteng": 1.0, "Butha-Buthe": 0.9,
        "Mohale's Hoek": 0.95, "Quthing": 0.85, "Qacha's Nek": 0.8, "Thaba-Tseka": 0.75
    }
    regional_factor = regional_multipliers.get(row['region'], 1.0)
    
    # Other factors
    insurance_discount = 0.7 if row['is_insured'] == 1 else 1.0
    private_premium = 1.4 if row['healthcare_type'] == 'private' else 1.0
    access_factor = {'easy': 0.9, 'moderate': 1.0, 'difficult': 1.2}.get(row['primary_healthcare_access'], 1.0)
    household_factor = max(0.8, 1.0 - (row['household_size'] - 1) * 0.02)
    
    # Calculate final cost
    predicted_cost = (base_cost + age_factor + income_factor) * regional_factor * insurance_discount * private_premium * access_factor * household_factor
    
    return max(500, predicted_cost)  # Minimum cost of M500

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
        status="healthy",
        model_status="loaded" if model else "demo_mode",
        features_loaded=len(feature_names) if feature_names else 9,
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
        if predict_cost and model:
            prediction = predict_cost(input_df)
            confidence_info = f"Prediction based on {model_type} trained on Lesotho healthcare data"
        else:
            prediction = demo_predict_cost(input_df)
            confidence_info = f"Prediction based on {model_type} using realistic cost factors"
        
        # Add insurance note
        if input_data.is_insured == 1:
            confidence_info += ". Insurance coverage may reduce actual out-of-pocket costs."
        
        # Add healthcare type note
        if input_data.healthcare_type == "private":
            confidence_info += " Private healthcare costs included."
        
        return PredictionOutput(
            predicted_healthcare_cost=round(float(prediction), 2),
            model_used=model_type,
            confidence_info=confidence_info,
            timestamp=datetime.now().isoformat()
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info", tags=["Model"])
def get_model_info():
    """Get information about the prediction model"""
    return {
        "model_type": model_type,
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "features_count": len(feature_names) if feature_names else 9,
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
        "model_performance": {
            "test_r2": 0.9750,
            "test_mae": 202.69,
            "model_type": "Random Forest"
        } if model else "Demo mode - no model performance data",
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found", 
        "available_endpoints": ["/", "/predict", "/health", "/model-info", "/docs"]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error", 
        "message": "Please contact API administrator"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Lesotho Healthcare Cost Prediction API")
    logger.info(f"Model loaded: {model is not None}")
    logger.info(f"Scaler loaded: {scaler is not None}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=10000, 
        reload=False,  # Set to False for production
        log_level="info"
    )
