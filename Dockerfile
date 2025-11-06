# Use a base image that includes both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs20

# Set working directory
WORKDIR /app

# Copy only requirement files first for caching
COPY requirements.txt ./

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Show installed packages clearly in logs
RUN echo "Installed Python packages:" && python -m pip list

# Copy the rest of your project files
COPY . .

# Install Node.js dependencies
RUN npm install

# Ensure Python path includes /app (important for Render)
ENV PYTHONPATH=/app

# Expose the port your Node.js backend uses
EXPOSE 10000

# Start your Node.js server
CMD ["npm", "start"]
