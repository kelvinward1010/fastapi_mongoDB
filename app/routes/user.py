from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, utils, oauth2
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
async def create_user(user: models.User):
    
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    user_add = database.collection_users.insert_one(dict(user, created_at = datetime.utcnow()))
    
    if not user_add:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Can't create user!")
    
    user_after_created = database.collection_users.find_one({"_id": ObjectId(user_add.inserted_id)})
    
    return {"data": schemas.initial_user(user_after_created), "Message": "Created successfully!!!"}

@router.post("/create_many", status_code=status.HTTP_201_CREATED)
async def create_many_user(users: list[models.User]):
    
    for user in users:
        dict(user)
        hashed_password = utils.has_password(user.password)
        user.password = hashed_password
    
    users_add = database.collection_users.insert_many(list(dict(user, created_at = datetime.utcnow()) for user in users))

    users_convert_ids = users_add.inserted_ids
    
    users_after_created = schemas.list_users(database.collection_users.find_one({"_id": ObjectId(post_id)}) for post_id in users_convert_ids)
    
    return {
        "data": users_after_created, 
        "Message": "Created many successfully!!!", 
    }

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

@router.put("/update_user_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id, user: models.User, current_user = Depends(oauth2.get_current_user)):
    
    find_user_check_owner = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not find_user_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to update!")
    
    if str(find_user_check_owner['_id']) != str(current_user['id']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to updated!")
    else:
        hashed_password = utils.has_password(user.password)
        user.password = hashed_password
        
        database.collection_users.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(user)
        })
    
    user_after_update = database.collection_users.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_user(user_after_update)}

@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id):
    
    find_user_delete = database.collection_users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not find_user_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id}")
    
    return {"Message": f"Delete successfully with id {id}"}

@router.delete("/delete_user_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id, current_user = Depends(oauth2.get_current_user)):
    
    find_user_check_owner = database.collection_users.find_one({"_id": ObjectId(id)})
    
    if not find_user_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found user with id: {id} to delete!")
    
    if str(find_user_check_owner['_id']) != str(current_user['id']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete!")
    else:
        database.collection_users.find_one_and_delete({"_id": ObjectId(id)})
    
    return {"Message": f"Delete successfully with id {id}"}