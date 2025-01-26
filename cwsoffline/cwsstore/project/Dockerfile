# # Use an official Node.js runtime as a parent image
# FROM node:16 AS build

# # Set the working directory in the container
# WORKDIR /app

# # Copy the package.json and package-lock.json files to the container
# COPY package*.json ./

# # Install the dependencies
# RUN npm install

# # Copy the rest of the application files
# COPY . .

# CMD ["npm", "run", "dev"]

# # Build the React app for production
# # RUN npm run build

# # # Use a lightweight web server to serve the app
# # FROM nginx:alpine

# # # Copy the build folder from the build stage to the Nginx server's root folder
# # COPY --from=build /app/build /usr/share/nginx/html

# # # Expose port 80 for the Nginx server
# # EXPOSE 80

# # # Start Nginx when the container is run
# # CMD ["nginx", "-g", "daemon off;"]

# Use the official Node.js image as a base image
FROM node:16-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire React project into the working directory
COPY . .

# Build the React app for production
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Serve the React app using a lightweight HTTP server
RUN npm install -g serve

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]
