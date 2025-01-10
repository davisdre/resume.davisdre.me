# Drew Davis' Resume Application

This repository contains a three-tier application designed to showcase my resume. The application is containerized using Docker and consists of the following components:

## Architecture

1. **Frontend**: A static website built with HTML, CSS, and JavaScript, served by an Nginx container.
2. **Backend**: A Python FastAPI application that provides an API for visitor count, running in a separate container.
3. **Database**: A MariaDB database to store visitor counts, running in its own container.

## Repository Structure

- `src/frontend`: Contains the frontend code and Dockerfile.
- `src/backend`: Contains the backend code and Dockerfile.
- `infra`: Contains the Docker Compose file to orchestrate the containers.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
    ```sh
    git clone https://github.com/davisdre/resume.davisdre.me.git
    cd resume.davisdre.me
    ```

2. Build and start the containers:
    ```sh
    docker-compose -f infra/docker-compose.yml up --build
    ```

3. Access the application:
    - Frontend: `http://localhost`
    - Backend: `http://localhost:8000`
    - Database: `localhost:3306`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- Template by [StyleShout](https://www.styleshout.com/free-templates/ceevee/)
