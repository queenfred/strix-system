# ✅ Test API - Strix System

Este proyecto incluye tests automatizados para verificar el correcto funcionamiento de los endpoints de la API construida con FastAPI.

---

## 📦 Requisitos

1. Tener el entorno virtual activado:

```bash
.\.venv\Scripts\Activate  # en Windows
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Tener corriendo una base de datos PostgreSQL válida con los datos necesarios para los tests:
   - Un usuario con ID = 1
   - Un rol con ID = 1
   - Un permiso con ID = 1
o similar
---

## 🧪 Ejecutar los tests

Desde la raíz del proyecto (`C:\Desarrollo\strix-system`):

```bash
pytest api/test/test_api_endpoints.py -v
pytest api/test/test_permissions.py -v
pytest api/test/test_access_control.py -v
```

---

## 📋 Qué prueba cada archivo

| Archivo                             | Endpoints que prueba                      |
|-------------------------------------|-------------------------------------------|
| `test_api_endpoints.py`             | `/health`, `/users`, `/roles`            |
| `test_permissions.py`              | `/permissions`                           |
| `test_access_control.py`           | `/access/assign-role`, `/access/assign-permission` |

---

## 🧠 Notas

- Si obtenés un error `ResponseValidationError`, asegurate de que las respuestas incluyan todos los campos requeridos por los schemas.
- Podés configurar datos en la base manualmente o agregar una carga inicial automática para entornos de prueba.

---

