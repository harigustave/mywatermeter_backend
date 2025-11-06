# Use official Python 3.10
FROM python:3.10-slim

# Install Node.js
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs build-essential && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Python packages installed inside Docker:" && python -m pip list

# Install Node.js dependencies
RUN npm install

# Expose port
EXPOSE 10000

# Start Node server
CMD ["npm", "start"]
