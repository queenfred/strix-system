
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "EJECUTANDO TESTS DE STRIX API" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

# Activar entorno virtual
$venvActivate = ".\.venv\Scripts\Activate.ps1"
if (-Not (Test-Path $venvActivate)) {
    Write-Error "❌ No se encontró el entorno virtual en .venv\Scripts\Activate.ps1"
    exit 1
}
. $venvActivate
Write-Host "Entorno virtual activado." -ForegroundColor Green
Write-Host "-----------------------------------------`n"

# Ejecutar tests de Access Control
Write-Host "EJECUTANDO TESTS: ACCESS CONTROL" -ForegroundColor Yellow
pytest `
  api/test/test_access_control.py::test_assign_permission_to_role `
  api/test/test_access_control.py::test_assign_role_to_user `
  -v

# Ejecutar tests de Users & Roles
Write-Host "`nEJECUTANDO TESTS: USERS & ROLES" -ForegroundColor Yellow
pytest `
  api/test/test_api_endpoints.py::test_create_role `
  api/test/test_api_endpoints.py::test_create_user `
  api/test/test_api_endpoints.py::test_get_role `
  api/test/test_api_endpoints.py::test_get_user `
  api/test/test_api_endpoints.py::test_health_check `
  -v

# Ejecutar tests de Permissions
Write-Host "`nEJECUTANDO TESTS: PERMISSIONS" -ForegroundColor Yellow
pytest `
  api/test/test_permissions.py::test_create_permission `
  api/test/test_permissions.py::test_get_permission `
  -v

Write-Host "`nTodos los tests seleccionados han finalizado." -ForegroundColor Green
