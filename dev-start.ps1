#!/usr/bin/env pwsh
# dev-start.ps1 - Start backend and frontend dev servers

# Activate venv
Write-Host "Activating Python venv..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Start backend in a new PowerShell window
Write-Host "Starting backend on port 8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", {
  . .\.venv\Scripts\Activate.ps1
  cd backend
  python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
}

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Start frontend in a new PowerShell window
Write-Host "Starting frontend on port 5173..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", {
  cd frontend
  npm run dev
}

Write-Host "Backend and frontend are starting in separate windows." -ForegroundColor Green
Write-Host "Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend: http://127.0.0.1:5173" -ForegroundColor Green
