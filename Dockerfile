# Use Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cortex/ ./cortex/
COPY web/ ./web/
COPY main.py .
COPY cortex_cli.py .
COPY examples/ ./examples/

# Create data directory
RUN mkdir -p /app/cortex_data

# Environment
ENV DATA_DIR=/app/cortex_data
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Start the web server
CMD ["python", "main.py"]
