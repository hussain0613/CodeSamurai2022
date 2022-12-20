from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import csv

from app import config

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