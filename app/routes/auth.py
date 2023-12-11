from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, utils
from bson import ObjectId
from typing import Annotated


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user_query = database.collection_users.find_one({"email": user_credentials.username})
    user = schemas.initial_user(user_query)
    
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    if not utils.verify(user_credentials.password, user.get('password')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Password!")
    
    # print(user)
    
    return {"data": user}

