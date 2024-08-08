# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json ./
COPY server/package*.json ./server/
COPY client/package*.json ./client/

# Install dependencies for both frontend and backend
RUN npm install && npm install --prefix server && npm install --prefix client

# Copy the rest of the application files
COPY . .

# Build the frontend React app
RUN npm run build --prefix client

# Expose port 8080 (for Google Cloud Run)
EXPOSE 5000

# Start the server
CMD ["npm", "start", "--prefix", "server"]