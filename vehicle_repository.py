"""Data access for vehicles.

All SQL lives here so services deal only in domain operations.
"""

from collections.abc import Sequence

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models import Vehicle


class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, vehicle_id: int) -> Vehicle | None:
        return self._session.get(Vehicle, vehicle_id)

    def list_all(self) -> Sequence[Vehicle]:
        return self._session.scalars(select(Vehicle).order_by(Vehicle.make, Vehicle.model)).all()

    def search(
        self,
        *,
        make: str | None = None,
        model: str | None = None,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> Sequence[Vehicle]:
        query = select(Vehicle)
        if make:
            query = query.where(func.lower(Vehicle.make).contains(make.strip().lower()))
        if model:
            query = query.where(func.lower(Vehicle.model).contains(model.strip().lower()))
        if category:
            query = query.where(func.lower(Vehicle.category) == category.strip().lower())
        if min_price is not None:
            query = query.where(Vehicle.price >= min_price)
        if max_price is not None:
            query = query.where(Vehicle.price <= max_price)
        return self._session.scalars(query.order_by(Vehicle.price)).all()

    def add(self, vehicle: Vehicle) -> Vehicle:
        self._session.add(vehicle)
        self._session.commit()
        self._session.refresh(vehicle)
        return vehicle

    def save(self, vehicle: Vehicle) -> Vehicle:
        self._session.commit()
        self._session.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self._session.delete(vehicle)
        self._session.commit()

    def adjust_quantity(self, vehicle_id: int, delta: int) -> bool:
        """Atomically add ``delta`` to stock, refusing to go below zero.

        Done as a single conditional UPDATE so two concurrent purchases can
        never oversell the last unit. Returns False if no row was changed.
        """
        statement = (
            update(Vehicle)
            .where(Vehicle.id == vehicle_id, Vehicle.quantity + delta >= 0)
            .values(quantity=Vehicle.quantity + delta)
        )
        result = self._session.execute(statement)
        self._session.commit()
        return result.rowcount == 1

    def refresh(self, vehicle: Vehicle) -> Vehicle:
        self._session.refresh(vehicle)
        return vehicle
