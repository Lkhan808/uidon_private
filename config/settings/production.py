from decouple import config as env

DEBUG = env('DEBUG', cast=bool)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='0.0.0.0').split()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', cast=int),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    }
}

