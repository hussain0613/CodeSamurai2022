import datetime
import jwt
import bcrypt

from sqlalchemy.orm.session import Session


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
        "dt1": bcrypt.hashpw(uid.encode(), bcrypt.gensalt()).decode(),
        "scope": scope,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = duration)
    }
    return jwt.encode(payload, secret_key)


