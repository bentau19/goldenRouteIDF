# Use node image as base
FROM node:18.13.0

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install axios
RUN npm install react

# Copy the rest of the application files
COPY . .

# Expose the port 3000
EXPOSE 3000

# Command to run the application
CMD [ "npm", "start" ]