import pytest
import json
from utils import jwt_decode


class TestAuthentication:

    def test_register_new_user(self, client):
        response = client.post(
            "/login/register",
            json={"username": "Lucas", "email": "mymail@email.com", "password": "1234"},
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "data" in response_data
        auth_token = response_data.get("data")
        assert "token" in auth_token
        assert jwt_decode(auth_token["token"])

    def test_not_register_user_with_same_email(self, client):
        response = client.post(
            "/login/register",
            json={
                "username": "Rodrigo",
                "email": "mymail@email.com",
                "password": "4321",
            },
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 409
        assert "error" in response_data
        assert "User email already exists." in response_data["error"]

    def test_login_user(self, client):
        response = client.post(
            "/login", json={"email": "mymail@email.com", "password": "1234"}
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "data" in response_data
        auth_token = response_data.get("data")
        assert "token" in auth_token
        assert jwt_decode(auth_token["token"])

    def test_invalid_password_login_user(self, client):
        response = client.post(
            "/login", json={"email": "mymail@email.com", "password": "wrongpassword"}
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 403
        assert "error" in response_data
        assert "Invalid password" in response_data["error"]

    def test_invalid_email_login_user(self, client):
        response = client.post(
            "/login", json={"email": "wrongemail@email.com", "password": "1234"}
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert "error" in response_data
        assert "User not found" in response_data["error"]

    def test_unauthorized_request(self, client):
        response = client.post(
            "/api/customers", json={"name": "Lucas", "email": "mymail@email.com"}
        )
        response_data = json.loads(response.data.decode("utf-8"))

        print(response_data)

        assert response.status_code == 403
        assert "error" in response_data
        assert "Login required for insert operation" in response_data["error"]
