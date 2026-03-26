FROM python:3.12-bookworm

WORKDIR /app

RUN pip install gunicorn==23.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl openssl \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /app/static /app/logs \
 && chown -R root:root /app

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "watchmatch.wsgi"]