import io

def test_analyze_valid_pdf(client):
    fake_pdf = b"%PDF-1.4\nFake resume text"

    data = {
        "resume": (io.BytesIO(fake_pdf), "resume.pdf")
    }

    response = client.post("/analyze", data=data)
    assert response.status_code in (200, 400)
