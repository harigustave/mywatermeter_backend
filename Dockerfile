# Use a base image that includes both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs20

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

RUN pip install numpy

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Python packages installed:" && python -m pip listpip list

# Install Node.js dependencies
RUN npm install

# Expose the port your Node.js backend uses
EXPOSE 10000

# Start your Node.js server
CMD ["npm", "start"]
