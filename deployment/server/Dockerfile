FROM python:3.9-slim

LABEL maintainer="JJshome <jjshome@github.com>"
LABEL description="AI-PsychDoodle-Analyzer Server"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY deployment/server/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY deployment/server/config.yml /app/config.yml
COPY deployment/server/server_config.py /app/server_config.py
COPY deployment/server/gunicorn_conf.py /app/gunicorn_conf.py

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/models/weights

# Set environment variables
ENV PYTHONPATH=/app
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8000
ENV SERVER_WORKERS=4
ENV SERVER_LOG_LEVEL=info
ENV API_REQUIRE_KEY=false
ENV USE_GPU=false

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "-c", "gunicorn_conf.py", "src.api.server:app"]