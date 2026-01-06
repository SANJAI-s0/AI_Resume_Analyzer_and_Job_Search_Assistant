# AI Resume Analyzer & Job Finder 🚀

A Flask-based web application that analyzes resumes (PDF) using AI (Google Gemini via LangChain) and finds matching job opportunities using SerpAPI.  
If AI keys are not configured, the app gracefully falls back to smart heuristic-based analysis.

---

## ✨ Features

-   📄 Upload PDF resume
-   🤖 AI-powered resume analysis (role, experience, skills, summary)
-   💯 Resume score calculation
-   🔍 Job search via Google Jobs (SerpAPI)
-   🏙️ Location-based & remote job filtering
-   🖥️ Modern responsive frontend (HTML/CSS/JS)
-   🔄 Fallback mode when API keys are missing

---

## 🛠 Tech Stack

**Backend**

-   Python 3.12
-   Flask
-   LangChain
-   Google Gemini (Generative AI)
-   SerpAPI (Google Jobs)
-   pypdf (PDF parsing)

**Frontend**

-   HTML
-   CSS
-   JavaScript (Fetch API)

---

## 📁 Project Structure

```
job-search-assistant/
│
├── app.py                     # Flask app entry point
├── Dockerfile                 # OCR-ready Docker configuration
├── Makefile                   # Developer shortcuts (install, test, run)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── DATABASE.md                # Database design & notes
├── pytest.ini                 # Pytest config & warning filters
├── .env                       # Environment variables (ignored by git)
├── .gitignore                 # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
│
├── database/
│   └── db.py                  # SQLite connection & persistence logic
│
├── services/
│   ├── resume_analysis.py     # AI + fallback resume analysis service
│   └── job_search.py          # SerpAPI + mock job search service
│
├── utils/
│   ├── pdf_utils.py           # PDF + OCR extraction helpers
│   └── logging_config.py      # Centralized logging configuration
│
├── templates/
│   └── index.html             # Main frontend HTML (Flask template)
│
├── static/
│   ├── css/
│   │   └── style.css          # UI styling
│   └── js/
│       └── app.js             # Frontend logic (fetch, UI updates)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures (Flask test client, temp DB)
│   ├── test_analyze.py        # /analyze endpoint tests
│   ├── test_fallback_mode.py  # Fallback behavior tests (no API keys)
│   ├── test_health.py         # /health endpoint tests
│   └── test_resume_analysis_service.py
│                               # Resume analysis service unit tests
│
└── logs/
    └── app.log                # Application log output (runtime)
```

---

## ⚙️ Requirements

-   Python **3.12+**
-   pip
-   Virtual environment (recommended)
-   Google Gemini API Key (optional)
-   SerpAPI Key (optional)

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SANJAI-s0/AI_Resume_Analyzer_and_Job_Search_Assistant.git
cd AI_Resume_Analyzer_and_Job_Search_Assistant
```

### 2️⃣ Create & activate virtual environment

```windows
python -m venv .venv
.venvScriptsactivate
```

```macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Upgrade pip

```python
python -m pip install --upgrade pip setuptools wheel
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuration

### 1️⃣ Set up environment variables

Create a `.env` file in the project root (same level as `app.py`) and add your API keys:

```
GEMINI_API_KEY=your_google_gemini_api_key
SERPAPI_KEY=your_serpapi_api_key
FLASK_DEBUG=1
```

> **Notes:**
> 
> -   GEMINI_API_KEY → Enables AI resume analysis
> -   SERPAPI_KEY → Enables real job search
> -   If keys are missing, the app still works using fallback logic

### OCR System Dependency

For OCR to work, install Tesseract:

-   Windows: `https://github.com/UB-Mannheim/tesseract/wiki`
-   Linux: `sudo apt install tesseract-ocr`
-   macOS: `brew install tesseract`

### 2️⃣ (Optional) Configure SerpAPI

Sign up at [SerpAPI](https://serpapi.com/) to get your API key for job search functionality.

---

## 🚀 Running the Application

### 1️⃣ Start the Flask server

```bash
python app.py
```

### 2️⃣ Access the application

Open your web browser and navigate to

```
http://127.0.0.1:5000
```

**Health Check:**

```
http://127.0.0.1:5000/health
```

---

## 🧩 API Endpoints

```
| Method | Endpoint   | Description                 |
| ------ | ---------- | --------------------------- |
| GET    | `/`        | Frontend UI                 |
| POST   | `/analyze` | Analyze resume & fetch jobs |
| GET    | `/health`  | Service health check        |
```

---

## Docker Support

**▶ Build & Run**

```dockerfile
docker build -t job-search-assistant .
docker run -p 5000:5000 --env-file .env job-search-assistant
```

---

## 🧠 Fallback Mode (No AI Keys)

If API keys are missing:

-   Resume is analyzed using keyword heuristics
-   Mock job listings are returned
-   App remains fully functional for demos/testing
-   Fallback mode does NOT require internet access and is ideal for demos.

---

## 🐛 Troubleshooting

-   Ensure Python 3.12+ is installed
-   Verify virtual environment is activated
-   Check API keys in `.env` file
-   Review console logs for errors
-   Consult documentation for dependencies

1.  **Python version check**

```bash
python --version
# Must be 3.12.x
```

2.  **Virtual environment activation**

```bash
# Windows
.venvScriptsactivate
# macOS/Linux
source .venv/bin/activate
```

3.  **API key verification** Ensure `.env` file contains valid keys.
    
4.  . **Dependency installation**
    

```bash
pip install -r requirements.txt
```

5.  **Port already in use** Edit `app.py`:

```python
app.run(port=5001)
```

> **PDF text not extracted**
> 
> -   Text-based PDFs work automatically
> -   Scanned PDFs require OCR
> -   OCR works if `pytesseract` and `pdf2image` are installed
> -   Tesseract OCR engine must be installed on the system

---