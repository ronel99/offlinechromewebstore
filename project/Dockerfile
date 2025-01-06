# Use an official Node.js runtime as a parent image
FROM node:16 AS build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app for production
RUN npm run build

# # Use a lightweight web server to serve the app
# FROM nginx:alpine

# # Copy the build folder from the build stage to the Nginx server's root folder
# COPY --from=build /app/build /usr/share/nginx/html

# # Expose port 80 for the Nginx server
# EXPOSE 80

# # Start Nginx when the container is run
# CMD ["nginx", "-g", "daemon off;"]
