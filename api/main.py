from fastapi import FastAPI
from fastapi.responses import JSONResponse
from security.services.health_check import health_check
from api.routes import users, roles, permissions ,access_control,event_domain

app = FastAPI(title="Strix System API")

@app.get("/health", summary="Verifica el estado de PostgreSQL y S3")
def get_health_status():
    return JSONResponse(content=health_check())

# Incluir routers
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)

app.include_router(access_control.router)
app.include_router(event_domain.router)