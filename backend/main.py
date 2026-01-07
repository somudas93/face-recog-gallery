from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cv2
import numpy as np
import os
import io
from PIL import Image
import uuid
from deepface import DeepFace
from typing import List, Dict

DB_DIR = os.path.join(os.path.dirname(__file__), "db")
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_images")

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(SAMPLE_DIR, exist_ok=True)

app = FastAPI(title="Face Recognizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


async def read_imagefile(file: UploadFile) -> np.ndarray:
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")
    return img


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    """Detect faces and return bounding boxes (x, y, w, h)"""
    try:
        img = await read_imagefile(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        boxes = [dict(x=int(x), y=int(y), w=int(w), h=int(h)) for (x, y, w, h) in faces]
        return JSONResponse({"faces": boxes, "count": len(boxes)})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    """Recognize face(s) against the local gallery using DeepFace.find
    Returns the closest match or an empty list.
    """
    try:
        # Write the uploaded file to a temporary path
        contents = await file.read()
        tmp_filename = os.path.join(SAMPLE_DIR, f"upload-{uuid.uuid4().hex}.jpg")
        with open(tmp_filename, "wb") as f:
            f.write(contents)

        # Use DeepFace.find to search the local gallery
        # This will return a pandas DataFrame of potential matches
        results = DeepFace.find(img_path=tmp_filename, db_path=DB_DIR, enforce_detection=False)
        # results is a list of dataframes (for each model), default will be 1
        # If no matches, the dataframe is empty
        # Convert top results to JSON-friendly structure
        if isinstance(results, list) and len(results) > 0:
            df = results[0]
        else:
            df = results

        matches = []
        if hasattr(df, "values") and len(df) > 0:
            for _, row in df.iterrows():
                matches.append({
                    "identity": str(row.get("identity")),
                    "distance": float(row.iloc[1]) if len(row) > 1 else None,
                })

        # Clean up the temp file
        try:
            os.remove(tmp_filename)
        except Exception:
            pass

        return JSONResponse({"matches": matches})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/add_face")
async def add_face(file: UploadFile = File(...), label: str = Form(...)):
    """Add a face to the local gallery under a label
    Saves the uploaded image as `db/{label}/{uuid}.jpg`
    """
    try:
        # Ensure a clean label
        safe_label = label.replace("/", "_").strip()
        person_dir = os.path.join(DB_DIR, safe_label)
        os.makedirs(person_dir, exist_ok=True)
        contents = await file.read()
        filename = f"{uuid.uuid4().hex}.jpg"
        path = os.path.join(person_dir, filename)
        with open(path, "wb") as f:
            f.write(contents)
        return JSONResponse({"status": "ok", "path": path})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.get("/gallery")
async def gallery():
    """List names in the local gallery and count of images"""
    people = []
    try:
        for name in os.listdir(DB_DIR):
            p = os.path.join(DB_DIR, name)
            if os.path.isdir(p):
                count = len([x for x in os.listdir(p) if os.path.isfile(os.path.join(p, x))])
                people.append({"name": name, "count": count})
        return JSONResponse({"gallery": people})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
