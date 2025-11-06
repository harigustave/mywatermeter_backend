# Use Python 3.10 slim
FROM python:3.10-slim

# Install Node.js 20 + build tools
RUN apt-get update && \
    apt-get install -y curl gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (enables Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "Installed packages:" && \
    python -m pip list | grep -E "numpy|opencv|torch|ultralytics|pillow"

# Copy the rest of the app
COPY . .

# Install Node.js dependencies
RUN npm install

# Expose port
EXPOSE 10000

# Start the app
CMD ["npm", "start"]