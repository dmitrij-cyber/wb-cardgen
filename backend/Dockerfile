FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt

# System deps for pillow & rembg (opencv libs not required here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libglib2.0-0 libgl1 libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

# Create data dir
RUN mkdir -p /app/data/assets /app/data/cutouts /app/data/composites /app/data/exports /app/data/backgrounds

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
