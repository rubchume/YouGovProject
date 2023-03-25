# Overview

This API is built using FastAPI and Pydantic.

The access to the database is handled by SQLAlchemy.

The dependency management is handled by Poetry.

# Installation

Create a virtual environment and install the dependencies by running
```bash
pip install -r requirements.txt
```
TODO: Right now there are more dependencies than needed. Clean up the dependencies.

# Usage

Execute the server by running
```bash
uvicorn app.api:app
```

and navigate to http://127.0.0.1:8000/docs to visualize the API.
