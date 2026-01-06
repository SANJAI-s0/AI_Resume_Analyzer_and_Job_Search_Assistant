def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "ok"
    assert "gemini" in data
    assert "ocr" in data
    assert "serpapi" in data
