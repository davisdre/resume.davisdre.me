# Drew Davis' Resume Application

This repository contains a containerized web application designed to showcase my resume. The application is built with modern technologies and follows cloud-native practices.

## Architecture

1. **Frontend**: A modern static website built with HTML, CSS, and JavaScript, featuring a responsive design and visitor counter integration.
2. **Backend**: A Python Flask application that serves both the static frontend content and provides a RESTful API for the visitor counter functionality.
3. **Database**: An external MariaDB database to persistently store visitor counts.

## Repository Structure

- `src/frontend/`: Contains the frontend static files and Nginx configuration
- `src/backend/`: Contains the Flask application and requirements
- `.github/workflows/`: Contains CI/CD pipeline configurations

## Features

- Modern, responsive design
- Visitor counter functionality
- Docker containerization
- Automated CI/CD pipeline with GitHub Actions
- Container image publishing to Docker Hub

## Getting Started

### Prerequisites

- Docker
- Docker Compose (optional for local development)

### Running Locally

1. Clone the repository:
    ```sh
    git clone https://github.com/davisdre/resume.davisdre.me.git
    cd resume.davisdre.me
    ```

2. Configure environment variables:
    ```sh
    DATABASE_USER=my_resume
    DATABASE_PASSWORD=your_password
    DATABASE_HOST=your_database_host
    ```

3. Build and run the container:
    ```sh
    docker run -p 8000:8000 \
      -e DATABASE_USER=${DATABASE_USER} \
      -e DATABASE_PASSWORD=${DATABASE_PASSWORD} \
      -e DATABASE_HOST=${DATABASE_HOST} \
      davisdre/resume:latest
    ```

### Accessing the Application

- Web Interface: `http://localhost:8000`
- Visitor Counter API: `http://localhost:8000/visitors`

## Deployment

The application uses GitHub Actions for CI/CD:
- Automated builds triggered by version tags (v*.*.*)
- Container images are published to Docker Hub with version tags and 'latest'
- Built-in security features including SBOM generation and Docker provenance

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- Template by [StyleShout](https://www.styleshout.com/free-templates/ceevee/)
- Icons by [Font Awesome](https://fontawesome.com/)
