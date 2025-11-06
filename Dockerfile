# Dockerfile — Render-Optimized + Debug
FROM python:3.10-slim


# Install Node.js 20
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# COPY requirements.txt FIRST
COPY requirements.txt .

# DEBUG: Show file exists and content
RUN echo "=== requirements.txt FOUND ===" && \
    ls -la requirements.txt && \
    cat requirements.txt && \
    echo "=== END DEBUG ==="

# INSTALL WITH VERBOSE + FAIL ON ERROR
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --verbose -r requirements.txt || \
    (echo "PIP INSTALL FAILED" && exit 1)

# Verify installation
RUN python -c "import numpy, cv2, torch, ultralytics, PIL; print('ALL PACKAGES LOADED!')" && \
    echo "INSTALLED PACKAGES:" && \
    python -m pip list | grep -E "numpy|opencv|torch|ultralytics|pillow"

# Now copy the rest
COPY . .

# Install Node deps
RUN npm install

EXPOSE 10000
CMD ["npm", "start"]