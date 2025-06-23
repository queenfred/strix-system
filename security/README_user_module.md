# 🛡️ Módulo de Usuarios - `UserService` y `UserRepository`

Este módulo maneja el registro, autenticación y administración de usuarios, incluyendo su vinculación con roles y permisos.

---

## 📦 Estructura

```
security/
├── models/
│   └── user.py
├── data_access/
│   └── user_repository.py
├── services/
│   └── user_service.py
test/
├── unit/
│   └── test_user_service.py
```

---

## 🧠 Servicios disponibles (`UserService`)

- `register_user(username, email, password, full_name)`
- `authenticate(username, password)`
- `get_user(username)`
- `get_user_by_email(email)`
- `list_users()`
- `deactivate(user_id)`

Todos los métodos usan `SQLAlchemyUnitOfWork`.

---

## 🧪 Tests unitarios

Los tests se encuentran en:

📄 `security/test/unit/test_user_service.py`

Se utiliza `pytest` + `unittest.mock` con mocking profundo del `UnitOfWork`.

```bash
pytest security/test/unit/test_user_service.py -v
```

---

## 🔗 Integración con Roles y Permisos

- Al autenticar un usuario, se devuelven los roles y permisos asociados.
- Se recomienda utilizar `AccessControlService` para asignar roles y permisos.

---

## 🔄 Dependencias

- `SQLAlchemy`
- `bcrypt` (para encriptar/verificar contraseñas)
- `pytest`
- `unittest.mock`

---

## 🚀 Ejemplo de uso

```python
from security.services.user_service import UserService

service = UserService()
user = service.register_user("admin", "admin@example.com", "securepass", "Admin User")
auth = service.authenticate("admin", "securepass")
```

---

## 🛠️ Recomendación

Evitá acceder directamente al repositorio (`UserRepository`). Usá siempre `UserService` para respetar la arquitectura limpia.
