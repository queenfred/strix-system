# 🧪 Estructura de Tests del Proyecto Strix

Este proyecto sigue una arquitectura de testing clara y escalable, separando los tests por módulo (`core`, `pipeline`, `security`) y por tipo (`unit`, `integration`, `e2e`).

---

## 📂 Estructura General

```
<root>/
├── core/
│   └── test/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── pipeline/
│   └── test/
│       ├── unit/
│       ├── integration/
│       └── e2e/
├── security/
│   └── test/
│       ├── unit/
│       ├── integration/
│       └── e2e/
```

---

## 🧩 Tipos de Tests

| Tipo           | ¿Qué prueba?                             | ¿Cómo se ejecuta?                           |
|----------------|-------------------------------------------|---------------------------------------------|
| `unit`         | Métodos de clases individuales (servicios/repos) usando mocks. | `pytest core/test/unit/` |
| `integration`  | Interacciones reales con BD o APIs.       | `pytest core/test/integration/` |
| `e2e`          | Flujos completos del usuario.             | `pytest core/test/e2e/` |


---

## ⚙️ Ajustar `pytest.ini`

Actualizá tu `pytest.ini` para buscar los tests en la carpeta nueva:

```ini
[pytest]
addopts = -ra -q
testpaths = 
    tests
python_files = test_*.py
```

---

## ▶ Cómo ejecutar tests

Desde la raíz del proyecto:

```bash
# Test unitarios
pytest core/test/unit/nombre del archivo  -v
pytest pipeline/test/unit/nombre del archivo  -v
pytest security/test/unit/nombre del archivo  -v

# Test de integración
pytest core/test/integration/nombre del archivo  -v

# Test de extremo a extremo (end-to-end)
pytest core/test/e2e/nombre del archivo  -v


Ejemplo

pytest core/test/unit/test_health_check.py  -v


```


```bash
O Desde ubicacion

pytest test_health_check.py -v
```


---

## ✅ Buenas prácticas

- **Nunca llames directamente a repositorios desde tests:** siempre a través de `services`.
- **Usá mocking profundo en `unit/`** (con `patch` o `MagicMock`)
- **Test integrados deben usar datos reales en una base controlada**
- **Los E2E deben validar flujos tal como los usaría un usuario final**
