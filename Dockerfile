FROM python:3.10-slim

WORKDIR /app

# Copiar backend completo
COPY backend/ /app/backend/

# Copiar colab dentro del backend (ruta correcta)
COPY backend/colab/ /app/backend/colab/

# Copiar frontend (si lo sirves desde FastAPI)
COPY frontend/ /app/frontend/

# Instalar dependencias
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

EXPOSE 8080

# Ejecutar FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
