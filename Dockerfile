FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential git libfreetype6-dev libpng-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords punkt

# Create directories with proper permissions before copying
RUN mkdir -p /app/uploads /app/graphs && \
    chmod -R 777 /app/uploads /app/graphs

COPY . /app

# Run as root to handle volume permissions properly
# The app will handle file creation with proper permissions
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
