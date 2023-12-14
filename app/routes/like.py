from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, oauth2
from bson import ObjectId

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
async def like(id, like: models.Like, current_user = Depends(oauth2.get_current_user)):
    
    id_current_user = current_user['id']
    
    post = schemas.initial_post(database.collection_posts.find_one({"_id": ObjectId(id)}))
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post has {id} not found!")
    
    find_likes: list = post['likes']
    isReadyLike = False
    for i in find_likes:
        if str(i) == str(id_current_user):
            isReadyLike = True
        else:
            isReadyLike = False
    
    if like.isLike == 1:
        if isReadyLike == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {id_current_user} has already like this post!")
        find_likes.append(id_current_user)
        database.collection_posts.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(post)
        })
        
        return {"message": "Successfully liked this post!"}
    
    if like.isLike == 0:
        if isReadyLike == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exits!")
        find_likes.remove(id_current_user)
        database.collection_posts.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(post)
        })
        
        return {"message": "Successfully remove like on this post!"}


@router.get("/{id}", status_code=status.HTTP_201_CREATED)
async def get_user_liked(id):
    
    post = schemas.initial_post(database.collection_posts.find_one({"_id": ObjectId(id)}))
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post has {id} not found!")
    
    likes: list = post['likes']
    
    users = schemas.list_users(database.collection_users.find_one({"_id": ObjectId(like)}) for like in likes)
    
    return {"data": users}