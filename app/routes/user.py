from fastapi import APIRouter, HTTPException, status
from .. import models, schemas, database, utils
from bson import ObjectId
from datetime import datetime

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

@router.get("/search", status_code=status.HTTP_202_ACCEPTED)
async def get_search_users(search):
    
    query_email = { "email": { "$regex": search }}
    users_query = schemas.list_users(database.collection_users.find(query_email))
    
    if not users_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with query: {search}")
    
    return users_query

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(user: models.User):
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    user_add = database.collection_users.insert_one(dict(user, created_at = datetime.utcnow()))
    
    if not user_add:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't create user!")
    
    user_after_created = database.collection_users.find_one({"_id": ObjectId(user_add.inserted_id)})
    
    return {"data": schemas.initial_user(user_after_created), "Message": "Created successfully!!!"}

@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id, user: models.User):
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    find_user_and_update = database.collection_users.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(user)
    })
    
    if not find_user_and_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    
    user_after_update = database.collection_users.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_user(user_after_update)}

@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id):
    
    find_user_delete = database.collection_users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not find_user_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}
