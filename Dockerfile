# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./
COPY server/package*.json ./server/
COPY client/package*.json ./client/

# Install dependencies for both frontend and backend
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the frontend React app
RUN cd client && npm run build

# Expose the ports for both frontend (3000) and backend (5000)
EXPOSE 3000 5000

# Start both frontend and backend servers
CMD ["npm", "start"]
