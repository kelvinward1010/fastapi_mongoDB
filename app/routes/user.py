from fastapi import APIRouter, HTTPException, status
from .. import models, schemas, database
from bson import ObjectId

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    users = schemas.list_users(database.collection_users.find())
    return users

@router.get("/find_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def find_user(id):
    user = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id}")
    
    return {"data": schemas.initial_user(user)}

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(user: models.UserCreate):
    
    user_add = database.collection_users.insert_one(dict(user))
    
    if not user_add:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't create user!")
    
    post_after_created = database.collection_users.find_one({"_id": ObjectId(user_add.inserted_id)})
    
    return {"data": schemas.initial_user(post_after_created), "Message": "Created successfully!!!", }

@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id):
    
    find_user_delete = database.collection_users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not find_user_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}
