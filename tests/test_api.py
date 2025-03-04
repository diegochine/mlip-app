import pytest
from src.api.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_no_data(client):
    # When no JSON is provided, expect a 400 error.
    response = client.post('/predict', json={})
    assert response.status_code == 400

def test_predict_invalid_input(client):
    # When the 'features' key is missing, expect a 400 error.
    response = client.post('/predict', json={"invalid_key": []})
    assert response.status_code == 400

def test_retrain_endpoint(client):
    # Trigger the retraining endpoint and expect a successful response.
    response = client.post('/retrain')
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
