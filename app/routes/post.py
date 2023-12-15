from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/")
async def get_posts():
    
    posts = schemas.list_posts(database.collection_posts.find())
    return posts

@router.get("/posts_follow_token")
async def get_posts(current_user = Depends(oauth2.get_current_user)):
    
    posts = schemas.list_posts(database.collection_posts.find({"owner_id": current_user['id']}))
    
    return posts

@router.get("/find_post/{id}")
async def find_post(id):
    post = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": schemas.initial_post(post)}

@router.get("/find_post_has_comments/{id}")
async def find_post_has_comments(id):
    post = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    comments_in_post = schemas.list_comments(database.collection_comments.find({"post_id": id}))
    
    config_post = dict(schemas.initial_post(post), comments = comments_in_post)
    
    return {"data": config_post}

@router.get("/posts_with_everthing")
async def find_post_has_comments():
    
    posts = schemas.list_posts(database.collection_posts.find())
    
    comments_in_posts = list(dict(post, comments = schemas.list_comments(database.collection_comments.find({"post_id": post['id']}))) for post in posts)
    
    return {"data": comments_in_posts}

@router.get("/search")
async def get_search_posts(search):
    
    myquery_title = { "title": { "$regex": search }}
    myquery_content = { "content": { "$regex": search }}
    posts_query_title = schemas.list_posts(database.collection_posts.find(myquery_title))
    
    
    if not posts_query_title:
        posts_query_content = schemas.list_posts(database.collection_posts.find(myquery_content))
        
        if not posts_query_content:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with query: {search}")
        
        return posts_query_content
    
    return posts_query_title

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: models.Post, current_user = Depends(oauth2.get_current_user)):
    post_add = database.collection_posts.insert_one(dict(post, created_at = datetime.utcnow(), owner_id = current_user['id'], likes = []))
    
    post_after_created = database.collection_posts.find_one({"_id": ObjectId(post_add.inserted_id)})
    
    return {"data": schemas.initial_post(post_after_created), "Message": "Created successfully!!!", }

@router.post("/create_many", status_code=status.HTTP_201_CREATED)
async def create_many_post(posts: list[models.Post], current_user = Depends(oauth2.get_current_user)):
    
    posts_add = database.collection_posts.insert_many(list(dict(post, created_at = datetime.utcnow(), owner_id = current_user['id'], likes = []) for post in posts))
    
    posts_convert_ids = posts_add.inserted_ids
    
    posts_after_created = schemas.list_posts(database.collection_posts.find_one({"_id": ObjectId(post_id)}) for post_id in posts_convert_ids)
    
    return {
        "data": posts_after_created, 
        "Message": "Created many successfully!!!", 
    }

@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: models.Post):
    
    post_find_and_update = database.collection_posts.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(post)
    })
    
    if not post_find_and_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    post_after_update = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_post(post_after_update)}

@router.put("/update_post_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: models.Post, current_user = Depends(oauth2.get_current_user)):
    
    find_post_check_owner = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not find_post_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    if find_post_check_owner['owner_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to updated!")
    else:
        database.collection_posts.find_one_and_update({"_id": ObjectId(id)},{
            "$set": dict(post)
        })
    
    post_after_update = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_post(post_after_update)}


@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id):
    post_find_delete = database.collection_posts.find_one_and_delete({"_id": ObjectId(id)})
    
    if not post_find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}

@router.delete("/delete_post_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id, current_user = Depends(oauth2.get_current_user)):
    
    find_post_check_owner = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not find_post_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    if find_post_check_owner['owner_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete!")
    else:
        database.collection_posts.find_one_and_delete({"_id": ObjectId(id)})
    
    return {"data": f"Delete successfully with id {id}"}

@router.delete("/delete_post_and_all_comment/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post_and_all_comment(id):
    
    find_post_check_owner = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not find_post_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    database.collection_posts.find_one_and_delete({"_id": ObjectId(id)})
    
    comments_in_post = schemas.list_comments(database.collection_comments.find({"post_id": id}))
    
    database.collection_comments.delete_many({"post_id": id})
    
    return {"data": f"Delete successfully with id {id}", "data have been deleted": comments_in_post}
