"""Unit tests for VehicleService business rules.

These run against a real (temporary) SQLite database through the repository,
but bypass HTTP entirely so the domain logic is tested in isolation.
"""

import pytest

from app.core.database import Database
from app.core.exceptions import InsufficientStockError, NotFoundError, ValidationError
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas import VehicleCreate, VehicleSearchParams, VehicleUpdate
from app.services.vehicle_service import VehicleService


@pytest.fixture
def service(tmp_path):
    database = Database(f"sqlite:///{tmp_path / 'unit.db'}")
    database.create_all()
    session = database.session_factory()
    try:
        yield VehicleService(VehicleRepository(session))
    finally:
        session.close()
        database.dispose()


def _new(service: VehicleService, **overrides):
    data = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24000, "quantity": 3}
    data.update(overrides)
    return service.create(VehicleCreate(**data))


class TestCreateAndRead:
    def test_create_assigns_an_id(self, service):
        vehicle = _new(service)
        assert vehicle.id is not None

    def test_get_unknown_vehicle_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.get(9999)

    def test_list_all_returns_every_vehicle(self, service):
        _new(service, model="Civic")
        _new(service, model="Accord")
        assert {v.model for v in service.list_all()} == {"Civic", "Accord"}


class TestUpdateAndDelete:
    def test_update_changes_only_supplied_fields(self, service):
        vehicle = _new(service, price=24000)
        updated = service.update(vehicle.id, VehicleUpdate(price=22000))
        assert updated.price == 22000
        assert updated.model == "Civic"

    def test_update_unknown_vehicle_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.update(9999, VehicleUpdate(price=1))

    def test_delete_removes_vehicle(self, service):
        vehicle = _new(service)
        service.delete(vehicle.id)
        with pytest.raises(NotFoundError):
            service.get(vehicle.id)


class TestPurchase:
    def test_purchase_decrements_quantity_by_one_by_default(self, service):
        vehicle = _new(service, quantity=3)
        assert service.purchase(vehicle.id).quantity == 2

    def test_purchase_multiple_units(self, service):
        vehicle = _new(service, quantity=3)
        assert service.purchase(vehicle.id, quantity=3).quantity == 0

    def test_purchase_more_than_stock_raises_and_keeps_stock(self, service):
        vehicle = _new(service, quantity=1)
        with pytest.raises(InsufficientStockError):
            service.purchase(vehicle.id, quantity=2)
        assert service.get(vehicle.id).quantity == 1

    def test_purchase_out_of_stock_raises(self, service):
        vehicle = _new(service, quantity=0)
        with pytest.raises(InsufficientStockError):
            service.purchase(vehicle.id)

    def test_purchase_unknown_vehicle_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.purchase(9999)


class TestRestock:
    def test_restock_increments_quantity(self, service):
        vehicle = _new(service, quantity=0)
        assert service.restock(vehicle.id, quantity=4).quantity == 4

    def test_restock_unknown_vehicle_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.restock(9999, quantity=1)


class TestSearch:
    @pytest.fixture(autouse=True)
    def _inventory(self, service):
        _new(service, make="Toyota", model="Corolla", category="Sedan", price=21000)
        _new(service, make="Toyota", model="RAV4", category="SUV", price=32000)
        _new(service, make="Ford", model="F-150", category="Truck", price=45000)

    def test_search_by_make_is_case_insensitive(self, service):
        results = service.search(VehicleSearchParams(make="toyota"))
        assert {v.model for v in results} == {"Corolla", "RAV4"}

    def test_search_by_partial_model(self, service):
        results = service.search(VehicleSearchParams(model="rav"))
        assert [v.model for v in results] == ["RAV4"]

    def test_search_by_category(self, service):
        results = service.search(VehicleSearchParams(category="suv"))
        assert [v.model for v in results] == ["RAV4"]

    def test_search_by_price_range_is_inclusive(self, service):
        results = service.search(VehicleSearchParams(min_price=21000, max_price=32000))
        assert {v.model for v in results} == {"Corolla", "RAV4"}

    def test_search_combines_filters(self, service):
        results = service.search(VehicleSearchParams(make="toyota", max_price=25000))
        assert [v.model for v in results] == ["Corolla"]

    def test_inverted_price_range_raises_validation_error(self, service):
        with pytest.raises(ValidationError):
            service.search(VehicleSearchParams(min_price=50000, max_price=10000))
