FROM python:latest
LABEL authors="uidon"
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR /uidon_backend

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /uidon_backend/requirements.txt
COPY . .
CMD gunicorn uidon_backend.config.wsgi:application -c gunicorn_config.py