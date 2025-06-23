from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from security.models.base import Base
from security.models.relationships import user_roles, role_permissions

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from security.models.user import User
    from security.models.permission import Permission

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }