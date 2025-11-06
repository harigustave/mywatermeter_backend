# Use a base image with Python 3.10 and Node.js 20
FROM nikolaik/python-nodejs:python3.10-nodejs20

# Set working directory
WORKDIR /app

# Copy project files
COPY package.json package-lock.json* ./
COPY requirements.txt ./
COPY server.js model.py testcodes.py ./

# Install Python dependencies first
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
RUN npm install

# Copy any other files (optional, if you have static resources)
COPY . .

# Expose backend port
EXPOSE 10000

# Start the Node server
CMD ["npm", "start"]
