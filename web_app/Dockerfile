# Use an official Node.js runtime as a parent image
FROM node:16 as build

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./


# Copy the application code into the container
COPY . .

# Build the Angular app
RUN npm run build

# Use a lightweight image for the final stage
FROM nginx:alpine

# Copy the built app from the build stage
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# Expose the port that Nginx will run on
EXPOSE 80

# Command to start Nginx
CMD ["nginx", "-g", "daemon off;"]
