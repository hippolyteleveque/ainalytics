from typing import Optional, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, UTC
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from sqlmodel import Session, select
from google.oauth2 import id_token
from google.auth.transport import requests

from ainalytics.config import settings
from ainalytics.database import engine

from .models import User
from .utils import create_hash
from .schemas import UserBase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = settings.OAUTH_SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Fetch the user from your database
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


def get_user_by_id(user_id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with email {user_id} not found",
        )
    return user


def create_user(email: str, password: str = None):
    if password is not None:
        hashed_password_binary = create_hash(password)
        password = hashed_password_binary.decode("utf-8")
    new_user = User(email=email, password=password)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return new_user


def get_user_by_email(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).one_or_none()
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def google_auth(token: str):
    try:
        # Verify the ID token
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )

        if id_info["aud"] != settings.GOOGLE_CLIENT_ID:
            raise ValueError("Invalid audience")

        return id_info
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


CurrentUser = Annotated[UserBase, Depends(get_current_user)]
