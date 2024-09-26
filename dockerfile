FROM python:3.12.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080