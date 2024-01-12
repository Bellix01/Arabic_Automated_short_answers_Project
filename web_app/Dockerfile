# Use the official Node.js image as the base image
FROM node:16-alpine as builder

# Set the working directory in the container
WORKDIR /app

COPY package.json ./

RUN npm install
# Copy the entire project to the working directory
COPY . .

RUN npm run build

# Use the official Nginx image as the base image for the final stage
FROM nginx:alpine

WORKDIR /usr/share/nginx/html
# Remove the default Nginx website
RUN rm -rf ./*

# Copy the built Angular app from the build stage to Nginx's web root
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
EXPOSE 443
# Start Nginx in the foreground
ENTRYPOINT ["nginx", "-g", "daemon off;"]

