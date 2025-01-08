
# Backend (debt-manager-backend-fastapi)

- REST API using FastAPI with JWT Authentication
- Backend for TaqTaq Core results

## Features

- REST API with FastAPI and JWT Authentication.
- Backend for managing Regulatory Processing System results.

## Python Layer Model (Universal Reference Architecture)

```plaintext
.github/                # GitHub Actions configuration or other workflow settings
.vscode/                # Visual Studio Code-specific configuration
app/                    
    main.py             # Main application (entry point)
    configs/            # Configuration files
    models/             # Database and domain models
    controllers/        # API endpoints
    middlewares/        # HTTP Middlewares
    services/           # Business logic services
    repositories/       # Data persistence and access logic
    tests/              # Unit and integration tests
docs/                   # Project documentation
scripts/                # Automation scripts
.env                    # Environment variables file
docker-compose.yml      # Docker Compose file for multi-container configuration
Dockerfile              # Dockerfile for image building
requirements.txt        # Python dependencies
README.md               # Project description
```

## Main Technologies Used - API (Backend Microservices)

![Python](https://img.shields.io/badge/Python-3.10-%237159c1?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-%237159c1?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-4.1.8-%237159c1?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.3-%237159c1?style=for-the-badge&logo=postgresql)
![MongoDB](https://img.shields.io/badge/MongoDB-1.14.1-%237159c1?style=for-the-badge&logo=mongodb)

---

## Environment Prerequisites

- **Python**: Version 3.10 or higher
- **Docker**: Containerization
- **PostgreSQL**: Relational database
- **MongoDB**: NoSQL database
- **VSCode**: Code editor

---

## Environment Setup

### Download the application code

```bash
git clone https://github.com/your-repo/debt-manager-backend-fastapi.git
```

### Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Install Docker dependencies

```bash
docker-compose up --build
```

### Run the application locally

```bash
uvicorn app.main:app --reload
```

### Swagger URL

```plaintext
http://localhost:8000/docs
```

---

## Dependencies

Install dependencies in `requirements.txt`:

```plaintext
fastapi
uvicorn
python-jose
passlib[bcrypt]
pydantic
sqlalchemy
databases
```

### Additional Libraries

```plaintext
pytest
docker
```

---

## Docker Compose Configuration

```yaml
version: '3.9'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/code
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/debt_database
  db:
    image: postgres:15.3
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: debt_database
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
```

## Debug

Debugging can be done via VSCode:

![img-debug](docs/__img/img-debug.png)

## Access Mode: NoSQL, SQL and REST API

- Localhost: [Swagger local machine](http://127.0.0.1:8000/docs)
  ![img](docs/__img/img.png)

---

## Access

- **Swagger Documentation**: [Localhost Swagger](http://localhost:8000/docs)
- **MongoDB Compass**: [MongoDB Compass](https://www.mongodb.com/products/compass)
- **DBeaver PostgreSQL**: [DBeaver](https://dbeaver.io/)

---

## Multi-Cloud, On-Premises, and Data Center Environment List

- Development: `environment-dev`
- Staging: `environment-hml`
- QA: `environment-qa`
- Production: `environment-prod`

---
