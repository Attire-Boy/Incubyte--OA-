"""API tests for purchase and restock inventory operations."""

VEHICLES = "/api/vehicles"


class TestPurchase:
    def test_purchase_decreases_quantity_by_one(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle(quantity=3)
        response = client.post(f"{VEHICLES}/{vehicle['id']}/purchase", headers=user_headers)
        assert response.status_code == 200
        assert response.json()["quantity"] == 2

    def test_purchase_accepts_explicit_quantity(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle(quantity=3)
        response = client.post(
            f"{VEHICLES}/{vehicle['id']}/purchase", json={"quantity": 2}, headers=user_headers
        )
        assert response.json()["quantity"] == 1

    def test_purchase_is_persisted(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle(quantity=3)
        client.post(f"{VEHICLES}/{vehicle['id']}/purchase", headers=user_headers)
        assert client.get(f"{VEHICLES}/{vehicle['id']}", headers=user_headers).json()["quantity"] == 2

    def test_purchase_out_of_stock_returns_409(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle(quantity=0)
        response = client.post(f"{VEHICLES}/{vehicle['id']}/purchase", headers=user_headers)
        assert response.status_code == 409

    def test_purchase_more_than_stock_returns_409_and_keeps_stock(
        self, client, user_headers, create_vehicle
    ):
        vehicle = create_vehicle(quantity=1)
        response = client.post(
            f"{VEHICLES}/{vehicle['id']}/purchase", json={"quantity": 5}, headers=user_headers
        )
        assert response.status_code == 409
        assert client.get(f"{VEHICLES}/{vehicle['id']}", headers=user_headers).json()["quantity"] == 1

    def test_purchase_zero_units_returns_422(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.post(
            f"{VEHICLES}/{vehicle['id']}/purchase", json={"quantity": 0}, headers=user_headers
        )
        assert response.status_code == 422

    def test_purchase_unknown_vehicle_returns_404(self, client, user_headers):
        assert client.post(f"{VEHICLES}/9999/purchase", headers=user_headers).status_code == 404

    def test_admin_can_also_purchase(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle(quantity=1)
        response = client.post(f"{VEHICLES}/{vehicle['id']}/purchase", headers=admin_headers)
        assert response.status_code == 200


class TestRestock:
    def test_admin_can_restock(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle(quantity=0)
        response = client.post(
            f"{VEHICLES}/{vehicle['id']}/restock", json={"quantity": 10}, headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["quantity"] == 10

    def test_regular_user_cannot_restock(self, client, user_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.post(
            f"{VEHICLES}/{vehicle['id']}/restock", json={"quantity": 10}, headers=user_headers
        )
        assert response.status_code == 403

    def test_restock_requires_positive_quantity(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle()
        for bad in (0, -3):
            response = client.post(
                f"{VEHICLES}/{vehicle['id']}/restock", json={"quantity": bad}, headers=admin_headers
            )
            assert response.status_code == 422

    def test_restock_requires_a_body(self, client, admin_headers, create_vehicle):
        vehicle = create_vehicle()
        response = client.post(f"{VEHICLES}/{vehicle['id']}/restock", headers=admin_headers)
        assert response.status_code == 422

    def test_restock_unknown_vehicle_returns_404(self, client, admin_headers):
        response = client.post(f"{VEHICLES}/9999/restock", json={"quantity": 1}, headers=admin_headers)
        assert response.status_code == 404

    def test_restock_makes_sold_out_vehicle_purchasable_again(
        self, client, admin_headers, user_headers, create_vehicle
    ):
        vehicle = create_vehicle(quantity=0)
        client.post(f"{VEHICLES}/{vehicle['id']}/restock", json={"quantity": 1}, headers=admin_headers)
        response = client.post(f"{VEHICLES}/{vehicle['id']}/purchase", headers=user_headers)
        assert response.status_code == 200
        assert response.json()["quantity"] == 0


class TestHealth:
    def test_health_endpoint_is_public(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
