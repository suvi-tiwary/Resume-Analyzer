import io
import pymupdf
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("--- Running Resume Analyzer Backend Test Suite ---")

    # Test 1: GET /
    r1 = client.get("/")
    assert r1.status_code == 200, f"GET / failed: {r1.status_code}"
    assert r1.json() == {"message": "Resume Analyzer API is running", "status": "ok"}
    print("[OK] PASS: GET / returns status ok")

    # Test 2: GET /health
    r2 = client.get("/health")
    assert r2.status_code == 200, f"GET /health failed: {r2.status_code}"
    assert r2.json() == {"status": "healthy"}
    print("[OK] PASS: GET /health returns healthy")

    # Test 3: GET /openapi.json & Swagger docs
    r3 = client.get("/openapi.json")
    assert r3.status_code == 200
    schema = r3.json()
    assert "/api/resume/parse" in schema["paths"], "Route /api/resume/parse missing from OpenAPI"
    print("[OK] PASS: OpenAPI contains /api/resume/parse")

    # Test 4: Empty file validation
    r4 = client.post("/api/resume/parse", files={"file": ("empty.pdf", b"", "application/pdf")})
    assert r4.status_code == 400
    assert "empty" in r4.json()["detail"].lower()
    print("[OK] PASS: Empty file rejected with HTTP 400")

    # Test 5: Unsupported file extension (.txt)
    r5 = client.post("/api/resume/parse", files={"file": ("resume.txt", b"some text", "text/plain")})
    assert r5.status_code == 400
    assert "unsupported" in r5.json()["detail"].lower()
    print("[OK] PASS: Unsupported file type rejected with HTTP 400")

    # Test 6: Text-based PDF extraction and parsing
    doc = pymupdf.open()
    page = doc.new_page()
    sample_text = (
        "Rishav Gupta\n"
        "rishav.gupta@example.com\n"
        "+91 98765 43210\n\n"
        "Skills:\n"
        "Python, FastAPI, React, Docker, Git, SQL, Machine Learning\n\n"
        "Education:\n"
        "B.Tech in Computer Science\n"
        "ABC Institute of Technology 2024 - 2028\n"
    )
    page.insert_text((50, 72), sample_text, fontsize=12)
    pdf_bytes = doc.tobytes()
    doc.close()

    r6 = client.post(
        "/api/resume/parse",
        files={"file": ("rishav_resume.pdf", pdf_bytes, "application/pdf")}
    )
    assert r6.status_code == 200, f"PDF parse failed: {r6.text}"
    data = r6.json()
    print("Parsed PDF Result:", data)
    assert data["name"] == "Rishav Gupta", f"Expected 'Rishav Gupta', got {data['name']}"
    assert data["email"] == "rishav.gupta@example.com"
    assert "98765" in data["phone"]
    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]
    assert "React" in data["skills"]
    assert isinstance(data["education"], list)
    assert isinstance(data["work_experience"], list)
    print("[OK] PASS: Digital PDF parsed into structured JSON successfully!")

    # Test 7: Image upload handling (PNG)
    img = Image.new("RGB", (200, 100), color=(255, 255, 255))
    img_buf = io.BytesIO()
    img.save(img_buf, format="PNG")
    img_bytes = img_buf.getvalue()

    r7 = client.post(
        "/api/resume/parse",
        files={"file": ("resume.png", img_bytes, "image/png")}
    )
    assert r7.status_code in (200, 422), f"Unexpected status: {r7.status_code} -> {r7.text}"
    print(f"[OK] PASS: Image upload handled gracefully (Status: {r7.status_code})")

    print("\n--- ALL BACKEND TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()
