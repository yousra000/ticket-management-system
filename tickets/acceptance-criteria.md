# Acceptance Criteria — Stage 1

Stage 1 is accepted only when every item below passes on the user's Windows machine.

## Setup
- [ ] `.env` exists in the project root and contains a valid `DATABASE_URL`.
- [ ] `database/schema.sql` runs without errors and creates the `ticketdb` database and `tickets` table.
- [ ] `ticket_user` can log in to MySQL with the password from `.env`.
- [ ] Backend dependencies install with `pip install -r backend\requirements-dev.txt`.
- [ ] Frontend dependencies install with `npm install` inside `frontend`.

## Backend
- [ ] `uvicorn app.main:app --app-dir backend --reload --port 8000` starts without errors.
- [ ] `GET /api/health` returns HTTP 200 with `{"status":"ok","database":"ok"}`.
- [ ] `POST /api/tickets` with a valid body returns HTTP 201 and the created ticket.
- [ ] `POST /api/tickets` with a title shorter than 3 characters returns HTTP 422.
- [ ] `GET /api/tickets` returns tickets newest first.
- [ ] `GET /api/tickets?status=open` returns only open tickets.
- [ ] `GET /api/tickets/{id}` returns 200 for an existing ticket and 404 for a missing one.
- [ ] `PUT /api/tickets/{id}` replaces the ticket fields and returns 200.
- [ ] `DELETE /api/tickets/{id}` returns 204, and the ticket is no longer retrievable.
- [ ] The backend returns HTTP 503 with a clear message when MySQL is stopped, and the process does not crash.

## Frontend
- [ ] `npm run dev` serves the app at `http://localhost:5173`.
- [ ] The header shows "Backend and database connected" when both services are running.
- [ ] A ticket can be created from the form and appears in the table without a page reload.
- [ ] Submitting a title with fewer than 3 characters shows a validation message and sends no request.
- [ ] Clicking Edit loads the ticket into the form, and Update saves the changes.
- [ ] Clicking Delete asks for confirmation, then removes the ticket.
- [ ] The status filter shows only tickets with the selected status.

## Tests
- [ ] `python -m pytest tests -v` reports all tests passing (20 tests).

## Data
- [ ] Tickets created through the UI persist after the backend is restarted.
