
Write-Host "⏳ Elevando permisos para ejecutar tests..." -ForegroundColor Cyan

powershell -ExecutionPolicy Bypass -File ".\scripts\run_selected_tests.ps1"
