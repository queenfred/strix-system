#!/bin/bash
# Script para ejecutar solo los tests seleccionados de Strix API

pytest \
  api/test/test_access_control.py::test_assign_permission_to_role \
  api/test/test_access_control.py::test_assign_role_to_user \
  api/test/test_api_endpoints.py::test_create_role \
  api/test/test_api_endpoints.py::test_create_user \
  api/test/test_api_endpoints.py::test_get_role \
  api/test/test_api_endpoints.py::test_get_user \
  api/test/test_api_endpoints.py::test_health_check \
  api/test/test_permissions.py::test_create_permission \
  api/test/test_permissions.py::test_get_permission \
  -v
