# Lotline: Car Dealership Inventory System

A full-stack inventory system for a car dealership. Buyers register, browse the lot, search and filter, and purchase vehicles. Admins also add, edit, delete and restock vehicles. Stock levels are enforced on the server, so a vehicle can never be oversold.

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2, SQLite (PostgreSQL-ready), JWT auth, bcrypt
- **Frontend:** React 19, Vite, Tailwind CSS 4, React Router
- **Tests:** pytest (100 tests, 99% coverage) and Vitest + Testing Library (23 tests). See [TEST_REPORT.md](TEST_REPORT.md).

![Admin dashboard](docs/screenshots/02-dashboard-admin.png)

## Contents

- [Features](#features)
- [Project structure](#project-structure)
- [Running locally](#running-locally)
- [Running the tests](#running-the-tests)
- [API reference](#api-reference)
- [Design decisions](#design-decisions)
- [Screenshots](#screenshots)

## Features

**Everyone (after logging in)**
- Register and log in; the session survives a page refresh and is re-validated on load
- See every vehicle as a "window sticker" card with price and stock
- Search by make or model, filter by category and price range, or show only in-stock vehicles
- Purchase a vehicle; the button is disabled when stock is zero

**Admins**
- Add, edit and delete vehicles
- Restock a vehicle when a delivery arrives

## Project structure

```
car-dealership/
├── backend/
│   ├── app/
│   │   ├── core/            config, database, security (bcrypt + JWT), domain exceptions
│   │   ├── repositories/    all SQL lives here (UserRepository, VehicleRepository)
│   │   ├── services/        business rules (AuthService, VehicleService)
│   │   ├── routers/         thin HTTP layer (auth.py, vehicles.py)
│   │   ├── dependencies.py  wires services per request; auth and admin guards
│   │   ├── models.py        SQLAlchemy models
│   │   ├── schemas.py       Pydantic request/response contracts
│   │   ├── seed.py          sample admin + inventory
│   │   └── main.py          app factory and error→HTTP status mapping
│   └── tests/
│       ├── unit/            security and VehicleService rules
│       └── api/             endpoint behaviour through the HTTP layer
├── frontend/
│   └── src/
│       ├── api/             fetch wrapper + one function per endpoint
│       ├── context/         AuthContext (session state)
│       ├── hooks/           useVehicles (debounced loading + local updates)
│       ├── components/      VehicleCard, VehicleForm, FilterBar, Modal, …
│       └── pages/           Login, Register, Dashboard
├── docs/screenshots/
└── TEST_REPORT.md
```

## Running locally

Prerequisites: **Python 3.11+** and **Node.js 20+**.

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # Windows: copy .env.example .env
# Edit .env and set JWT_SECRET to a long random value:
#   python -c "import secrets; print(secrets.token_urlsafe(48))"

python -m app.seed                 # creates admin@example.com / Admin@12345 and 10 sample vehicles
uvicorn app.main:app --reload --port 8000
```

The API is now at http://localhost:8000, with interactive docs at http://localhost:8000/docs.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server forwards `/api` requests to the backend on port 8000.

### 3. Try it

- Log in as the seeded admin: `admin@example.com` / `Admin@12345`
- Or register a new account. It's a regular buyer unless its email is listed in `ADMIN_EMAILS` in `backend/.env`.

### Using PostgreSQL instead of SQLite

Set `DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dealership` in `backend/.env`. Tables are created automatically on startup.

### Production build

```bash
cd frontend
VITE_API_URL=https://your-api.example.com npm run build   # output in frontend/dist
```

Add the deployed frontend's origin to `CORS_ORIGINS` in the backend's environment.

## Running the tests

```bash
# Backend
cd backend
pytest                                   # 100 tests, ~7 seconds
pytest --cov=app --cov-report=term-missing

# Frontend
cd frontend
npm test                                 # 23 tests
npm run coverage
```

Each backend test gets its own temporary SQLite file, so tests are isolated from each other and from your local database. The test settings lower bcrypt's work factor to keep the suite fast.

## API reference

All `/api/vehicles` routes need an `Authorization: Bearer <token>` header. Errors return `{"detail": "..."}`.

| Method | Path | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register` | Public | `{name, email, password}` → `201 {access_token, user}` |
| POST | `/api/auth/login` | Public | `{email, password}` → `200 {access_token, user}` |
| GET | `/api/auth/me` | User | Current user |
| GET | `/api/vehicles` | User | All vehicles |
| GET | `/api/vehicles/search` | User | Query: `make`, `model`, `category`, `min_price`, `max_price` |
| GET | `/api/vehicles/{id}` | User | One vehicle |
| POST | `/api/vehicles` | Admin | Create: `{make, model, category, price, quantity, year?, color?, image_url?, description?}` |
| PUT | `/api/vehicles/{id}` | Admin | Partial update; only fields sent are changed |
| DELETE | `/api/vehicles/{id}` | Admin | `204 No Content` |
| POST | `/api/vehicles/{id}/purchase` | User | Optional `{quantity}` (default 1); decreases stock |
| POST | `/api/vehicles/{id}/restock` | Admin | `{quantity}` (≥ 1); increases stock |
| GET | `/api/health` | Public | Liveness check |

Status codes: `400` business-rule violation (e.g. `min_price > max_price`), `401` missing or invalid token, `403` not an admin, `404` unknown vehicle, `409` duplicate email or not enough stock, `422` invalid input.

## Design decisions

- **Layered backend.** Routers handle HTTP only, services hold business rules, repositories hold SQL. Services raise framework-free domain errors (`NotFoundError`, `InsufficientStockError`, …) and `main.py` maps them to status codes in one place. This keeps rules unit-testable without HTTP and lets the storage layer change without touching business logic.
- **No overselling.** Purchase is a single conditional `UPDATE … SET quantity = quantity - n WHERE id = ? AND quantity >= n`. Two simultaneous purchases of the last unit cannot both succeed. A database `CHECK (quantity >= 0)` backs this up.
- **Admin-only catalogue changes.** The brief marks only delete and restock as admin-only, but its frontend section gives add and update to admins too. Letting any buyer edit prices would be a real security hole, so create and update are admin-only as well.
- **How admins are made.** Registration never accepts a role from the client. Emails listed in `ADMIN_EMAILS` become admins on registration, and `python -m app.seed` creates one directly.
- **Auth hygiene.** Passwords are bcrypt-hashed; tokens are HS256 JWTs with expiry; login returns the same error for an unknown email and a wrong password, so it doesn't reveal which accounts exist; emails are normalised to lower case.
- **App factory.** `create_app(settings)` takes settings explicitly, so tests build an app against a throwaway database without monkey-patching globals.
- **Frontend data flow.** Filters are debounced (300 ms) and stale responses are discarded. After a purchase or edit the card updates in place from the server's response; on a failed purchase the list reloads to show true stock. An expired session logs the user out instead of showing an error.
- **Visual design.** The interface borrows from the dealership itself: each vehicle is a window sticker, the accent is parking-lot line paint, and the header carries a lane marking. One self-hosted typeface (Archivo) is used at an expanded width for badges and normal width for text.

## Screenshots

| | |
|---|---|
| ![Login](docs/screenshots/01-login.png) Login | ![Search](docs/screenshots/04-search-filter.png) Search and filter |
| ![Purchase](docs/screenshots/03-purchase-toast.png) Purchase confirmation | ![Add vehicle](docs/screenshots/05-add-vehicle.png) Admin: add a vehicle |
| ![Restock](docs/screenshots/06-restock.png) Admin: restock | ![Mobile](docs/screenshots/07-buyer-mobile.png) Buyer view on mobile |
