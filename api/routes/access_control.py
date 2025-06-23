from fastapi import APIRouter, HTTPException
from api.schemas.access_control import AssignRoleSchema, AssignPermissionSchema
from security.services.access_control_service import AccessControlService


router = APIRouter(prefix="/access", tags=["Access Control"])
service = AccessControlService()

@router.post("/assign-role", summary="Asignar rol a usuario")
def assign_role(data: AssignRoleSchema):
    ok = service.assign_role_to_user(user_id=data.user_id, role_id=data.role_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Error asignando el rol")
    return {"message": "Rol asignado correctamente"}

@router.post("/assign-permission", summary="Asignar permiso a rol")
def assign_permission(data: AssignPermissionSchema):
    ok = service.assign_permission_to_role(role_id=data.role_id, permission_id=data.permission_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Error asignando el permiso")
    return {"message": "Permiso asignado correctamente"}
