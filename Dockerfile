FROM python:3.10-slim

WORKDIR /app

COPY backend/ /app/backend/
COPY colab/ /app/colab/

RUN pip install --no-cache-dir -r /app/backend/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
