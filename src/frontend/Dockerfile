# Dockerfile for Frontend
FROM nginxinc/nginx-unprivileged:stable-alpine

# Copy files
COPY index.html /usr/share/nginx/html/index.html
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY images /usr/share/nginx/html/images
COPY favicon-200x200.png /usr/share/nginx/html/favicon-200x200.png
COPY site.webmanifest /usr/share/nginx/html/site.webmanifest

# Expose port 8080 (default for nginx-unprivileged)
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]