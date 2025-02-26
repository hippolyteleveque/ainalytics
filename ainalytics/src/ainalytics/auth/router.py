from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND


from .service import create_user, get_user_by_email, create_access_token, google_auth
from .utils import verify_hash
from .schemas import UserCreate, UserBase, GoogleAuth


class UserCheck(BaseModel):
    email: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth", tags=["authentication"])
users_router = APIRouter(prefix="/users", tags=["users"])


@auth_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(request.username)
    if not verify_hash(request.password, user.password):
        return HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Bad credentials")

    access_token, expiration_time = create_access_token(
        data={"email": request.username}
    )

    return {
        "access_token": access_token,
        "token_expiration_time": expiration_time,
        "user_id": user.id,
    }


@auth_router.post("/google")
def google(request: GoogleAuth):
    info = google_auth(request.token)
    user = get_user_by_email(info["email"])
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    access_token, expiration_time = create_access_token(data={"email": info["email"]})
    return {
        "access_token": access_token,
        "token_expiration_time": expiration_time,
    }


@users_router.post("/", response_model=UserBase)
def post_users(user: UserCreate):
    # Check if the user already exists
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    # If the user doesn't exist, create a new account
    new_user = create_user(email=user.email, password=user.password)
    return new_user
