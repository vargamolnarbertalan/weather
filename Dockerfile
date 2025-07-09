# Use a slim Debian-based Python image (Playwright-friendly)
FROM python:3.12-slim

# Set timezone and UTF-8 encoding
ENV TZ=Europe/Budapest
ENV PYTHONUNBUFFERED=1

# Install required system packages for Playwright
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    wget \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    libxshmfence1 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libglib2.0-0 \
    libudev1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps

# Set working directory
WORKDIR /app

# Copy app files
COPY server.py /app/

# Expose Flask port
EXPOSE 7123

# Start the Flask app
ENTRYPOINT ["python", "server.py"]