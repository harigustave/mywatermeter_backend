# Use a base image with Python 3.10 and Node.js 20
FROM nikolaik/python-nodejs:python3.10-nodejs20

# Set working directory
WORKDIR /app

# Copy only the requirements first (for caching)
COPY requirements.txt ./

# Upgrade pip, setuptools, wheel first
RUN python -m pip install --upgrade pip setuptools wheel

# Install Python dependencies from requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy Node dependencies files
COPY package.json package-lock.json* ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the app code
COPY . .

# Expose backend port
EXPOSE 10000

# Start Node server
CMD ["npm", "start"]
