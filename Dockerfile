FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential git libfreetype6-dev libpng-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords punkt
RUN mkdir -p uploads
COPY . /app

# создаём непользовательского юзера
RUN groupadd -r app && useradd -r -g app app && chown -R app:app /app
USER app

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
