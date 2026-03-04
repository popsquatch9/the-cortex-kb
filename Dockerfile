# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY cortex/ ./cortex/
COPY cortex_cli.py .
COPY .env.example .env

# Create data directory
RUN mkdir -p /app/cortex_data

# Set environment variables
ENV DATA_DIR=/app/cortex_data
ENV PYTHONUNBUFFERED=1

# Make CLI executable
RUN chmod +x cortex_cli.py

# Default command shows help
CMD ["python", "cortex_cli.py", "--help"]

# To run interactively: docker run -it cortex-kb bash
# To use: docker run -v $(pwd)/cortex_data:/app/cortex_data cortex-kb add document.md
