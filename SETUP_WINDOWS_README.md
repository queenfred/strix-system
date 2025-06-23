# Instrucciones de Configuración en Windows

Este README describe paso a paso cómo limpiar un entorno virtual existente, crear uno nuevo, e instalar y arrancar los módulos `core` y `security` de Strix System en Windows.

---

## 1. Cerrar procesos que usen la carpeta venv

Antes de modificar o eliminar el entorno virtual:

- Cierra cualquier intérprete de Python que esté usando `.venv` o `venv`.
- Cierra tu editor de código si lo tienes apuntando a esa carpeta.

## 2. Eliminar la carpeta venv vieja

Si existe una carpeta de entorno virtual con problemas, elimínala:

```powershell
Remove-Item -Recurse -Force .\.venv
```

> Si da error de permisos, abre PowerShell como **Run as Administrator**.

## 3. Crear el nuevo entorno virtual

Windows a veces bloquea nombres que empiezan por punto. Usaremos `venv`:

```powershell
python -m venv venv
```

(En lugar de `python`, usa `py -3` si tu comando por defecto no apunta a Python 3.)

## 4. Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

> Para desactivar, ejecuta `deactivate`.

## 5. Actualizar pip

Dentro del entorno activado, actualiza pip con:

```powershell
pip install --upgrade pip
```

## 6. Instalar dependencias del proyecto

```powershell
pip install -r requirements.txt
```

## 7. Instalar el paquete `core` en modo editable

```powershell
cd core
pip install -e .
cd ..
```

## 8. Instalar el paquete `security` en modo editable

```powershell
cd security
pip install -e .
cd ..
```

## 9. Verificar importaciones (opcional)

Puedes comprobar que ambos paquetes estén disponibles:

pip list


## 10. Arrancar el servicio de `security`

Si `security` expone una aplicación FastAPI (por ejemplo en `security/main.py`):

```powershell
uvicorn security.main:app --reload --host 0.0.0.0 --port 8000
```

Luego accede a tu navegador en `http://localhost:8000` (o el endpoint configurado) para verificar que el servicio esté en funcionamiento.

---

Con estos pasos tendrás un entorno limpio, el módulo `core` y `security` instalados en editable, y el servicio de seguridad corriendo de forma independiente en Windows.
