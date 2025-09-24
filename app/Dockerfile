FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Healthcheck + fallback build tools (in case a wheel is missing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
COPY input_data /app/input_data
COPY static /app/static
COPY config /app/config
COPY routes /app/routes



EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=3s --retries=5 \
  CMD curl -fsS http://localhost:5000/healthz || exit 1

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]

