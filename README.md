# News API

This API created using Django and DRF.

# How to install
**Requirements**
* Python 3.6
* Docker (for PostgreSQL)

## Step by step

1. Fire up PostgreSQL using docker-compose `docker-compose up -d`
2. Install pipenv `pip install pipenv`
3. Install requirements `pipenv install` 
4. Run migrations `pipenv shell && python manage.py migrate`
5. Run the server `python manage.py runserver`
