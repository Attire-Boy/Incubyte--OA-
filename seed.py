"""Seed the local database with an admin account and sample inventory.

Usage (from the backend folder):
    python -m app.seed

Idempotent: re-running it won't duplicate the admin or the vehicles.
"""

import os

from app.core.config import Settings
from app.core.database import Database
from app.core.security import PasswordHasher
from app.models import User, Vehicle
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository

SAMPLE_VEHICLES = [
    {"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 21550, "quantity": 8, "year": 2025, "color": "Silver"},
    {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24650, "quantity": 5, "year": 2025, "color": "Blue"},
    {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 29800, "quantity": 6, "year": 2025, "color": "White"},
    {"make": "Hyundai", "model": "Creta", "category": "SUV", "price": 18900, "quantity": 0, "year": 2024, "color": "Red"},
    {"make": "Ford", "model": "F-150", "category": "Truck", "price": 38900, "quantity": 3, "year": 2024, "color": "Black"},
    {"make": "Tesla", "model": "Model 3", "category": "Electric", "price": 40240, "quantity": 4, "year": 2025, "color": "Pearl White"},
    {"make": "Tata", "model": "Nexon EV", "category": "Electric", "price": 17500, "quantity": 7, "year": 2025, "color": "Teal"},
    {"make": "Mazda", "model": "MX-5 Miata", "category": "Convertible", "price": 29930, "quantity": 2, "year": 2024, "color": "Soul Red"},
    {"make": "BMW", "model": "M4", "category": "Coupe", "price": 79100, "quantity": 1, "year": 2025, "color": "Isle of Man Green"},
    {"make": "Volkswagen", "model": "Golf GTI", "category": "Hatchback", "price": 32000, "quantity": 0, "year": 2024, "color": "Grey"},
]


def seed() -> None:
    settings = Settings.from_env()
    database = Database(settings.database_url)
    database.create_all()
    session = database.new_session()
    try:
        users = UserRepository(session)
        admin_email = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com").lower()
        admin_password = os.getenv("SEED_ADMIN_PASSWORD", "Admin@12345")
        if users.get_by_email(admin_email) is None:
            users.add(
                User(
                    name="Dealership Admin",
                    email=admin_email,
                    password_hash=PasswordHasher(settings.bcrypt_rounds).hash(admin_password),
                    is_admin=True,
                )
            )
            print(f"Created admin user: {admin_email} / {admin_password}")
        else:
            print(f"Admin user already exists: {admin_email}")

        vehicles = VehicleRepository(session)
        if vehicles.list_all():
            print("Vehicles already present, skipping sample inventory.")
        else:
            for data in SAMPLE_VEHICLES:
                vehicles.add(Vehicle(**data))
            print(f"Added {len(SAMPLE_VEHICLES)} sample vehicles.")
    finally:
        session.close()
        database.dispose()


if __name__ == "__main__":
    seed()
