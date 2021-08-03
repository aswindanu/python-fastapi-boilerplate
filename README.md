# FastAPI (PostgreSQL)

## Prequisitions

What need to be installed in this project are:

    python
    pip
    mysql
    virtualenv
    docker (optional)

Technology that used for development are:

- Programming Language : `Python 3.7.2`
- Framework : `FastAPI v0.63.0`
- Database : `MySQL`
- Documentation API : `Swagger/postman`


## This project using this kind of library:

* API Framework : 
    
    FastAPI : https://fastapi.tiangolo.com/

* ORM : https://flask-sqlalchemy.palletsprojects.com/en/2.x/
* Configs : https://pypi.org/project/python-dotenv/
* Logging : https://docs.sentry.io/platforms/python/


#### How to Start Project

1. Clone this project:
    ```
    git clone https://github.com/aswindanu/python-fastapi-starter
    ```

2. Create env:
    ```
    python -m venv env
    ```

3. Activate ENV (Linux/OSX):
    ```
    source env/bin/activate
    ```

4. Go to dir project:
    ```
    cd python-fastapi-starter
    ```

4. install requirements:
    ```
    pip install -r requirements.txt
    ```

5. Create .env in root project:
    ```
    touch .env
    ```

6. configure env in .env file

    - DEBUG=True
    - SECRET_KEY=`your-jwt-secret`
    - SENTRY_URL=`your-sentry-url`
    - DATABASE_USER=`username`
    - DATABASE_PASSWORD=`password`
    - DATABASE_HOST=127.0.0.1
    - DATABASE_PORT=3306
    - DATABASE_NAME=`database-name`

7. set PYTHONPATH env(Linux/OS) or Windows:
    ```
    export PYTHONPATH=.
    ```

    or

    ```
    $Env:PYTHONPATH="."
    ```

8. migrate the database:
    ```
    alembic revision --autogenerate -m "First migration"
    ```

9. upgrade database:
    ```
    alembic upgrade head
    ```

10. run the program (using Uvicorn ASGI):
    
    ```
    uvicorn main:app --reload
    ```

NOTE :
    For every additional __crud__, please update `crud/__init__.py`
    For every additional __model__, please update `models/__init__.py`
    For every additional __schemas__, please update `schemas/__init__.py`

## Swagger collection
Collection & environment of Swagger can be accessed from this listed endpoint

    https://127.0.0.1:8000/docs


#### Run with Docker Compose
```docker-compose up```


#### Update requirements (virtualenv only)
```pip freeze -l > requirements.txt```


#### OTHER

Check databse heroku : https://stackoverflow.com/questions/5951105/heroku-database-url

```python3.9
# Usage of * and / in code
def combined_example(pos_only, /, standard, *, kwd_only):
     print(pos_only, standard, kwd_only)
```

For more documentation, see docs in this listed link below

- FastAPI : https://fastapi.tiangolo.com/
- Git Repo (backend) : https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app

