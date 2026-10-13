# MarketPulse

MarketPulse es una aplicación web interactiva que combina datos financieros en tiempo real con modelos predictivos entrenados en Python.  
Incluye un ticker animado estilo Bloomberg/CNBC, un sistema multilenguaje y un backend FastAPI que sirve predicciones basadas en vectores de mercado.

## Características principales

- Ticker financiero en tiempo real con animación continua.
- Predicciones de señales usando modelos entrenados en Colab.
- Frontend moderno (HTML, CSS, JS) con soporte multilenguaje.
- Backend FastAPI con endpoints REST para precios y predicciones.
- Arquitectura modular: routers, servicios, modelos, notebooks.
- Listo para deploy en Railway, Render, Netlify o Vercel.

## Estructura del proyecto

marketpulse/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── index.html
│   ├── routers/
│   │   ├── model_router.py
│   │   └── ticker_router.py
│   └── services/
│       ├── alpha_service.py
│       └── fmp_service.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   ├── translations.js
│   └── marketpulse-logo.png
│
├── notebooks/
│   ├── Financial_Data_Pipeline.ipynb
│   └── Model_Training_and_Evaluation.ipynb
│
└── colab/


## Modelos de predicción

Los modelos fueron entrenados en Google Colab usando:

- Ingeniería de features (Notebook 1)
- Entrenamiento y evaluación (Notebook 2)

Modelos exportados:

- model_reg.pkl
- model_clf.pkl
- scaler.pkl

El backend los carga mediante joblib.

## Endpoints del backend

### GET /ticker/
Devuelve precios actualizados de múltiples símbolos del mercado.

### POST /predict/
Entrada:
{
"features": [1.2, 3.4, 5.6],
"horizon": 5
}


Salida:
{
"prediction": "BUY"
}


## Cómo correr el backend
cd backend
uvicorn main:app --reload


## Cómo correr el frontend

Abrir:
frontend/index.html

O servirlo con cualquier hosting estático.


## Deploy

### Backend (Railway / Render)
1. Subir carpeta backend/
2. Instalar dependencias desde requirements.txt
3. Comando de inicio:
uvicorn main:app --host 0.0.0.0 --port 

### Frontend (Netlify / Vercel)
Subir carpeta frontend/.

## Licencia

Proyecto creado por Lycan (EABS).  
Uso educativo y experimental.
