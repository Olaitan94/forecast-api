#This file contains code for the API's functionalities: health & predict
#APIrouter is used to create path operations for this two functionalities
#This APIrouter will then be included in the main API

import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
#from fastapi.encoders import jsonable_encoder
from loguru import logger
from forecast_model import __version__ as model_version
from forecast_model.forecast import get_forecast

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

#path operation to get the health metrics of the model& API
#we define the path for the end point as "/health"
#we define that the response format should follow the schema in schemas.health
#Then we write for the function for this path operation
#it doesnt take in any input parameters
#Once the function is called, it returns a dictionary with the health metrics
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()

#path operation for to get the forecast from the ML model
#we define the path for the end point as "/predict"
#we define that the response format should follow the schema in schemas.PredictionResults
#Then we write for the function for this path operation
#it takes one input - which should be an integer as defined in the schema
#Once the function is called, it returns the forecast dates, prices, any errors & the model version
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.ModelInputs) -> Any:
    """
    Make CAD-USD exchange price forecast with the forecast model
    """

    forecast_period = input_data.inputs

    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = get_forecast(forecast_period = forecast_period)

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Forecast Prices: {results.get('forecast_prices')}\n Forecast Dates: {results.get('forecast_dates')} ")

    return results
