# Architecture — Stage 1 (Local Development)

## Components
```
+-------------------+        HTTP JSON         +-------------------+       SQL (PyMySQL)      +-------------+
|  React frontend   |  -------------------->   |  FastAPI backend  |  ---------------------->  |  MySQL 8.x  |
|  Vite dev server  |  <--------------------   |  Uvicorn :8000    |  <----------------------  | ticketdb    |
|  localhost:5173   |                          |                   |                           | tickets     |
+-------------------+                          +-------------------+                           +-------------+
```

- **Frontend (React 18 + Vite):** single-page UI. It calls the backend with `fetch`. Components: `App` (state and layout), `TicketForm` (create and edit with validation), `TicketList` (table with actions), `api.js` (HTTP client).
- **Backend (FastAPI + SQLAlchemy 2.0):** REST endpoints under `/api`. Pydantic schemas validate input. SQLAlchemy ORM maps the `Ticket` model to the `tickets` table. CORS allows requests from the frontend origin.
- **Database (MySQL):** one database (`ticketdb`) and one table (`tickets`). CHECK constraints enforce allowed status and priority values as a second line of defence.

## Request flow (example: create a ticket)
1. The user submits the form. `TicketForm` validates the input and calls `api.createTicket`.
2. `api.js` sends `POST http://localhost:8000/api/tickets` with a JSON body.
3. FastAPI validates the body against `TicketInput`. Invalid input returns 422 before any database call.
4. The route creates a `Ticket` ORM object, commits it to MySQL, and reads the saved row back.
5. The response (201) returns the ticket. The frontend reloads the list.

## Configuration
- `DATABASE_URL` in the root `.env` file selects the database.
- `CORS_ORIGINS` lists allowed frontend origins.
- `VITE_API_URL` (optional, in `frontend/.env`) overrides the backend URL.

## Design decisions
| Decision | Reason |
|----------|--------|
| PUT replaces the whole ticket | Simple and predictable; the form always sends all fields. |
| Status and priority as strings with CHECK constraints | Portable across MySQL and the SQLite used by tests. |
| Naive UTC timestamps in MySQL, `Z` suffix in JSON | MySQL DATETIME has no timezone; the browser converts to local time. |
| Table created at startup if missing | Lets the app start on a fresh database. `schema.sql` remains the authoritative setup. |
| API starts even when MySQL is down | Health checks can report the fault, and the process stays up for troubleshooting. |
| Tests use SQLite in memory | Fast tests without a running MySQL server. Real MySQL is covered by manual tests. |

## Stage 2 preview (not implemented yet)
Docker images for frontend and backend, a `compose.yaml` with a MySQL container, and a persistent volume. MySQL stays outside the backend container.
