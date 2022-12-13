import math

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, desired_forecast: int) -> None:
    # Given
    payload = {
        "inputs": desired_forecast
    }

    # When
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Then
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["forecast_prices"]
    assert prediction_data["forecast_dates"]
    assert prediction_data["errors"] is None
    assert math.isclose(prediction_data["forecast_prices"][0], 0.732185, abs_tol=0.01)
