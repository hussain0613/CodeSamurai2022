from fastapi import APIRouter

from sqlalchemy.orm.session import Session

from app import sessionMaker
from models.db import Project
from models.schema import ProjectSchema

router = APIRouter(prefix = "/project", tags=["project"])

@router.get("/get/")
def get_projects():
    session: Session = sessionMaker()

    projects_db: list[Project] = session.query(Project).all()
    projects = list(map(ProjectSchema.from_orm, projects_db))

    session.close()
    
    return projects
