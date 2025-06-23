# 🧪 Scripts de Test - Strix System

Esta carpeta contiene los scripts automatizados para ejecutar los tests de API en diferentes entornos de desarrollo.

---

## 📂 Estructura

```
scripts/
├── run_selected_tests.ps1        # ✅ Versión limpia sin emojis ni codificación especial
├── start_selected_tests.ps1      # Ejecuta el anterior con permisos bypass
└── README_scripts.md             # Este archivo
```

---

## ✅ Requisitos

- Tener el entorno virtual `.venv` creado y activado
- Estar ubicado en la raíz del proyecto (`C:\Desarrollo\strix-system`)

---

## ▶ Cómo ejecutar

### PowerShell (seguro)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\scripts\run_selected_tests.ps1
```

### PowerShell con lanzador automático

```powershell
.\scripts\start_selected_tests.ps1
```


---

## ℹ️ Notas

- Se ejecutan tests de: `/users`, `/roles`, `/permissions`, `/access`
- El entorno virtual se activa automáticamente dentro de los scripts
- Podés editar estos scripts para agregar o quitar tests según tu necesidad



