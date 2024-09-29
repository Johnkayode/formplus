# Formplus API

[![CI Status](https://github.com/Johnkayode/formplus/actions/workflows/test.yml/badge.svg)](https://github.com/Johnkayode/formplus/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> [!NOTE]
> This project is a submission.

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
   cp .env.template .env
   ```
4. Build and run the services:
    ```bash
    docker-compose up --build
    ```
5. The API will be running on `http://localhost:5500` 

## API Documentation
Swagger Docs: [http://localhost:5500/swagger/ui](http://localhost:5500/swagger/ui/#/)

## Testing
Test environment is set up with Github Actions.
Run locally by setting up a test database and running the tests:

```bash
pytest
```

## Examples
- **Create A New Form**: `POST /forms/`\
  Request Body:
    ```json
    {
        "title": "Sample Form",
        "description": "Sample Description",
        "metadata": {
            "theme": "#000000"
        },
        "quota": 1000,
        "sections": [
            {
                "title": "Section A",
                "description": "Description",
                "fields": [
                    {
                    "description": "",
                    "field_type": "short_text",
                    "label": "First Name",
                    "required": true
                    },
                    {
                    "description": "",
                    "field_type": "short_text",
                    "label": "Last Name",
                    "required": true
                    },
                    {
                    "description": "Gender",
                    "field_type": "dropdown",
                    "label": "Gender",
                    "options": ["Male", "Female", "Other"],
                    "required": true
                    }
                ]
            }
        ]
    }
    ```
- **Submit response to a form**: `POST /forms/{form-id}/submit`\
  Request Body:
    ```json
    {
        "sections": {
            "section_id": {
                "field_id_1": "Dwight",
                "field_id_2": "Shrute",
                "field_id_3": 0
            }
        }
    }
    ```

