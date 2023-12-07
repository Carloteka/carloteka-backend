ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt requirements.txt
COPY .env .env
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/
COPY . /code
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
RUN python manage.py generate_data

EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]