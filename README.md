# CURSO-FastAPI

API REST construida con FastAPI aplicando autenticación con JWT, middlewares personalizados y modelos de datos, como práctica de desarrollo backend moderno en Python.

## Qué incluye

- Autenticación con JWT (`/login`) y protección de rutas con `HTTPBearer`.
- CRUD completo de un recurso (`/movies`) con validación de datos vía Pydantic (`Field`, longitudes, rangos).
- Persistencia con SQLAlchemy sobre SQLite.
- Manejo de errores centralizado con un middleware propio.

## Stack

Python, FastAPI, SQLAlchemy, PyJWT, Pydantic, Uvicorn.

## Cómo ejecutarlo

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

La documentación interactiva queda disponible en `http://localhost:8000/docs`.
