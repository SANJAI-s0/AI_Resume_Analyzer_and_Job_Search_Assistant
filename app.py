import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# =====================================================
# App Setup
# =====================================================
load_dotenv()

app = Flask(__name__, template_folder="templates")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# =====================================================
# Optional LangChain + Gemini
# =====================================================
langchain_available = False
llm = parser = prompt = None

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_google_genai import ChatGoogleGenerativeAI
    langchain_available = True
except Exception:
    langchain_available = False

if GEMINI_API_KEY and langchain_available:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=GEMINI_API_KEY,
            temperature=0.1,
            max_output_tokens=800,
        )

        parser = JsonOutputParser()

        system_template = """
Analyze this resume EXACTLY and return JSON:

{
  "role": "MOST ACCURATE job title from resume",
  "experience_level": "Intern/Junior/Mid/Senior",
  "skills": ["exact skills mentioned"],
  "summary": "2 sentences describing candidate",
  "job_keywords": ["3-5 keywords for job search"]
}

IMPORTANT:
- Do NOT assume skills
- Match resume content precisely
"""

        human_template = """
Desired role: {desired_role}

Resume:
{resume_text}
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", human_template),
        ])
    except Exception:
        llm = parser = prompt = None

# =====================================================
# Internal Imports (your architecture)
# =====================================================
from utils.pdf_utils import extract_text_from_pdf, ocr_available
from services.resume_analysis import get_fallback_analysis
from services.job_search import search_jobs
from database.db import init_db, save_analysis

# Initialize DB once
init_db()

# =====================================================
# Resume Analysis (AI or fallback)
# =====================================================
def analyze_resume(resume_text: str, desired_role: str | None) -> dict:
    if not (GEMINI_API_KEY and llm and prompt and parser):
        return get_fallback_analysis(resume_text)

    try:
        chain = prompt | llm | parser
        result = chain.invoke({
            "desired_role": desired_role or "",
            "resume_text": resume_text,
        })
        data = dict(result)
    except Exception:
        return get_fallback_analysis(resume_text)

    return {
        "role": data.get("role", "Professional"),
        "experience_level": data.get("experience_level", "Junior"),
        "skills": data.get("skills", []),
        "summary": data.get("summary", "Experienced professional"),
        "job_keywords": data.get("job_keywords", []),
    }

# =====================================================
# ROUTES
# =====================================================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["GET"])
def analyze_get():
    return jsonify({
        "message": "Use POST to submit resume analysis"
    }), 405

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    pdf_bytes = request.files["resume"].read()
    if not pdf_bytes:
        return jsonify({"error": "Empty file"}), 400

    # Extract text (OCR + fallback)
    resume_text = extract_text_from_pdf(pdf_bytes)
    if not resume_text:
        # 🔥 Allow fallback analysis even for broken PDFs
        resume_text = pdf_bytes.decode(errors="ignore")

    desired_role = request.form.get("desired_role", "").strip()
    city = request.form.get("city", "").strip()
    country = request.form.get("country", "IN").strip()
    remote_only = request.form.get("remote_only") == "on"

    # Analyze
    analysis = analyze_resume(resume_text, desired_role)

    # 🔥 Resume Score Logic (from old code)
    score = 75
    if len(analysis.get("skills", [])) >= 4:
        score += 15
    if desired_role and desired_role.lower() in resume_text.lower():
        score += 10
    score = min(100, score)

    # Job Search
    role_for_search = desired_role or analysis["role"]
    keywords = analysis.get("job_keywords") or analysis.get("skills", [])
    jobs = search_jobs(
        role_for_search,
        keywords,
        city,
        country,
        remote_only,
    )

    # 🔥 Suggested locations (India)
    suggested_locations = []
    if not jobs and country.lower() == "in":
        suggested_locations = [
            "Bangalore",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mumbai",
        ]

    # Save to DB
    save_analysis(analysis, score)

    return jsonify({
        "analysis": analysis,
        "jobs": jobs,
        "resume_score": score,
        "suggested_locations": suggested_locations,
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "gemini": bool(GEMINI_API_KEY and langchain_available),
        "ocr": ocr_available,
        "serpapi": bool(SERPAPI_KEY),
    })

# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
