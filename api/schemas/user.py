from pydantic import BaseModel, EmailStr, ConfigDict


from typing import List, Optional
from api.schemas.role import RoleSchema

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    roles: List[RoleSchema] = []


