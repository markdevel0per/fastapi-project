import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_submit_city():
    response = client.post('/submit', data={"user_input": "London"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_weather():
    response = client.get('/weather/London')
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_my_history():
    response = client.get('/history')
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
