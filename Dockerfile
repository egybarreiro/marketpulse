FROM python:3.10-slim

WORKDIR /app

# Copiar requirements primero
COPY backend/requirements.txt /app/backend/requirements.txt

# Forzar reconstrucción de dependencias SIEMPRE
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copiar backend completo
COPY backend/ /app/backend/

# Copiar colab
COPY backend/colab/ /app/backend/colab/

# Copiar frontend
COPY frontend/ /app/frontend/

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
