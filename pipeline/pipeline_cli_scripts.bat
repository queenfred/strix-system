REM run_pipeline_cli.bat - Script avanzado para ejecutar el CLI
@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo    STRIX PORTFOLIO PIPELINE CLI
echo ==========================================

REM Verificar directorio
if not exist "venv" (
    echo ❌ Error: Ejecutar desde la raiz del proyecto
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Navegar a pipeline
cd pipeline

REM Ejemplos de uso
echo 🔧 EJEMPLOS DE USO:
echo.
echo 1. Procesamiento básico:
echo    python main.py
echo.
echo 2. Últimos 7 días con modo paralelo:
echo    python main.py --days 7 --mode parallel
echo.
echo 3. Fechas específicas con detalles:
echo    python main.py --start 2025-04-30 --end 2025-05-01 --verbose
echo.
echo 4. Solo eventos de hoy:
echo    python main.py --today
echo.
echo 5. Simulación (dry-run):
echo    python main.py --dry-run --verbose
echo.
echo 6. Ver configuración del sistema:
echo    python main.py --show-config
echo.
echo 7. Listar portfolios activos:
echo    python main.py --list-portfolios
echo.
echo 8. Procesar portfolios específicos:
echo    python main.py --portfolio-ids 1,2,3
echo.

REM Preguntar al usuario qué hacer
echo ¿Qué deseas hacer?
echo [1] Ejecutar configuración básica (fechas por defecto)
echo [2] Mostrar configuración del sistema
echo [3] Listar portfolios activos  
echo [4] Ejecutar con últimos 7 días (modo paralelo)
echo [5] Simulación (dry-run) con detalles
echo [6] Ingreso manual de comando
echo [Q] Salir
echo.
set /p choice="Selecciona una opción [1-6,Q]: "

if /i "%choice%"=="Q" goto :end
if "%choice%"=="1" (
    echo 🚀 Ejecutando configuración básica...
    python main_cli.py
) else if "%choice%"=="2" (
    echo 🔧 Mostrando configuración del sistema...
    python main_cli.py --show-config
) else if "%choice%"=="3" (
    echo 📁 Listando portfolios activos...
    python main_cli.py --list-portfolios
) else if "%choice%"=="4" (
    echo 🚀 Ejecutando últimos 7 días con modo paralelo...
    python main_cli.py --days 7 --mode parallel --verbose
) else if "%choice%"=="5" (
    echo 🧪 Ejecutando simulación con detalles...
    python main_cli.py --dry-run --verbose
) else if "%choice%"=="6" (
    echo 💻 Ingresa tu comando personalizado:
    echo Ejemplo: --start 2025-04-30 --end 2025-05-01 --mode parallel --verbose
    set /p custom_args="Argumentos: "
    echo 🚀 Ejecutando: python main.py !custom_args!
    python main_cli.py !custom_args!
) else (
    echo ❌ Opción inválida
    goto :end
)

REM Capturar resultado
set EXIT_CODE=%ERRORLEVEL%

:end
cd ..
echo.
echo ==========================================
if %EXIT_CODE% == 0 (
    echo ✅ OPERACIÓN COMPLETADA
) else (
    echo ❌ OPERACIÓN FALLÓ
)
echo ==========================================
pause
exit /b %EXIT_CODE%

REM ==================================================
REM pipeline_help.bat - Muestra ayuda completa
REM ==================================================

REM @echo off
REM echo ==========================================
REM echo    STRIX PIPELINE - AYUDA COMPLETA
REM echo ==========================================
REM 
REM call venv\Scripts\activate.bat
REM cd pipeline
REM python main.py --help
REM cd ..
REM pause

REM ==================================================
REM quick_run.bat - Ejecución rápida con parámetros comunes
REM ==================================================

REM @echo off
REM call venv\Scripts\activate.bat
REM cd pipeline
REM 
REM REM Configuración rápida - modifica según necesites
REM python main.py --days 1 --mode parallel --verbose
REM 
REM set EXIT_CODE=%ERRORLEVEL%
REM cd ..
REM 
REM if %EXIT_CODE% == 0 (
REM     echo ✅ Pipeline completado exitosamente
REM ) else (
REM     echo ❌ Pipeline falló
REM )
REM pause
