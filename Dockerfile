# Dockerfile — Render-Proof
FROM python:3.10-slim

# Install Node.js
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# CRITICAL: Copy requirements FIRST
COPY requirements.txt /tmp/requirements.txt

# DEBUG: Show file exists
RUN echo "=== START DEBUG ===" && \
    ls -la /tmp/requirements.txt && \
    cat /tmp/requirements.txt && \
    echo "=== END DEBUG ==="

# INSTALL WITH FAIL-ON-ERROR
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt || \
    (echo "PIP INSTALL FAILED — CHECK ABOVE LOG" && exit 1)

# Verify imports
RUN python -c "import numpy, cv2, torch, ultralytics, PIL; print('ALL PACKAGES OK')"

# Copy app
COPY . .

# Install Node deps
RUN npm install

EXPOSE 10000
CMD ["npm", "start"]