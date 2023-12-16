from fastapi import APIRouter, HTTPException, status, Depends, Header, Request, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, utils, oauth2
from bson import ObjectId
from typing import Annotated
from jose import jwt


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
async def login(user_credentials: models.User, responses: Response):
    
    user_query = database.collection_users.find_one({"email": user_credentials.email})
    
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with email: {user_credentials.email} to login!")
    
    user = schemas.initial_user(user_query)
    
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_credentials.password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password!")
    
    access_token = oauth2.create_access_token(data = {"id": user["id"]})
    
    responses.set_cookie("access_token", access_token, httponly=True)
    
    return {
        "Message": f"Login with email: {user_credentials.email} successful!", 
        "current_user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(responses: Response):
    
    responses.delete_cookie("access_token", secure=True, samesite=None)

    return {"Message": f"Logout!"}
