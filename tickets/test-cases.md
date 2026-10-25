# Test Cases — Stage 1

## Automated tests (`tests/test_tickets_api.py`, run with `python -m pytest tests -v`)

The automated tests use an in-memory SQLite database so they run without MySQL. They verify API behaviour and validation. The live MySQL connection is verified separately using the manual cases below.

| ID | Test | Expected result |
|----|------|-----------------|
| T-01 | Health check | 200, `{"status":"ok","database":"ok"}` |
| T-02 | Create ticket with all fields | 201, fields match, `created_at` ends with `Z` |
| T-03 | Create ticket with only title | Defaults `status=open`, `priority=medium`, description null |
| T-04 | Title of 2 characters | 422 |
| T-05 | Blank title (spaces only) | 422 |
| T-06 | Missing title | 422 |
| T-07 | Invalid priority value | 422 |
| T-08 | Invalid status value | 422 |
| T-09 | Title with surrounding spaces | Stored trimmed |
| T-10 | List order | Newest ticket first |
| T-11 | Filter by status | Only matching tickets returned |
| T-12 | Filter by priority | Only matching tickets returned |
| T-13 | Invalid filter value | 422 |
| T-14 | Get existing ticket | 200 |
| T-15 | Get missing ticket | 404 with detail message |
| T-16 | Update all fields | 200, changes persisted |
| T-17 | Update with invalid priority | 422, stored ticket unchanged |
| T-18 | Update missing ticket | 404 |
| T-19 | Delete ticket | 204, then GET returns 404 |
| T-20 | Delete missing ticket | 404 |

## Manual end-to-end tests (Windows, MySQL running)

| ID | Steps | Expected result |
|----|-------|-----------------|
| M-01 | Run `database/schema.sql` | No errors; `tickets` table exists |
| M-02 | Start backend, open `http://localhost:8000/api/health` | `{"status":"ok","database":"ok"}` |
| M-03 | Stop MySQL service, call `/api/health` | 503 `{"status":"error","database":"unavailable"}`; backend still running |
| M-04 | With MySQL stopped, call `GET /api/tickets` | 503 with the "Database is unavailable" message |
| M-05 | Start MySQL again, call `/api/health` | 200 again without restarting backend |
| M-06 | Create a ticket in the UI, restart backend, reload UI | Ticket still listed |
| M-07 | Open the UI with backend stopped | Header shows an error status; form errors display if submitted |
| M-08 | Edit a ticket, change status to Resolved | Table shows Resolved badge |
| M-09 | Delete a ticket and cancel the confirmation dialog | Ticket remains |
| M-10 | Filter by "Closed" in the UI | Only closed tickets are shown |
