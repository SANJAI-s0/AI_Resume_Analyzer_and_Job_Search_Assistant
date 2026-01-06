import os
import requests
from typing import List, Dict

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_mock_jobs(role: str, city: str) -> List[Dict]:
    """
    Fallback jobs when SerpAPI is unavailable.
    These links MUST be real so frontend never breaks.
    """
    return [
        {
            "title": f"Junior {role}",
            "company": "TechCorp India",
            "location": city or "India",
            "description": "Entry-level position. Freshers welcome. Training provided.",
            "url": f"https://www.naukri.com/{role.lower().replace(' ', '-')}-jobs",
            "source": "Mock",
        },
        {
            "title": f"{role} (Remote)",
            "company": "Global Solutions",
            "location": "Remote",
            "description": "Remote-friendly role. Great for early-career developers.",
            "url": f"https://www.linkedin.com/jobs/search/?keywords={role}",
            "source": "Mock",
        },
    ]


def search_jobs(
    role: str,
    keywords: list,
    city: str,
    country: str,
    remote_only: bool,
) -> List[Dict]:
    """
    Search jobs via SerpAPI Google Jobs.
    Robust URL extraction to prevent broken links.
    """

    if not SERPAPI_KEY:
        return get_mock_jobs(role, city)

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_jobs",
        "q": f"{role} {' '.join(keywords)}",
        "api_key": SERPAPI_KEY,
    }

    if city:
        params["l"] = f"{city}, {country}"

    if remote_only:
        params["location"] = "Remote"

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return get_mock_jobs(role, city)

    jobs = []

    for item in data.get("jobs_results", [])[:10]:
        # 🔥 FIX: job URLs are NOT always in `job_url`
        job_url = (
            item.get("job_url")
            or (item.get("related_links", [{}])[0].get("link"))
            or ""
        )

        # Detect source (optional but useful)
        source = "Company Site"
        if "linkedin.com" in job_url:
            source = "LinkedIn"
        elif "indeed.com" in job_url:
            source = "Indeed"
        elif "naukri.com" in job_url:
            source = "Naukri"

        jobs.append({
            "title": item.get("title", ""),
            "company": item.get("company_name", ""),
            "location": item.get("location", ""),
            "description": (item.get("description") or "")[:300],
            "url": job_url,
            "source": source,
        })

    # Absolute safety fallback
    return jobs or get_mock_jobs(role, city)
