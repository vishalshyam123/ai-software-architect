# Stage 1: Build React static assets with Vite
FROM node:20-alpine AS build

WORKDIR /app

# Copy package configurations
COPY package.json ./

# Install npm dependencies
RUN npm install --silent

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Serve with lightweight Nginx web server
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom reverse-proxy and SPA routing config
COPY nginx.conf /etc/nginx/conf.d/

# Copy built frontend assets
COPY --from=build /app/dist /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
