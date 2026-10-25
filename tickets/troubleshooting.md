# Troubleshooting — Stage 1 (Windows)

## MySQL and database

**`mysql` is not recognized as a command**
MySQL's `bin` folder is not on PATH. Open the MySQL install folder (usually `C:\Program Files\MySQL\MySQL Server 8.4\bin`) and add it to the Windows PATH, or run the command with the full path. Open a new terminal afterwards.

**`ERROR 2003 (HY000): Can't connect to MySQL server`**
The MySQL service is stopped. Open Services (`Win + R`, type `services.msc`), find **MySQL84** (or similar), and click **Start**.

**`ERROR 1045 (28000): Access denied for user 'root'`**
The root password typed is wrong. Retry with `mysql -u root -p`. If you forgot it, use the MySQL Installer to reconfigure the server.

**`source database/schema.sql` fails with "No such file"**
The terminal is not in the project root. Run `cd C:\path\to\ticket-management-system` first and confirm with `dir database`.

**Backend shows `Access denied for user 'ticket_user'`**
The password in `.env` does not match the one in `database/schema.sql`. Make them identical, then rerun `schema.sql`.

**`RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods`**
The backend dependencies were not fully installed. Run `pip install -r backend\requirements-dev.txt` again. The `cryptography` package is in `requirements.txt`.

## Python and backend

**`DATABASE_URL is not set`**
The `.env` file is missing or in the wrong place. It must be in the project root, named exactly `.env` (not `.env.txt`). Create it with `Copy-Item .env.example .env`. In File Explorer, enable "File name extensions" to check for `.txt`.

**`'uvicorn' is not recognized`**
The virtual environment is not active. Run `.\.venv\Scripts\Activate.ps1`. The prompt should begin with `(.venv)`.

**`.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled`**
Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer `Y`, then activate again.

**`ModuleNotFoundError: No module named 'app'`**
Start uvicorn from the project root with `--app-dir backend`, exactly as shown in the README. Do not run it from inside `backend` without that option.

**`Address already in use` on port 8000**
Another program uses the port. Find it with `netstat -ano | findstr :8000`, stop that process in Task Manager, or start the backend on another port (`--port 8001`) and update `VITE_API_URL`.

**`pytest` reports `ModuleNotFoundError`**
Dependencies are not installed in the active virtual environment. Activate it and run `pip install -r backend\requirements-dev.txt`.

## Frontend

**`npm` is not recognized**
Node.js is not installed or the terminal was opened before installation. Install Node.js 22 LTS and open a new terminal.

**Header shows "Cannot reach the backend" or "Backend status: unreachable"**
The backend is not running, or runs on a different port. Start it and confirm `http://localhost:8000/api/health` opens in a browser.

**Browser console shows a CORS error**
The frontend origin is not allowed. The default is `http://localhost:5173`. Make sure `CORS_ORIGINS` in `.env` includes that exact address, then restart the backend.

**Header shows HTTP 503 "unavailable"**
The backend runs but cannot reach MySQL. Check that the MySQL service is running and that `DATABASE_URL` in `.env` is correct. Restart the backend after changing `.env`.

**Port 5173 already in use**
`npm run dev` uses `--strictPort`, so it stops instead of switching ports. Close the other program using 5173, or stop the old dev server with `Ctrl + C`.

**Changes to code do not show in the browser**
Save the file and check the terminal for errors. Hard-refresh the browser with `Ctrl + F5`.

## Quick diagnostics
1. `http://localhost:8000/api/health` — tells you whether the API and database work.
2. `http://localhost:8000/docs` — lets you try each endpoint directly.
3. Backend terminal output — shows the database error details.
