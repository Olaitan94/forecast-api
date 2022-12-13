from typing import Generator

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.main import app


#This fixture will be used to provide argument value to the prediction test
@pytest.fixture()
def desired_forecast():
    return 180


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as _client:
        yield _client
        app.dependency_overrides = {}
