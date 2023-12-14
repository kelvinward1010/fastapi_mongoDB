from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.get("/")
async def get_comments():
    
    comments = schemas.list_comments(database.collection_comments.find())
    return comments


@router.post("/create/{id}", status_code=status.HTTP_201_CREATED)
async def create_post(id, comment: models.Comment, current_user = Depends(oauth2.get_current_user)):
    
    post = schemas.initial_post(database.collection_posts.find_one({"_id": ObjectId(id)}))
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    comment_add = database.collection_comments.insert_one(dict(comment, created_at = datetime.utcnow(), owner_id = current_user['id'], post_id = id))
    
    comment_after_created = database.collection_comments.find_one({"_id": ObjectId(comment_add.inserted_id)})
    
    return {"data": schemas.initial_comment(comment_after_created), "Message": "Created successfully!!!", }


@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_comment(id, comment: models.Comment):
    
    comment_find_and_update = database.collection_comments.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(comment)
    })
    
    if not comment_find_and_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found comment with id: {id}")
    
    comment_after_update = database.collection_comments.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_comment(comment_after_update)}


@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_comment(id):
    comment_find_delete = database.collection_comments.find_one_and_delete({"_id": ObjectId(id)})
    
    if not comment_find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found comment with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}