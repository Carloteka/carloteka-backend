
# carloteka-backend

RESTful api backend for [carloteka.com](https://carloteka.com)

## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Authors

## Run Docker container

Clone the project

```bash
  git clone git@github.com:Carloteka/carloteka-backend.git -b dev
```

Go to the project directory

```bash
  cd carloteka-backend
```

#### Activate docker

Linux 

```bash
    sudo docker-compose up
```

Windows

```bash
    docker-compose up
```

Add ```--force-recreate``` to the end if you want to rebuild container

## Run Locally

Clone the project

```bash
  git clone git@github.com:Carloteka/carloteka-backend.git -b dev
```

Go to the project directory

```bash
  cd carloteka-backend
```

Create venv (on linux)

```bash
  python3 -m venv venv
```

Activate venv (on linux)

```bash
  source venv/bing/activate
```

Install requirements

```bash
  pip install -r requirements.txt
```
Before starting the server check the next section "Environment Variables" right below

Start the server

```bash
  python manage.py runserver
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file 

File direction /vscubing-backend/.env

```
export SECRET_KEY = 'django-key'

export DEBUG = 1 # 1 == True, 0 == False

export GOOGLE_REDIRECT_URL = 'http://127.0.0.1:3000'

export ALLOWED_HOSTS = '["127.0.0.1", "127.0.0.1:8000", "0.0.0.0:8000", "192.168.1.7"]'

export DEVELOPMENT = 1

export PRODUCTION = 0

#### only in production needed for database

export DB_NAME = dbname

export DB_USER = dbusername

export DB_PASSWORD = Password

```


## Run Tests
Go to the project directory

```bash
  cd carloteka-backend
```
Run tests:

```bash
  pytest
```

## Documentation

[API docs](/docs/api/README.md)

