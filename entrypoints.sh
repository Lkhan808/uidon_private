python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn -b 0.0.0.0:8000 config.wsgi --reload