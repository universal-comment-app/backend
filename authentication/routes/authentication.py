import os

from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import json
import requests
from dotenv import load_dotenv
load_dotenv(verbose=True)

rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
from users.schemas.users import (
    UserInLogin,
    UserInResponse,
)

router = APIRouter()


def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True) -> UserInResponse:
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })
    FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_WEB_API_KEY')
    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    token = r.json().get("idToken", None)
    if token is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=r.json()["error"]["message"]
        )
    userInResponse = UserInResponse(token)
    return userInResponse


@router.post("/login", name="auth:login")
async def login(user_login: UserInLogin = Body(..., embed=True, alias="user")):
    user = sign_in_with_email_and_password(email=user_login.email, password=user_login.password,
                                                 return_secure_token=True)
    return user.__dict__