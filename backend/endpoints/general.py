from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import csv

from app import config
from models.db import model_map
from auth_utils import auth_dependency_factory

router = APIRouter(tags=["general"])

@router.get("/")
def index():
    
    if(config.get("INDEX_REDIRECT")): 
        return RedirectResponse(config["INDEX_REDIRECT"])
    
    return "Hellow World"
    

@router.get("/get_projects/", tags=["project"])
def get_projects():
    
    projects = []
    with open("projects.csv", "r") as csv_file:
        projects = list(csv.reader(csv_file))
    
    return projects

@router.get("/get_model_names/")
def get_model_names(_ = Depends(auth_dependency_factory(["SYSADMIN"]))):
    return list(model_map.keys())