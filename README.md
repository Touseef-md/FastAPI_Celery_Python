# FastAPI Celery Project

This project demonstrates the integration of FastAPI, Celery, and Redis for background task processing.

## Project Structure

- `alembic`: Alembic-related files for database schema migrations.
- `app`: Main application logic, including FastAPI, Celery, and database configurations.
- `gemini`: Gemini-related functionalities.
- `reviews`: Review-related APIs.
-  `db.sqlite3`: SQLite database

## Step by Step Guide

Run the following commands from the project's root directory:

1. Make a python virtual environment with python version >=3.10
    ``` bash
    python3.10 -m venv myenv
    ```

2. Activate the python virtual environment
    ``` bash
    source myenv/bin/activate
    ```

3. Install the required packages:
    ``` bash
    pip install -r requirements.txt
    ```
4. Install Redis on your system. You can follow instructions given here [here](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/)

5. Change the `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` variables inside the /app/config.py file accordingly.

6. Migrate the Alembic database:

    `Whenever you make changes to your database schema, you need to migrate` 
    ``` bash
    alembic revision --autogenerate

    alembic upgrade head
    ```

    If alembic is not initialized, you need to initialize and configure Alembic:

    ```bash
    alembic init alembic
    ```

    Update alembic/env.py:

    ```python

        from app import create_app
        from app.config import settings
        from app.database import Base
        
        config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL)) # set the database connection string

        fastapi_app = create_app() # instance to ensure the relevant models are loaded

        target_metadata = Base.metadata #new models are discovered by Alembic
    ```
    After this, migrate the database.


    
6. Start the Celery worker:
    ``` bash
    celery -A main.celery worker --loglevel=info
    ```

6. Start the Flower monitoring tool (optional):
    ``` bash
    celery -A main.celery flower --port=5555
    ```

7. Add your Gemini API_KEY to the `/app/gemini/__init__.py` file.


8. Run the FastAPI application:
    ``` bash
    uvicorn main:app --reload
    ```