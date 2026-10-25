"""Vehicle catalogue and inventory business rules."""

from collections.abc import Sequence

from app.core.exceptions import InsufficientStockError, NotFoundError, ValidationError
from app.models import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas import VehicleCreate, VehicleSearchParams, VehicleUpdate


class VehicleService:
    def __init__(self, vehicles: VehicleRepository) -> None:
        self._vehicles = vehicles

    # ----- Catalogue -----

    def create(self, data: VehicleCreate) -> Vehicle:
        return self._vehicles.add(Vehicle(**data.model_dump()))

    def get(self, vehicle_id: int) -> Vehicle:
        vehicle = self._vehicles.get(vehicle_id)
        if vehicle is None:
            raise NotFoundError(f"Vehicle {vehicle_id} not found")
        return vehicle

    def list_all(self) -> Sequence[Vehicle]:
        return self._vehicles.list_all()

    def search(self, params: VehicleSearchParams) -> Sequence[Vehicle]:
        if (
            params.min_price is not None
            and params.max_price is not None
            and params.min_price > params.max_price
        ):
            raise ValidationError("min_price cannot be greater than max_price")
        return self._vehicles.search(**params.model_dump())

    def update(self, vehicle_id: int, data: VehicleUpdate) -> Vehicle:
        vehicle = self.get(vehicle_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vehicle, field, value)
        return self._vehicles.save(vehicle)

    def delete(self, vehicle_id: int) -> None:
        self._vehicles.delete(self.get(vehicle_id))

    # ----- Inventory -----

    def purchase(self, vehicle_id: int, quantity: int = 1) -> Vehicle:
        vehicle = self.get(vehicle_id)
        if not self._vehicles.adjust_quantity(vehicle_id, -quantity):
            raise InsufficientStockError(
                f"Only {vehicle.quantity} unit(s) of {vehicle.make} {vehicle.model} in stock"
            )
        return self._vehicles.refresh(vehicle)

    def restock(self, vehicle_id: int, quantity: int) -> Vehicle:
        vehicle = self.get(vehicle_id)
        self._vehicles.adjust_quantity(vehicle_id, quantity)
        return self._vehicles.refresh(vehicle)
