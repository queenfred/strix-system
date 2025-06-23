from pydantic import BaseModel

class AssignRoleSchema(BaseModel):
    user_id: int
    role_id: int

class AssignPermissionSchema(BaseModel):
    role_id: int
    permission_id: int
