# 🚀 Strix System - API

Este proyecto utiliza **FastAPI** como capa de entrega para exponer servicios RESTful, incluyendo un endpoint de verificación de estado (`/health`) que chequea conectividad con PostgreSQL y S3.

---

## ✅ Requisitos previos

- Python 3.10+ instalado
- Git instalado
- Tener PostgreSQL accesible (y configurado en tu `.env`)
- Tener configurado AWS S3 (o MinIO) accesible
- Tener un entorno virtual (recomendado)

---

## ⚙️ Instalación del entorno

### 1. Clonar el proyecto

```bash
git clone https://tus-repos/strix-system.git
cd strix-system
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
.\.venv\Scripts\Activate   # En Windows
# source .venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecutar la API con Uvicorn

### 1. Navegar a la raíz del proyecto (donde está la carpeta `api/`)

```bash
cd C:\Desarrollo\strix-system
```

### 2. Ejecutar FastAPI

```bash
uvicorn api.main:app --reload
```

### 3. Verás algo como:

```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🔍 Probar `/health`

Abre tu navegador en:

```
http://localhost:8000/health
```

Si todo está correcto, verás una respuesta como:

```json
{
  "postgres": "OK",
  "s3": "OK"
}
```

---

## 📚 Documentación interactiva (Swagger)

También podés acceder a la documentación automática de FastAPI:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠 Archivos importantes

- `api/main.py`: Punto de entrada de la API
- `security/services/health_check.py`: Lógica de verificación de salud
- `core/infraestructure/uow/`: Unit of Work para manejar transacciones

---

## ✅ Tips

- Si `uvicorn` no es reconocido, asegurate de que tu entorno virtual está activado.
- Si el módulo `security` no se encuentra, agregá este snippet al inicio de `main.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

## 📦 Extra

Para generar `requirements.txt` automáticamente:

```bash
pip freeze > requirements.txt
```

O bien, si querés un archivo limpio:

```bash
pip install pipreqs
pipreqs ./ --force
```

---

Hecho con ❤️ por el equipo de Strix
