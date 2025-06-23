@echo off
REM run_pipeline.bat - Script para ejecutar el pipeline desde Windows
REM PS C:\code\strix-system> .\pipeline\pipeline_run_script.bat

echo ==========================================
echo    STRIX PORTFOLIO PIPELINE LAUNCHER
echo ==========================================

REM Verificar si estamos en el directorio correcto
if not exist "venv" (
    echo ❌ Error: No se encuentra el directorio venv
    echo 💡 Ejecuta este script desde la raiz del proyecto
    echo    Ejemplo: C:\code\strix-system\
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está disponible en el entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado

REM Navegar al directorio pipeline
cd pipeline

REM Ejecutar el pipeline
echo 🚀 Ejecutando pipeline...
echo.
python main.py

REM Capturar código de salida
set EXIT_CODE=%ERRORLEVEL%

REM Volver al directorio raíz
cd ..

REM Mostrar resultado final
echo.
echo ==========================================
if %EXIT_CODE% == 0 (
    echo ✅ PIPELINE COMPLETADO EXITOSAMENTE
) else (
    echo ❌ PIPELINE FALLÓ ^(Código: %EXIT_CODE%^)
)
echo ==========================================

pause
exit /b %EXIT_CODE%
