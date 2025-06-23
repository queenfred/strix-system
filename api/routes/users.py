from fastapi import APIRouter, Depends, HTTPException
from api.schemas.user import UserCreate, UserOut
from security.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
user_service = UserService()

@router.post("/", response_model=UserOut, summary="Crear un nuevo usuario")
def create_user(user: UserCreate):
    created = user_service.register_user(
        username=user.username,
        email=user.email,
        password=user.password,
        full_name=user.full_name
    )
    if not created:
        raise HTTPException(status_code=400, detail="Usuario ya existe o error de validación")
    return created

@router.get("/{username}", response_model=UserOut, summary="Obtener usuario por nombre de usuario")
def get_user(username: str):
    user = user_service.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
