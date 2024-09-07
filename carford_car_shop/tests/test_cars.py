import pytest
import json


class TestCars:

    def test_get_all_cars_route(self, client):
        response = client.get("/api/cars")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "cars" in response_data
        assert len(response_data["cars"]) > 0
        cars = response_data["cars"]
        for car in cars:
            assert "id" in car
            assert "model" in car
            assert "color" in car

    def test_get_car_by_id_route(self, client):
        response = client.get("/api/cars/1")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "cars" in response_data
        car = response_data["cars"]
        assert car["id"] == 1
        assert "owner_id" in car

    def test_add_car_route(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.post(
            "/api/cars",
            headers=header,
            json={"model": "hatch", "color": "yellow", "owner_id": 1},
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "message" in response_data
        assert "Car added to customer 1." in response_data["message"]

    def test_remove_car_route(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.delete("/api/cars/6", headers=header)
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        assert "message" in response_data
        assert "Car deleted" in response_data["message"]

    def test_car_by_id_not_found(self, client):
        response = client.get("/api/cars/99")
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert "message" in response_data
        assert "Car of ID 99 not found." in response_data["message"]

    def test_not_add_car_invalid_input(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.post(
            "/api/cars",
            headers=header,
            json={"model": "fiat", "color": "yellow", "owner_id": 1},
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "error" in response_data
        assert "Invalid car Model/Color. Check the input." in response_data["error"]

    def test_not_add_car_customer_has_three(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.post(
            "/api/cars",
            headers=header,
            json={"model": "sedan", "color": "yellow", "owner_id": 4},
        )
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 400
        assert "message" in response_data
        assert (
            "Customer own 3 cars and can not add a new one." in response_data["message"]
        )

    def test_not_remove_car_not_found(self, client, token_jwt):
        header = {"Authorization": f"Bearer {token_jwt}"}
        response = client.delete("/api/cars/99", headers=header)
        response_data = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert "message" in response_data
        assert "Car of ID 99 not found." in response_data["message"]
