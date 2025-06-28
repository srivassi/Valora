# Use official Python image
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY backend/ backend/
COPY data/useful_database /app/data/useful_database
COPY data/clean_fundamentals.csv /app/data/clean_fundamentals.csv
COPY backend/requirements.txt /app/requirements.txt
COPY data/useful_database/ratios.csv /app/data/useful_database/ratios.csv

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.services.chatbot:app", "--host", "0.0.0.0", "--port", "8080"]