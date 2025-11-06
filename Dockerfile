# Use an official lightweight Node.js image
FROM node:20-slim

# Create and set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first (for better caching)
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of your source code
COPY . .

# Expose the port your app will listen on
EXPOSE 10000

# Start the backend
CMD ["node", "server.js"]
