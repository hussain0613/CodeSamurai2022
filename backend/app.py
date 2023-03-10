from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from utils import get_config, get_cors_settings, db_init

cors_settings = get_cors_settings()
config = get_config()

engine, Base, sessionMaker = db_init(config)

if(config.get("ROOT_PATH")):
    app = FastAPI(root_path=config["ROOT_PATH"])
else:
    app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings["origins"],
    allow_credentials=cors_settings["credentials"],
    allow_methods=cors_settings["methods"],
    allow_headers=cors_settings["headers"],
)

from endpoints import include_routers
include_routers(app)



