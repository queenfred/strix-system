from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from security.models.base import Base
from security.models.relationships import role_permissions

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }