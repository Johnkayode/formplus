# Formplus API

[![CI Status](https://github.com/johnkayode/formplus/workflows/test/badge.svg)](https://github.com/johnkayode/formplus/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Note: This project is a submission.

- **Framework**: Python/Flask
- **Database**: MongoDB

## Setup and Installation

1. Ensure Docker is installed on your machine.
2. Clone the repository:
    ```bash
    git clone https://github.com/johnkayode/formplus.git
    ```
3. Configure environment:
   ```bash
   cp .env.example .env
   ```
4. Build and run the services:
    ```bash
    docker-compose up --build
    ```
5. The API will be running on `http://localhost:5500` 

## API Documentation

Swagger Docs: [http://localhost:5500/swagger/ui](`http://localhost:5500/swagger/ui/#/`)

## Testing
Test environment is set up with Github Actions.
Run locally by setting up a test database and running the tests:

```bash
pytest
```

