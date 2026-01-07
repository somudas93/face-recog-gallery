# Face Recognizer Gallery

A simple Tauri desktop application demonstrating face detection and recognition.

- Frontend: React + Tailwind (Vite)
- Backend: Python FastAPI + DeepFace
- Bundler: Tauri (Rust) - automatically starts the Python backend when the desktop app launches.

## Quick start (Development)

Prerequisites:
- Node.js 18+
- Python 3.10+ with pip
- Rust + cargo (for Tauri)

1. Install backend Python deps

```powershell
python -m venv .venv; .\.venv\Scripts\activate; pip install -r backend\requirements.txt
```

2. Install frontend dependencies

```powershell
cd frontend; npm install; cd ..
```

3. Start the backend

```powershell
# In a terminal
cd backend; uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Start the frontend dev server

```powershell
cd frontend; npm run dev
```

5. Open frontend at http://127.0.0.1:5173


## Run as a Desktop App (Tauri)

1. Install Rust (and required toolchains) and Tauri prerequisites
2. For development, from root run:

```powershell
# In one terminal: start backend
cd backend; uvicorn main:app --reload --host 127.0.0.1 --port 8000

# In another: start frontend
cd frontend; npm run dev

# In another: start tauri dev
cd src-tauri; cargo run
```

Tauri's `main.rs` will attempt to spawn the backend automatically when built as a bundle.

## Notes
- This project uses DeepFace which downloads models on first run. Expect the first recognition to take longer while models are cached.
- This is an example and not meant for production.

