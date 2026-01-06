import os
from typing import Dict, Any

# Optional LangChain + Gemini
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_google_genai import ChatGoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = parser = prompt = None

if GEMINI_API_KEY and LANGCHAIN_AVAILABLE:
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
  "role": "MOST ACCURATE job title",
  "experience_level": "Intern/Junior/Mid/Senior",
  "skills": ["exact", "skills"],
  "summary": "2 sentences",
  "job_keywords": ["3-5 keywords"]
}

IMPORTANT: No assumptions.
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
# PUBLIC SERVICE API (BACKWARD COMPATIBLE)
# =====================================================
def analyze_resume(
    resume_text: str,
    desired_role: str | None = None,
    **_: Any,  # 🔥 Ignore legacy / unused keyword args safely
) -> Dict:
    """
    Analyze resume using Gemini if available, otherwise fallback.
    Accepts extra kwargs for backward compatibility.
    """
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
        "summary": data.get("summary", ""),
        "job_keywords": data.get("job_keywords", []),
    }


# =====================================================
# FALLBACK LOGIC
# =====================================================
def get_fallback_analysis(resume_text: str) -> Dict:
    text = resume_text.lower()

    if any(k in text for k in ["python", "developer", "flask"]):
        return {
            "role": "Software Developer",
            "experience_level": "Junior",
            "skills": ["Python", "Flask"],
            "summary": "Entry-level developer with programming experience.",
            "job_keywords": ["python developer", "junior developer"],
        }

    return {
        "role": "Professional",
        "experience_level": "Junior",
        "skills": ["Communication", "Teamwork"],
        "summary": "Motivated professional seeking opportunities.",
        "job_keywords": ["entry level", "junior"],
    }
