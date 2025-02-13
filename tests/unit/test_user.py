from flask import url_for
from app import create_app



def test_login_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Login" in response.data