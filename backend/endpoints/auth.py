import secrets
import json

from fastapi import Request, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

from app import config, sessionMaker
from models.db import User
from auth_utils import create_access_token, verify_user


from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token_via_json")
def get_access_token(creds: dict):
    db: Session = sessionMaker()
    user: User = None

    try:
        user: User = verify_user(creds["username"], creds["password"], db)

    except LookupError as err:
        raise HTTPException(status_code=401)

    dur = 86400 ## 24 hours
    if creds.get("remember_me"):
        dur *= 365 ## 1 year
    
    token = create_access_token(user.uid, "login", dur, config.get("SECRET_KEY"))
    
    db.close()
    
    return {"access_token": token}


@router.post("/token")
def outh2_token(form: OAuth2PasswordRequestForm = Depends()):
    creds: dict = form.__dict__
    return get_access_token(creds)    


@router.post("/login")
def login(creds: dict, request: Request):
    dt2 = request.cookies.get("dt2")
    if dt2:
        raise HTTPException(status_code=403, detail="already logged in, to login with another account please logout first")

    token = get_access_token(creds).get("access_token")

    resp = Response(content= f"successfully logged in")
    resp.set_cookie("dt0", secrets.token_urlsafe(15))
    resp.set_cookie("dt1", secrets.token_urlsafe(15))

    if creds.get("remember_me"): resp.set_cookie("dt2", token, expires=86400*365)
    else: resp.set_cookie("dt2", token)
    resp.set_cookie("dt3", secrets.token_urlsafe(15))
    resp.set_cookie("dt4", secrets.token_urlsafe(15))

    return resp


@router.post("/logout")
def logout():
    resp = Response(content= json.dumps({"detail": f"successfully logged out"}))
    resp.headers["content-type"] = "application/json"
    resp.set_cookie("dt0", "", expires=0)
    resp.set_cookie("dt1", "", expires=0)

    resp.set_cookie("dt2", "", expires=0)
    resp.set_cookie("dt3", "", expires=0)
    resp.set_cookie("dt4", "", expires=0)

    return resp



@router.post("/register")
def register(data: dict):
    """
    Registers a new USER with the given data.
    
    When creating an user with this enpoint user's role i.e user_type is set to "APP" by default and force.
    """
    db: Session = sessionMaker()
    user: User = db.query(User).filter_by(email = data.get("email")).all()
    if user:
        db.close()
        raise HTTPException(status_code=409, detail="user already exists")
    
    data["user_type"] = "APP"

    user = User(** data)

    try:
        db.add(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        db.close()
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    
    db.commit()

    db.close()
    return {"detail": "User created successfully. You can now login with your new password"}

    
