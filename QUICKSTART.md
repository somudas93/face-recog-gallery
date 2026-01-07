# Face Recognizer Gallery – Complete Setup & Run Guide

## What's Included

A full-stack face detection and recognition desktop application:

- **Backend**: FastAPI (Python) + DeepFace for face detection, recognition, and gallery management
- **Frontend**: React + Tailwind + Vite for a modern web UI
- **Desktop**: Tauri (Rust) for packaging as a Windows/macOS/Linux desktop app

## Prerequisites

1. **Python 3.10+** (download from python.org)
2. **Node.js 18+** (download from nodejs.org)
3. **Rust + Cargo** (optional, for building desktop app) – install from [rustup.rs](https://rustup.rs)

## Setup (One-Time)

### 1. Create and activate Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Python backend dependencies

```powershell
pip install -r backend/requirements.txt
```

This installs:
- `fastapi` – Web framework
- `uvicorn` – ASGI server
- `deepface` – Face recognition models
- `opencv-python` – Image processing
- `pillow`, `numpy`, `pandas` – Data handling

### 3. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

## Run the Application

### Option A: Web App (Recommended for Development)

Best for testing and development. Run the backend and frontend separately.

**Terminal 1 – Backend API:**
```powershell
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

API docs available at: `http://127.0.0.1:8000/docs`

**Terminal 2 – Frontend:**
```powershell
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

**Open your browser** to `http://localhost:5173` and use the app:
1. Upload an image
2. Click **Detect** to find faces
3. Click **Recognize** to match against your gallery
4. Click **Add to Gallery** to save a face with a name

---

### Option B: Automated Dev Start (Windows)

Run both backend and frontend with one command:

```powershell
.\dev-start.ps1
```

This opens both servers in separate PowerShell windows.

---

### Option C: Desktop App (Tauri)

Requires Rust. Build and run as a native desktop app that auto-launches the backend.

```powershell
cd src-tauri
cargo run
```

The Tauri window will open with the app, and the Python backend will start automatically.

To build a release executable:
```powershell
cd src-tauri
cargo build --release
# Executable at: target/release/face-recog-gallery.exe
```

---

## Using the App

### Detect
Finds all faces in an uploaded image. Returns bounding box coordinates (x, y, width, height).

### Recognize
Matches faces in the uploaded image against your local gallery. Returns the closest matching person(s) and confidence scores.

### Add to Gallery
Saves an uploaded image in the local gallery under a person's name. Images are stored in `backend/db/{person_name}/`.

### Gallery
View all people in your gallery and the number of photos for each.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'uvicorn'"
- Ensure the venv is activated: `.\.venv\Scripts\Activate.ps1`
- Reinstall requirements: `pip install -r backend/requirements.txt`

### "Port 8000 already in use"
Change the backend port:
```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Then set the frontend API URL:
```powershell
$env:VITE_API_URL = "http://127.0.0.1:8001"
npm run dev
```

### "npm ERR! ..." in frontend
Clear and reinstall npm dependencies:
```powershell
cd frontend
rm -r node_modules package-lock.json
npm install
```

### "No module named 'deepface'" when starting Tauri app
The desktop app needs the backend to be running. Either:
1. Run the backend manually (Terminal 1 above) before launching the desktop app, or
2. Use the web app (Option A) instead.

### First recognition is slow
DeepFace downloads pre-trained models (~200 MB) on first use. Subsequent recognitions are fast. Be patient!

---

## Project Structure

```
face-recog-gallery/
├── backend/                  # FastAPI server
│   ├── main.py              # API endpoints
│   ├── requirements.txt      # Python dependencies
│   ├── db/                  # Local face gallery (auto-created)
│   └── sample_images/       # Temp uploads
├── frontend/                # React app
│   ├── src/
│   │   ├── App.tsx          # Main component
│   │   ├── main.tsx         # Entry point
│   │   └── styles.css       # Tailwind CSS
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── src-tauri/              # Desktop app (Tauri)
│   ├── src/main.rs         # Auto-starts Python backend
│   ├── Cargo.toml
│   └── tauri.conf.json
├── .venv/                  # Python virtual environment
├── README.md
├── QUICKSTART.md           # This file
└── dev-start.ps1           # Quick dev launcher script
```

---

## Development Notes

- **Backend**: Runs on `http://127.0.0.1:8000`
  - API Docs: `http://127.0.0.1:8000/docs` (interactive Swagger UI)
  - Reload on code change: enabled with `--reload` flag

- **Frontend**: Runs on `http://localhost:5173`
  - Hot module reloading (changes appear instantly)
  - Uses Vite for fast bundling

- **Desktop**: Tauri wraps the web app and bundles Python
  - Auto-launches Python backend on startup
  - Supports native OS integrations (file dialogs, system menu, etc.)

---

## Next Steps

1. Run the app using Option A or B above
2. Upload some test images
3. Add people to your gallery
4. Try detecting and recognizing faces
5. Customize the UI in `frontend/src/App.tsx`
6. Add new API endpoints in `backend/main.py`

Happy face recognizing! 🎉

