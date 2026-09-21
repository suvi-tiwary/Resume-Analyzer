# Resume Analyzer Backend

FastAPI service for extracting and parsing resume information from PDFs and images into structured JSON.

## Features

- **Document Ingestion**: Supports PDF (`application/pdf`) and Images (`JPG`, `JPEG`, `PNG`).
- **Direct PDF Text Extraction**: High-performance in-memory extraction using PyMuPDF (`pymupdf`) with fallback to `pypdf`.
- **OCR Integration**: Dedicated OCR service utilizing Tesseract for scanned PDFs and image files with graceful degradation and error handling.
- **Rule-based Parser**: Extracts Name, Email, Phone, and Technical Skills using regex and dictionary matching.
- **Consistent Response Schema**: Predictable Pydantic data model with empty defaults (no unexpected `null` values).
- **CORS Configured**: Ready for local React + Vite frontend (`http://localhost:5173`).
- **Swagger / OpenAPI**: Auto-generated interactive documentation at `/docs`.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint & CORS
│   ├── routes/
│   │   ├── __init__.py
│   │   └── resume.py            # POST /api/resume/parse
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py     # In-memory text extraction from PDFs
│   │   ├── ocr_service.py       # Tesseract OCR for images & scanned PDFs
│   │   └── resume_parser.py     # Rule-based resume structuring
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── resume.py            # Consistent Pydantic response models
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # File type, size, and presence validation
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Running Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Optional)* If you plan to parse scanned PDFs or image uploads, ensure [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) is installed and available in your system `PATH` or set `TESSERACT_CMD` in `.env`.

### 2. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 3. Run the Development Server

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

Server will start on: `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status message |
| `GET` | `/health` | Service health check |
| `POST` | `/api/resume/parse` | Parse uploaded resume (PDF/JPG/PNG) |
| `GET` | `/docs` | Interactive Swagger documentation |
| `GET` | `/redoc` | OpenAPI ReDoc documentation |

### Response Schema (`POST /api/resume/parse`)

```json
{
  "name": "Rishav Gupta",
  "email": "rishav.gupta@example.com",
  "phone": "+91 98765 43210",
  "skills": ["Python", "FastAPI", "React", "Docker", "Git"],
  "education": [
    {
      "degree": "B.Tech",
      "institution": "ABC Institute of Technology",
      "field": "Computer Science",
      "start_year": "2024",
      "end_year": "2028"
    }
  ],
  "work_experience": [
    {
      "job_title": "Software Developer Intern",
      "company": "XYZ Technologies",
      "start_date": "June 2026",
      "end_date": "August 2026",
      "description": "Worked on web applications, REST APIs and frontend integration."
    }
  ]
}
```
