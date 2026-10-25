"""Vehicle catalogue and inventory endpoints.

Every route requires a valid token. Catalogue mutations (create, update,
delete) and restocking additionally require an admin account.
"""

from typing import Annotated

from fastapi import APIRouter, Body, Query, Response, status

from app.dependencies import AdminUser, CurrentUser, VehicleServiceDep
from app.schemas import (
    QuantityRequest,
    RestockRequest,
    VehicleCreate,
    VehicleOut,
    VehicleSearchParams,
    VehicleUpdate,
)

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: VehicleCreate, service: VehicleServiceDep, _: AdminUser):
    return service.create(payload)


@router.get("", response_model=list[VehicleOut])
def list_vehicles(service: VehicleServiceDep, _: CurrentUser):
    return service.list_all()


# Declared before "/{vehicle_id}" so "search" is not parsed as an id.
@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(
    service: VehicleServiceDep,
    _: CurrentUser,
    params: Annotated[VehicleSearchParams, Query()],
):
    return service.search(params)


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, service: VehicleServiceDep, _: CurrentUser):
    return service.get(vehicle_id)


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, service: VehicleServiceDep, _: AdminUser):
    return service.update(vehicle_id, payload)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, service: VehicleServiceDep, _: AdminUser) -> Response:
    service.delete(vehicle_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{vehicle_id}/purchase", response_model=VehicleOut)
def purchase_vehicle(
    vehicle_id: int,
    service: VehicleServiceDep,
    _: CurrentUser,
    payload: Annotated[QuantityRequest | None, Body()] = None,
):
    """Buy one unit by default, or ``{"quantity": n}`` units."""
    return service.purchase(vehicle_id, (payload or QuantityRequest()).quantity)


@router.post("/{vehicle_id}/restock", response_model=VehicleOut)
def restock_vehicle(vehicle_id: int, payload: RestockRequest, service: VehicleServiceDep, _: AdminUser):
    return service.restock(vehicle_id, payload.quantity)
