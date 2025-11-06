# Dockerfile — Render-Proof, Debug-Enabled, Fail-Fast
FROM python:3.10-slim

# Install Node.js 20 + build tools
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install OpenCV runtime dependencies (critical for cv2)
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt to a safe temp location
COPY requirements.txt /tmp/requirements.txt

# DEBUG: Confirm file exists and show content
RUN echo "=== DEBUG: requirements.txt FOUND ===" && \
    ls -la /tmp/requirements.txt && \
    cat /tmp/requirements.txt && \
    echo "=== END DEBUG ==="

# Upgrade pip and install Python packages with VERBOSE + FAIL ON ERROR
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --verbose -r /tmp/requirements.txt || \
    (echo "=== PIP INSTALL FAILED — SEE ABOVE LOG ===" && exit 1)

# Verify all required packages can be imported
RUN python -c "import numpy, cv2, torch, ultralytics, PIL; print('ALL PACKAGES IMPORTED SUCCESSFULLY!')"

# Copy the rest of the application
COPY . .

# Install Node.js dependencies
RUN npm install

# Expose port
EXPOSE 10000

# Start the server
CMD ["npm", "start"]