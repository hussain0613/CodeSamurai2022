from fastapi import APIRouter

from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query

from app import sessionMaker
from models.db import Project
from models.schema import ProjectSchema

router = APIRouter(prefix = "/project", tags=["project"])

@router.get("/get/")
def get_projects(location: str = None, agency_code: str = None, offset: int = 0, limit: int = None):
    session: Session = sessionMaker()

    query: Query = session.query(Project)
    if (location):
        query = query.filter(Project.location == location)
    if (agency_code):
        query = query.filter(Project.exec_ == agency_code)
    
    query = query.offset(offset).limit(limit)
    
    projects_db: list[Project] = query.all()
    
    session.close()
    
    return projects_db

@router.get("/get_locations/")
def get_locations(offset: int = 0, limit: int = None):
    session: Session = sessionMaker()

    query: Query = session.query(Project.location).distinct(Project.location)
    query = query.offset(offset).limit(limit)
    
    projects_locations_db: list[Project.location] = query.all()
    projects_locations: list[str] = list(map(lambda proj: proj[0], projects_locations_db))
    session.close()
    
    return projects_locations
