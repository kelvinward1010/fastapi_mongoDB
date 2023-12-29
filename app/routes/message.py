from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, oauth2
from bson import ObjectId
from datetime import datetime

router = APIRouter(
    prefix="/message",
    tags=["Message"]
)


@router.get("/")
async def get_messages():
    
    messages = schemas.list_messages(database.collection_messages.find())
    return messages


@router.post("/create/{id}", status_code=status.HTTP_201_CREATED)
async def create_message(id, message: models.Message, current_user = Depends(oauth2.get_current_user)):
    
    conversation = schemas.initial_conversation(database.collection_conversations.find_one({"_id": ObjectId(id)}))
    
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found conversation with id: {id}")
    
    message_add = database.collection_messages.insert_one(dict(message, created_at = datetime.utcnow(), owner_id = current_user['id'], conversation_id = id))
    
    message_after_created = database.collection_messages.find_one({"_id": ObjectId(message_add.inserted_id)})
    
    return {"data": schemas.initial_message(message_after_created), "Message": "Created successfully!!!", }


@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_message(id):
    message_find_delete = database.collection_messages.find_one({"_id": ObjectId(id)})
    
    if not message_find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found message with id: {id}")
    
    database.collection_messages.find_one_and_delete({"_id": ObjectId(id)})
    
    return {"data": f"Delete successfully with id {id}"}


@router.delete("/delete_follow_token/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_message_follow_token(id, current_user = Depends(oauth2.get_current_user)):
    
    find_message_check_owner = database.collection_messages.find_one({"_id": ObjectId(id)})
    
    if not find_message_check_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found message with id: {id}")
    
    if find_message_check_owner['owner_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete!")
    else:
        database.collection_messages.find_one_and_delete({"_id": ObjectId(id)})
    
    return {"data": f"Delete successfully message with id {id}"}