# ==============================
# Base Image
# ==============================
FROM python:3.12-slim

# ==============================
# System Dependencies
# ==============================
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Environment
# ==============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ==============================
# Install Python dependencies
# ==============================
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# ==============================
# Copy application
# ==============================
COPY . .

# ==============================
# Expose port
# ==============================
EXPOSE 5000

# ==============================
# Run app
# ==============================
CMD ["python", "app.py"]
