@echo off

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install requirements
pip install -r requirements.txt

:: Apply migrations
python manage.py makemigrations
python manage.py migrate

:: Run the development server
python manage.py runserver
