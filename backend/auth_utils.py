import datetime
import jwt
import bcrypt

from fastapi import Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm.session import Session


from app import sessionMaker, config
from models.db import User

def verify_user(username: str, password: str, session: Session) -> User:
    user: User = session.query(User).filter_by(username = username).first()
    if not user:
        raise LookupError("user does not exist")
    
    hashed_pass: str = user.password
    if not bcrypt.checkpw(password.encode(), hashed_pass.encode()):
        raise LookupError("wrong password")
    
    return user



def create_access_token(uid: str, scope: str, duration: float, secret_key: str) -> str:
    
    
    payload = {
        "dt1": uid,
        "scope": scope,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = duration)
    }
    return jwt.encode(payload, secret_key)


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request):
        if not request.headers.get("Authorization"):
            if request.cookies.get("dt2"):
                return request.cookies["dt2"]
            
        return await super().__call__(request)


tokenUrl = "/auth/token"
if config.get("ROOT_PATH"):
    tokenUrl = config["ROOT_PATH"] + tokenUrl

outh2_scheme = CustomOAuth2PasswordBearer(tokenUrl=tokenUrl)


def auth_dependency_factory(required_utypes: list[str] = None, dbSession: Session = None):

    async def authorize(request: Request, token: str = Depends(outh2_scheme)) -> User:
        session: Session = None
        if not dbSession:
            session = sessionMaker()
        else:
            session = dbSession
    
        if token.__class__.__name__ != "str":
            token = await CustomOAuth2PasswordBearer.__call__(outh2_scheme, request)
        
        payload = jwt.decode(token, key = config.get("SECRET_KEY"), algorithms="HS256")

        uid = payload.get("dt1")
        print("...................................................", uid)
        user: User = session.query(User).get(uid)
        if not user:
            if not dbSession:
                session.close()
            raise HTTPException(401)
        
        if required_utypes and user.user_type not in required_utypes:
            if not dbSession:
                session.close()
            raise HTTPException(403)
        
        if not dbSession:
                session.close()

        return user
    
    return authorize
