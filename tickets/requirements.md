# Requirements — Ticket Management System (Stage 1)

## Purpose
A small internal tool where team members create, track, update, and close work tickets (bugs, requests, incidents).

## Functional requirements
| ID | Requirement |
|----|-------------|
| FR-01 | Users can create a ticket with a title, description, status, priority, and assignee. |
| FR-02 | Users can view a list of all tickets, newest first. |
| FR-03 | Users can filter the list by status and by priority (API) and by status (UI). |
| FR-04 | Users can view a single ticket by ID. |
| FR-05 | Users can edit any field of an existing ticket. |
| FR-06 | Users can delete a ticket after confirming the action. |
| FR-07 | The system stores tickets in a MySQL database so data survives restarts. |
| FR-08 | The backend exposes a health-check endpoint that verifies database connectivity. |
| FR-09 | Invalid input is rejected with a clear error message. |

## Ticket fields
| Field | Type | Required | Rules |
|-------|------|----------|-------|
| id | integer | generated | Auto-increment primary key |
| title | text | yes | 3–200 characters after trimming spaces |
| description | text | no | Up to 5000 characters |
| status | enum | no (default `open`) | `open`, `in_progress`, `resolved`, `closed` |
| priority | enum | no (default `medium`) | `low`, `medium`, `high`, `critical` |
| assignee | text | no | Up to 100 characters |
| created_at | timestamp | generated | UTC, set when the ticket is created |

## Non-functional requirements
- Runs on Windows 10/11 with Python 3.12, Node.js 22 LTS, and MySQL 8.x (or MariaDB 10.6+ for development).
- No authentication in Stage 1 (single-team internal use on localhost). Authentication is out of scope until a later stage.
- Secrets (database password) are read from a `.env` file and never hard-coded in application code.
- Backend API responds in under 500 ms for list and single-record operations with up to 1,000 tickets on a local machine.

## Out of scope for Stage 1
User accounts and login, file attachments, comments, email notifications, and Docker or AWS deployment (Stages 2–7).
