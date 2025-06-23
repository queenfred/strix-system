import sys
import os

# Agregar la ruta al proyecto para importar core desde security
sys.path.append("C:/Desarrollo/strix-system")

import pytest
from security.services.user_service import UserService
from security.services.role_service import RoleService
from security.services.permission_service import PermissionService
from security.services.access_control_service import AccessControlService

@pytest.mark.integration
def test_user_role_permission_integration():
    user_service = UserService()
    role_service = RoleService()
    permission_service = PermissionService()
    access_service = AccessControlService()

    # Crear usuario
    username = "integration_user3"
    email = "integration3@example.com"
    role_name = "role_integration3"
    perm_name = "perm_integration3"

    user = user_service.register_user(
        username=username,
        email=email,
        password="testpass123",
        full_name="Integración Test3"
    )
    assert user is not None

    # Crear permiso
    permission = permission_service.get_or_create_permission(
        name=perm_name,
        description="Permiso de integración3"
    )
    assert permission is not None

    # Crear rol
    role = role_service.get_or_create_role(
        name=role_name,
        description="Rol de integración3"
    )
    assert role is not None

    # Asignar permiso al rol
    assigned_perm = access_service.assign_permission_to_role(role_id=role["id"], permission_id=permission["id"])
    assert assigned_perm is True

    # Asignar rol al usuario
    assigned_role = access_service.assign_role_to_user(user_id=user["id"], role_id=role["id"])
    assert assigned_role is True

    # Autenticar usuario y verificar permisos
    auth = user_service.authenticate(username, "testpass123")
    assert auth is not None
    assert "roles" in auth
    assert any(r["name"] == role_name for r in auth["roles"])

    perms = [p["name"] for r in auth["roles"] for p in r["permissions"]]
    assert perm_name in perms