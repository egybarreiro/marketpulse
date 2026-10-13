FROM python:3.10-slim

WORKDIR /app

# Fuerza reconstrucción de dependencias
COPY backend/requirements.txt /app/backend/requirements.txt

# Copia backend completo
COPY backend/ /app/backend/

# Copia colab
COPY backend/colab/ /app/backend/colab/

# Copia frontend
COPY frontend/ /app/frontend/

# Instala dependencias
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
