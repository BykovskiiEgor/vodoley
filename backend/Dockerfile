FROM python:3.10.7-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app/backend

COPY ./requirements.txt /app/backend

RUN apk update && apk add --no-cache build-base

RUN apk --no-cache add gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/backend

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "shop:application"]
