import io


def test_fallback_without_keys(client, monkeypatch):
    # Remove API keys
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("SERPAPI_KEY", raising=False)

    fake_pdf = b"%PDF-1.4\nPython developer resume"

    data = {
        "resume": (io.BytesIO(fake_pdf), "resume.pdf")
    }

    response = client.post("/analyze", data=data)

    # ✅ Must succeed in fallback mode
    assert response.status_code == 200

    payload = response.get_json()

    # ✅ Core keys must exist
    assert "analysis" in payload
    assert "resume_score" in payload
    assert "jobs" in payload

    analysis = payload["analysis"]

    # ✅ Fallback logic validation
    assert analysis["role"] == "Software Developer"
    assert "Python" in analysis["skills"]
