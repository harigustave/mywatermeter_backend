FROM nikolaik/python-nodejs:python3.10-nodejs20

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r model/requirements.txt

# Install Node.js dependencies
RUN npm install

EXPOSE 10000
CMD ["npm", "start"]