from fastapi import APIRouter, HTTPException
from api.schemas.role import RoleSchema
from security.services.access_control_service import AccessControlService

router = APIRouter(prefix="/roles", tags=["Roles"])
access_service = AccessControlService()

@router.post("/", response_model=RoleSchema, summary="Crear un nuevo rol")
def create_role(role: RoleSchema):
    created = access_service.create_role(name=role.name, description=role.description)
    if not created:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    return created

@router.get("/{name}", response_model=RoleSchema, summary="Obtener un rol por nombre")
def get_role(name: str):
    role = access_service.get_or_create_role(name=name)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role
