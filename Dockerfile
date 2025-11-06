# Use a base image that includes both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs20

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

RUN pip install numpy

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "Python packages installed:" && pip list

# Install Node.js dependencies
RUN npm install

# Expose the port your Node.js backend uses
EXPOSE 10000

# Start your Node.js server
CMD ["npm", "start"]
