from fastapi import FastAPI

from endpoints.general import router as general_router
from endpoints.import_db import router as import_db_router
from endpoints.projects import router as projects_router
from endpoints.crud import router as crud_router
from endpoints.auth import router as auth_router

def include_routers(app: FastAPI):
    app.include_router(general_router)
    app.include_router(import_db_router)
    app.include_router(projects_router)
    app.include_router(crud_router)
    app.include_router(auth_router)
