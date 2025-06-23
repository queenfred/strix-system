from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from api.schemas.permission import PermissionSchema

class RoleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[PermissionSchema] = []

    model_config = ConfigDict(from_attributes=True)
