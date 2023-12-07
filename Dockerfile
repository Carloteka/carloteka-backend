ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code

WORKDIR /code
COPY . /code
RUN rm -f db.sqlite3
RUN cp .env-example .env --remove-destination
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/

RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
RUN python manage.py generate_data_acc
RUN python manage.py generate_data_shop

EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]