from fastapi import APIRouter, HTTPException, status
from .. import models, schemas, database
from bson import ObjectId

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/")
async def get_posts():
    posts = schemas.list_posts(database.collection_posts.find())
    return posts

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
async def create_post(post: models.Post):
    post_add = database.collection_posts.insert_one(dict(post))
    
    post_after_created = database.collection_posts.find_one({"_id": ObjectId(post_add.inserted_id)})
    
    return {"data": schemas.initial_post(post_after_created), "Message": "Created successfully!!!", }

@router.get("/find_post/{id}")
async def find_post(id):
    post = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": schemas.initial_post(post)}

@router.put("/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id, post: models.Post):
    
    post_find_and_update = database.collection_posts.find_one_and_update({"_id": ObjectId(id)},{
        "$set": dict(post)
    })
    
    if not post_find_and_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    post_after_update = database.collection_posts.find_one({"_id": ObjectId(id)})
    
    return {"data": schemas.initial_post(post_after_update)}


@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id):
    post_find_delete = database.collection_posts.find_one_and_delete({"_id": ObjectId(id)})
    
    if not post_find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post with id: {id}")
    
    return {"data": f"Delete successfully with id {id}"}

