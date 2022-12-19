from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import csv

from utils import get_cors_settings

cors_settings = get_cors_settings()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings["origins"],
    allow_credentials=cors_settings["credentials"],
    allow_methods=cors_settings["methods"],
    allow_headers=cors_settings["headers"],
)

@app.get("/")
def index():
    return "Hellow World"


@app.get("/get_projects/")
def get_projects():
    
    projects = []
    headers = []
    
    with open("projects.csv", "r") as csv_file:
        projects = list(csv.reader(csv_file))
    
    return projects


