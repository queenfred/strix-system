# 🚀 Strix Portfolio Pipeline CLI

Pipeline de procesamiento de eventos de portfolios con soporte para ejecución paralela y CLI avanzado.

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Instalación](#-instalación)
- [Uso Básico](#-uso-básico)
- [Configuración de Fechas](#-configuración-de-fechas)
- [Modos de Procesamiento](#-modos-de-procesamiento)
- [Opciones Avanzadas](#-opciones-avanzadas)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Scripts de Automatización](#-scripts-de-automatización)
- [Troubleshooting](#-troubleshooting)
- [Métricas y Rendimiento](#-métricas-y-rendimiento)

## 🎯 Descripción General

El Strix Portfolio Pipeline procesa eventos de portfolios almacenados en S3 y los inserta en PostgreSQL, con capacidades de procesamiento paralelo para mejorar el rendimiento.

### Características principales:

- ✅ **Procesamiento paralelo** con auto-detección de workers óptimos
- ✅ **CLI completo** con múltiples opciones de configuración
- ✅ **Flexibilidad de fechas** (rangos específicos, días relativos, hoy/ayer)
- ✅ **Modos de ejecución** (auto, paralelo, estándar)
- ✅ **Validación robusta** de argumentos y conexiones
- ✅ **Métricas detalladas** de rendimiento
- ✅ **Modo dry-run** para testing sin procesamiento real

## 🔧 Instalación

### Prerrequisitos

1. **Python 3.8+**
2. **PostgreSQL** configurado y accesible
3. **AWS S3** con credenciales configuradas
4. **Entorno virtual** activado

### Pasos de instalación

```bash
# 1. Clonar el repositorio y navegar al proyecto
cd C:\code\strix-system

# 2. Activar entorno virtual
.\venv\Scripts\Activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
cd pipeline
python main.py --show-config
```

### Dependencias principales

```txt
# Core
sqlalchemy==2.0.29
psycopg2-binary==2.9.9
boto3==1.34.79
pandas==2.2.3

# Paralelización
psutil==6.0.0

# API (si se usa)
fastapi==0.110.0
uvicorn==0.29.0
```

## 🚀 Uso Básico

### Ejecución simple

```bash
# Navegar al directorio pipeline
cd pipeline

# Activar entorno virtual
..\venv\Scripts\Activate

# Ejecutar con configuración por defecto
python main.py
```

### Verificar configuración

```bash
# Ver configuración del sistema
python main.py --show-config

# Listar portfolios activos
python main.py --list-portfolios

# Ver ayuda completa
python main.py --help
```

## 📅 Configuración de Fechas

### Opciones disponibles

```bash
# Fechas específicas
python main.py --start 2025-04-30 --end 2025-05-01

# Últimos N días
python main.py --days 7

# Solo eventos de hoy
python main.py --today

# Solo eventos de ayer
python main.py --yesterday

# Por defecto (sin argumentos): procesa desde ayer hasta hoy
python main.py
```

### Formato de fechas

- **Formato requerido**: `YYYY-MM-DD`
- **Ejemplos válidos**: `2025-04-30`, `2025-12-01`
- **Zona horaria**: UTC

## ⚡ Modos de Procesamiento

### Tipos de procesador

| Modo | Descripción | Cuándo usar |
|------|-------------|-------------|
| `auto` | Auto-detecta el mejor procesador disponible | **Recomendado** para uso general |
| `parallel` | Fuerza el uso del procesador paralelo | Para grandes volúmenes de datos |
| `standard` | Usa el procesador estándar (single-thread) | Para debugging o sistemas limitados |

### Configuración de workers

```bash
# Auto-detectar workers óptimos (recomendado)
python main.py --mode parallel

# Especificar número de workers
python main.py --mode parallel --workers 4

# Forzar modo de ejecución
python main.py --mode parallel --execution-mode thread
```

### Modos de ejecución paralela

- **`auto`**: Detecta automáticamente (thread para I/O, process para CPU)
- **`thread`**: ThreadPoolExecutor (recomendado para operaciones I/O como S3/DB)
- **`process`**: ProcessPoolExecutor (para operaciones CPU intensivas)

## 🔧 Opciones Avanzadas

### Información del sistema

```bash
# Ver configuración completa del sistema
python main.py --show-config

# Listar todos los portfolios
python main.py --list-portfolios

# Ver versión
python main.py --version
```

### Opciones de ejecución

```bash
# Modo verbose (información detallada)
python main.py --verbose

# Modo quiet (solo información esencial)
python main.py --quiet

# Simulación sin procesamiento real
python main.py --dry-run

# Saltar verificación de conexiones
python main.py --skip-health-check

# Continuar aunque falle la verificación
python main.py --force
```

### Procesamiento selectivo

```bash
# Procesar portfolios específicos
python main.py --portfolio-ids 1,2,3

# Combinar con otras opciones
python main.py --portfolio-ids 1,5 --days 3 --verbose
```

## 📚 Ejemplos de Uso

### Casos comunes

#### Procesamiento diario básico
```bash
python main.py --yesterday --mode parallel
```

#### Reprocesar un periodo específico
```bash
python main.py --start 2025-06-01 --end 2025-06-15 --mode parallel --verbose
```

#### Testing y debugging
```bash
# Simulación completa
python main.py --dry-run --verbose --show-config

# Procesar un portfolio específico con detalles
python main.py --portfolio-ids 1 --days 1 --verbose
```

#### Ejecución en producción
```bash
# Silenciosa para scripts automatizados
python main.py --days 1 --mode parallel --quiet

# Con validación completa
python main.py --days 1 --mode parallel --verbose
```

### Análisis de rendimiento

```bash
# Comparar modos de procesamiento
python main.py --days 1 --mode standard --verbose
python main.py --days 1 --mode parallel --verbose

# Probar diferentes configuraciones de workers
python main.py --days 1 --workers 2 --verbose
python main.py --days 1 --workers 4 --verbose
python main.py --days 1 --workers 8 --verbose
```

## 🤖 Scripts de Automatización

### Scripts Windows (.bat)

#### `run_pipeline_cli.bat` - Menú interactivo
```batch
@echo off
call venv\Scripts\activate.bat
cd pipeline

echo Selecciona una opción:
echo [1] Procesamiento básico
echo [2] Últimos 7 días paralelo
echo [3] Dry-run con detalles
set /p choice="Opción: "

if "%choice%"=="1" python main.py
if "%choice%"=="2" python main.py --days 7 --mode parallel --verbose
if "%choice%"=="3" python main.py --dry-run --verbose
```

#### `daily_pipeline.bat` - Ejecución diaria
```batch
@echo off
call venv\Scripts\activate.bat
cd pipeline
python main.py --yesterday --mode parallel --quiet
```

#### `quick_test.bat` - Testing rápido
```batch
@echo off
call venv\Scripts\activate.bat
cd pipeline
python main.py --dry-run --show-config
```

### Scripts para Linux/Mac

#### `run_pipeline.sh`
```bash
#!/bin/bash
source venv/bin/activate
cd pipeline
python main.py "$@"
```

#### `daily_pipeline.sh`
```bash
#!/bin/bash
source venv/bin/activate
cd pipeline
python main.py --yesterday --mode parallel --quiet
```

### Cron Jobs

```bash
# Ejecutar diariamente a las 2 AM
0 2 * * * cd /path/to/strix-system && ./daily_pipeline.sh

# Ejecutar cada hora durante el día laborable
0 9-17 * * 1-5 cd /path/to/strix-system && python pipeline/main.py --today --quiet
```

## 🔍 Troubleshooting

### Problemas comunes y soluciones

#### Error de importación de módulos
```bash
# Verificar configuración
python main.py --show-config

# Reinstalar módulos en modo editable
cd ..
pip install -e core -e security -e pipeline
cd pipeline
```

#### Problemas de conexión
```bash
# Verificar conexiones
python main.py --show-config

# Saltar verificación temporalmente
python main.py --skip-health-check --force

# Verificar variables de entorno
echo $DATABASE_URL
echo $AWS_ACCESS_KEY_ID
```

#### Errores de permisos (Windows)
```bash
# Ejecutar como administrador
# O usar --force para continuar
python main.py --force
```

#### Problemas de rendimiento
```bash
# Verificar configuración del sistema
python main.py --show-config

# Probar con menos workers
python main.py --workers 2

# Usar modo estándar si hay problemas
python main.py --mode standard
```

### Códigos de salida

- **0**: Ejecución exitosa
- **1**: Error en ejecución o validación de argumentos

### Logs y debugging

```bash
# Máximo detalle de información
python main.py --verbose

# Información específica del sistema
python main.py --show-config --verbose

# Simulación para debug sin procesamiento
python main.py --dry-run --verbose
```

## 📊 Métricas y Rendimiento

### Métricas disponibles

El CLI proporciona las siguientes métricas:

- **⏱️ Tiempo total de ejecución**
- **🚀 Speedup estimado** (vs ejecución secuencial)
- **🔧 Workers utilizados**
- **📂 Portfolios procesados** (exitosos/fallidos)
- **📈 Tasa de éxito**
- **📊 Tiempo promedio por portfolio**
- **💻 Información del sistema** (CPU, RAM)

### Ejemplo de output

```
📊 RESULTADO FINAL:
✅ Éxito: SÍ
📝 Mensaje: Pipeline paralelo completado: 15/15 exitosos
⏱️ Duración: 45.23 segundos

📈 MÉTRICAS DETALLADAS:
   🔧 Workers utilizados: 4
   📂 Portfolios procesados: 15
   ✅ Exitosos: 15
   ❌ Fallidos: 0
   📈 Tasa de éxito: 100.0%
   🚀 Speedup: 3.2x
   📊 Tiempo promedio por portfolio: 3.02s
```

### Optimización de rendimiento

#### Configuración recomendada por escenario:

| Escenario | Configuración recomendada |
|-----------|---------------------------|
| **Pocos portfolios (<5)** | `--mode standard` |
| **Portfolios medianos (5-20)** | `--mode parallel --workers 4` |
| **Muchos portfolios (>20)** | `--mode parallel --workers 8` |
| **I/O intensivo** | `--execution-mode thread` |
| **CPU intensivo** | `--execution-mode process` |

#### Factores que afectan el rendimiento:

- **Número de portfolios activos**
- **Tamaño de los archivos en S3**
- **Latencia de red a S3/PostgreSQL**
- **Recursos del sistema (CPU, RAM)**
- **Número de workers configurados**

## 🛡️ Consideraciones de Seguridad

### Variables de entorno requeridas

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@host:port/database

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Opcional
S3_BUCKET_NAME=your_bucket_name
```

### Mejores prácticas

- ✅ Usar variables de entorno para credenciales
- ✅ Ejecutar `--dry-run` antes de procesamientos grandes
- ✅ Monitorear logs en modo `--verbose` para debugging
- ✅ Usar `--quiet` en scripts automatizados
- ✅ Configurar timeouts apropiados para conexiones

## 📞 Soporte y Contribución

### Reportar problemas

1. Ejecutar `python main.py --show-config --verbose`
2. Incluir el output completo en el reporte
3. Especificar la configuración de sistema y argumentos usados

### Desarrollar nuevas características

El CLI está diseñado para ser extensible:

- **Agregar nuevos argumentos** en `create_parser()`
- **Implementar validaciones** en `validate_args()`
- **Extender métricas** en `print_results()`

---

## 📋 Resumen de Comandos

### Comandos más utilizados

```bash
# Uso básico
python main.py

# Configuración y estado
python main.py --show-config
python main.py --list-portfolios

# Procesamiento con fechas
python main.py --days 7 --mode parallel
python main.py --start 2025-04-30 --end 2025-05-01

# Testing
python main.py --dry-run --verbose

# Producción
python main.py --yesterday --mode parallel --quiet
```

### Referencia rápida de argumentos

| Argumento | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--start` | Fecha de inicio | `--start 2025-04-30` |
| `--end` | Fecha de fin | `--end 2025-05-01` |
| `--days` | Últimos N días | `--days 7` |
| `--mode` | Modo de procesamiento | `--mode parallel` |
| `--workers` | Número de workers | `--workers 4` |
| `--verbose` | Información detallada | `--verbose` |
| `--quiet` | Información mínima | `--quiet` |
| `--dry-run` | Simulación | `--dry-run` |

---

**Versión**: 1.0.0  
**Última actualización**: Enero 2025  
**Mantenedor**: Strix System Team