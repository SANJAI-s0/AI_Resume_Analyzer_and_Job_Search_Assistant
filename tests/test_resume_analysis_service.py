from services.resume_analysis import analyze_resume


def test_service_fallback_without_key():
    result = analyze_resume(
        resume_text="Python Flask developer",
        desired_role="",
        gemini_api_key=None,
    )

    assert result["role"] == "Software Developer"
    assert "Python" in result["skills"]
