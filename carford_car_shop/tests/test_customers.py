import pytest
import json


class TestCustomer:

    def test_get_all_customers_route(self, client):
        response = client.get("/api/customers")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "customers" in response_data
        assert len(response_data["customers"]) > 0
        customers = response_data["customers"]
        for customer in customers:
            assert "id" in customer
            assert "name" in customer
            assert "cars" in customer

    def test_get_customer_by_id_route(self, client):
        response = client.get("/api/customers/1")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "customers" in response_data
        customer = response_data["customers"]
        assert customer["id"] == 1
        assert "cars" in customer

    def test_add_customer_route(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.post(
            "/api/customers",
            headers=header,
            json={"name": "Lucas", "email": "mymail@email.com"},
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "message" in response_data
        assert "Customer added" in response_data["message"]

    def test_remove_customer_route(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.delete("/api/customers/5", headers=header)
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "message" in response_data
        assert "Customer deleted" in response_data["message"]

    def test_get_customers_potential_buyers(self, client):
        response = client.get("/api/customers?buyers=true")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "customers" in response_data
        customers = response_data["customers"]
        for customer in customers:
            assert "id" in customer
            assert customer["cars"] == []

    def test_customer_by_id_not_found(self, client):
        response = client.get("/api/customers/99")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert "message" in response_data
        assert response_data["message"] == "Customer of ID 99 not found."

    def test_not_add_customer_error_response(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.post(
            "/api/customers",
            headers=header,
            json={"name": 2, "email": "mymail@email.com"},
        )

        assert response.status_code != 200

    def test_not_remove_customer_not_found(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.delete("/api/customers/99", headers=header)
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert "message" in response_data
        assert response_data["message"] == "Customer of ID 99 not found."
