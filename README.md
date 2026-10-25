# Ticket Management System

A ticket tracker built with React (frontend), FastAPI (backend), and MySQL (database).

## Project layout
```
ticket-management-system/
├── backend/          FastAPI application and dependencies
├── frontend/         React application (Vite)
├── database/         schema.sql — creates the database, user, and table
├── tests/            Automated backend API tests (pytest)
├── tickets/          Requirements, acceptance criteria, API spec, test cases, architecture, troubleshooting
├── .env.example      Template for local configuration (copy to .env)
└── README.md
```

## Prerequisites (Windows)
- Python 3.12 (during installation, tick **Add python.exe to PATH**)
- Node.js 22 LTS
- MySQL Server 8.0 or 8.4 (with the `mysql` command-line client on PATH)
- Visual Studio Code

Check each installation in a new terminal:
```powershell
py -3.12 --version
node --version
npm --version
mysql --version
```

## Open the project in VS Code
1. Extract the ZIP to a simple path such as `C:\Projects\ticket-management-system`.
2. In VS Code: **File → Open Folder** → select `ticket-management-system`.
3. Open a terminal: **Terminal → New Terminal** (PowerShell).

## 1. Create the database
```powershell
mysql -u root -p -e "source database/schema.sql"
```
Enter your MySQL root password when prompted.

## 2. Configure environment variables
```powershell
Copy-Item .env.example .env
```
The default `DATABASE_URL` uses user `ticket_user` and password `ChangeMe_Local_123`, which match `database/schema.sql`. If you change the password, change it in both places.

## 3. Install and start the backend
Run these commands in the first terminal, from the project root:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements-dev.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```
Leave this terminal running. Verify in a browser: `http://localhost:8000/api/health` should show `{"status":"ok","database":"ok"}`. API docs are at `http://localhost:8000/docs`.

## 4. Install and start the frontend
Open a **second terminal** (**Terminal → New Terminal**) in the project root:
```powershell
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173`. The header should show **Backend and database connected**.

## 5. Run the automated tests
In a terminal with the virtual environment active, from the project root:
```powershell
python -m pytest tests -v
```
Expected result: 20 passed.

## Stopping the application
Press `Ctrl + C` in each terminal. To leave the virtual environment, run `deactivate`.

## Documentation
Detailed requirements, acceptance criteria, API specification, test cases, architecture, and troubleshooting are in the `tickets/` folder.
