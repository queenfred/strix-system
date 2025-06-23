from fastapi import APIRouter, HTTPException
from api.schemas.permission import PermissionSchema
from security.services.access_control_service import AccessControlService

router = APIRouter(prefix="/permissions", tags=["Permissions"])
access_service = AccessControlService()

@router.post("/", response_model=PermissionSchema, summary="Crear un nuevo permiso")
def create_permission(permission: PermissionSchema):
    created = access_service.create_permission(name=permission.name, description=permission.description)
    if not created:
        raise HTTPException(status_code=400, detail="El permiso ya existe")
    return created

@router.get("/{name}", response_model=PermissionSchema, summary="Obtener un permiso por nombre")
def get_permission(name: str):
    existing = access_service.get_or_create_permission(name=name)
    if not existing:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return existing
