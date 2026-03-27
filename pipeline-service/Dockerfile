FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2 and dlt
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cache breaker to ensure latest code is copied
ARG CACHE_BUST=1
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
