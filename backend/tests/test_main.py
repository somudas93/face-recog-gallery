from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_gallery_status():
    r = client.get("/gallery")
    assert r.status_code == 200
    assert "gallery" in r.json()


def test_detect_invalid():
    r = client.post("/detect", files={"file": ("notanimage.txt", b"nope", "text/plain")})
    assert r.status_code in (400, 422) or "error" in r.json()


def test_add_face_missing_label():
    # should fail because label is required
    r = client.post("/add_face", files={"file": ("notanimage.txt", b"nope", "text/plain")})
    assert r.status_code == 422 or "error" in r.json()
