# Project "Books"

This project provides an API for working with books. It allows you to manage books, their authors, genres, and other related data through a RESTful API. The project also supports authorization via OAuth.

## Technology stack

- **Python**: A programming language for implementing server-side logic.
- **Django**: A framework for developing web applications.
- **Django REST Framework**: A library for creating RESTful APIs in Django.
- **Docker**: For containerizing the application.
- **Poetry**: A dependency and virtual environment manager for Python.
- **Flake8**: A linter for checking code for compliance with PEP 8 standards.
- **PostgreSQL**: A relational database for storing project data.
- **OAuth**: An authorization protocol for secure access to the API.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Lokrip/books
cd books
```

2. Install dependencies using Poetry:


```bash
poetry install
```

3. Create and apply database migrations:

```bash
poetry run python manage.py migrate
```

## Authorization

The project supports OAuth authorization. Use your OAuth credentials to access the API.

## Running the Project with Docker

The project will soon support Docker for running the application in a containerized environment. Stay tuned for detailed instructions on setting up and running the project using Docker.