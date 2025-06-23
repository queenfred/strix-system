from pydantic import BaseModel, ConfigDict

class PermissionSchema(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
