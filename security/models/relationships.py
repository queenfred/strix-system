from sqlalchemy import Table, Column, Integer, ForeignKey
from security.models.base import Base

user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", Integer, ForeignKey("public.users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("public.roles.id"), primary_key=True),
    schema="public"
)

role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", Integer, ForeignKey("public.roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("public.permissions.id"), primary_key=True),
    schema="public"
)
