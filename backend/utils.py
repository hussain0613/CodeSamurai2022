import json

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


def db_init(config:dict):
    DB_URL = config["DATABASE_URL"]
    if DB_URL.startswith("sqlite"):
        
        engine: sa.engine.Engine = sa.create_engine(
            DB_URL, 
            connect_args = {'check_same_thread': config["DB_CHECK_SAME_THREAD"]},
            echo = config["DB_ECHO"]
        )
    else:
        # POOL_SIZE = config["DB_POOL_SIZE"]
        # MAX_OVERFLOW = config["DB_POOL_MAX_OVERFLOW"]
        
        engine: sa.engine.Engine = sa.create_engine(
            config["DATABASE_URL"], 
            # pool_size = POOL_SIZE, 
            # max_overflow = MAX_OVERFLOW,
            echo = config.get("DB_ECHO", False)
        )
    
    Base = declarative_base(bind=engine, metadata=sa.MetaData(naming_convention=naming_convention))
    Session: sessionmaker = sessionmaker(bind = engine)
    return engine, Base, Session

def get_config() -> dict:
    with open("settings.json") as f:
        settings = json.load(f)
    return settings


def get_cors_settings() -> dict:
    
    try:
        with open("cors_settings.json") as f:
            cors_settings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cors_settings = {
            "origins": ["*"],
            "credentials": False,
            "methods": ["*"],
            "headers": ["*"],
        }
        with open("cors_settings.json", "w") as f:
            json.dump(cors_settings, f)
    
    return cors_settings