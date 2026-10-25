"""API tests for vehicle CRUD and search endpoints."""

import pytest

VEHICLES = "/api/vehicles"


class TestAuthenticationRequired:
    @pytest.mark.parametrize(
        ("method", "path"),
        [
            ("get", VEHICLES),
            ("post", VEHICLES),
            ("get", f"{VEHICLES}/search"),
            ("get", f"{VEHICLES}/1"),
            ("put", f"{VEHICLES}/1"),
            ("delete", f"{VEHICLES}/1"),
            ("post", f"{VEHICLES}/1/purchase"),
            ("post", f"{VEHICLES}/1/restock"),
        ],
    )
    def test_every_vehicle_endpoint_requires_a_token(self, client, method, path):
        response = getattr(client, method)(path)
        assert response.status_code == 401


class TestCreateVehicle:
    def test_admin_can_create_vehicle(self, client, admin_headers, vehicle_payload):
        response = client.post(VEHICLES, json=vehicle_payload, headers=admin_headers)
        assert response.status_code == 201
        body = response.json()
        assert isinstance(body["id"], int)
        for field in ("make", "model", "category", "price", "quantity"):
            assert body[field] == vehicle_payload[field]

    def test_regular_user_cannot_create_vehicle(self, client, user_headers, vehicle_payload):
        response = client.post(VEHICLES, json=vehicle_payload, headers=user_headers)
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "override",
        [
            {"price": 0},
            {"price": -10},
            {"quantity": -1},
            {"make": ""},
            {"model": "   "},
            {"category": ""},
        ],
    )
    def test_invalid_payload_returns_422(self, client, admin_headers, vehicle_payload, override):
        response = client.post(VEHICLES, json={**vehicle_payload, **override}, headers=admin_headers)
        assert response.status_code == 422

    @pytest.mark.parametrize("missing", ["make", "model", "category", "price", "quantity"])
    def test_missing_required_field_returns_422(self, client, admin_headers, vehicle_payload, missing):
        payload = {k: v for k, v in vehicle_payload.items() if k != missing}
        assert client.post(VEHICLES, json=payload, headers=admin_headers).status_code == 422

    def test_text_fields_are_trimmed(self, client, admin_headers, vehicle_payload):
        payload = {**vehicle_payload, "make": "  Tesla  ", "model": " Model 3 "}
        body = client.post(VEHICLES, json=payload, headers=admin_headers).json()
        assert (body["make"], body["model"]) == ("Tesla", "Model 3")


class TestListAndGet:
    def test_list_returns_all_vehicles(self, client, user_headers, create_vehicle):
        create_vehicle(model="Corolla")
        create_vehicle(model="Camry")
        response = client.get(VEHICLES, headers=user_headers)
        assert response.status_code == 200
        assert {v["model"] for v in response.json()} == {"Corolla", "Camry"}

    def test_list_is_empty_when_no_vehicles(self, client, user_headers):
        assert client.get(VEHICLES, headers=user_headers).json() == []

    def test_get_single_vehicle(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.get(f"{VEHICLES}/{vehicle['id']}", headers=user_headers)
        assert response.status_code == 200
        assert response.json()["id"] == vehicle["id"]

    def test_get_unknown_vehicle_returns_404(self, client, user_headers):
        assert client.get(f"{VEHICLES}/9999", headers=user_headers).status_code == 404


class TestSearch:
    @pytest.fixture(autouse=True)
    def _inventory(self, create_vehicle):
        create_vehicle(make="Toyota", model="Corolla", category="Sedan", price=21000)
        create_vehicle(make="Toyota", model="RAV4", category="SUV", price=32000)
        create_vehicle(make="Ford", model="F-150", category="Truck", price=45000)

    def _search(self, client, headers, **params):
        response = client.get(f"{VEHICLES}/search", params=params, headers=headers)
        assert response.status_code == 200, response.text
        return {v["model"] for v in response.json()}

    def test_search_by_make(self, client, user_headers):
        assert self._search(client, user_headers, make="toyota") == {"Corolla", "RAV4"}

    def test_search_by_model(self, client, user_headers):
        assert self._search(client, user_headers, model="F-1") == {"F-150"}

    def test_search_by_category(self, client, user_headers):
        assert self._search(client, user_headers, category="Truck") == {"F-150"}

    def test_search_by_min_price(self, client, user_headers):
        assert self._search(client, user_headers, min_price=30000) == {"RAV4", "F-150"}

    def test_search_by_max_price(self, client, user_headers):
        assert self._search(client, user_headers, max_price=30000) == {"Corolla"}

    def test_search_with_no_filters_returns_everything(self, client, user_headers):
        assert self._search(client, user_headers) == {"Corolla", "RAV4", "F-150"}

    def test_search_with_no_matches_returns_empty_list(self, client, user_headers):
        assert self._search(client, user_headers, make="Ferrari") == set()

    def test_inverted_price_range_returns_400(self, client, user_headers):
        response = client.get(
            f"{VEHICLES}/search", params={"min_price": 50000, "max_price": 1000}, headers=user_headers
        )
        assert response.status_code == 400

    def test_negative_price_returns_422(self, client, user_headers):
        response = client.get(f"{VEHICLES}/search", params={"min_price": -5}, headers=user_headers)
        assert response.status_code == 422


class TestUpdateVehicle:
    def test_admin_can_partially_update_vehicle(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle(price=21500)
        response = client.put(f"{VEHICLES}/{vehicle['id']}", json={"price": 19999}, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["price"] == 19999
        assert response.json()["model"] == vehicle["model"]

    def test_regular_user_cannot_update_vehicle(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.put(f"{VEHICLES}/{vehicle['id']}", json={"price": 1}, headers=user_headers)
        assert response.status_code == 403

    def test_update_unknown_vehicle_returns_404(self, client, admin_headers):
        response = client.put(f"{VEHICLES}/9999", json={"price": 1}, headers=admin_headers)
        assert response.status_code == 404

    def test_update_with_invalid_value_returns_422(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.put(f"{VEHICLES}/{vehicle['id']}", json={"price": -1}, headers=admin_headers)
        assert response.status_code == 422


class TestDeleteVehicle:
    def test_admin_can_delete_vehicle(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle()
        assert client.delete(f"{VEHICLES}/{vehicle['id']}", headers=admin_headers).status_code == 204
        assert client.get(f"{VEHICLES}/{vehicle['id']}", headers=admin_headers).status_code == 404

    def test_regular_user_cannot_delete_vehicle(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle()
        assert client.delete(f"{VEHICLES}/{vehicle['id']}", headers=user_headers).status_code == 403

    def test_delete_unknown_vehicle_returns_404(self, client, admin_headers):
        assert client.delete(f"{VEHICLES}/9999", headers=admin_headers).status_code == 404
