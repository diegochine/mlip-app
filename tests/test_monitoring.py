import numpy as np
import pytest
from src.monitoring import drift_detector

def test_calculate_psi_no_drift():
    # Generate identical distributions to check that PSI is near zero
    expected = np.random.normal(0, 1, 1000)
    actual = expected.copy()
    psi_value = drift_detector.calculate_psi(expected, actual)
    assert psi_value < 0.05

def test_detect_drift():
    # Generate distributions with a shift to simulate drift
    expected = np.random.normal(0, 1, 1000)
    actual = np.random.normal(0.5, 1.5, 1000)
    drift_detected, _ = drift_detector.detect_drift(expected, actual)
    assert drift_detected

from src.api.app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_metrics_endpoint(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    # Check that the Prometheus metric name is in the response
    assert b"app_requests_total" in response.data
