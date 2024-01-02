from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, database, oauth2
from bson import ObjectId
from datetime import datetime
import itertools


router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"]
)



@router.get("/")
async def get_conversations():
    
    conversations = schemas.list_conversations(database.collection_conversations.find())
    return conversations

@router.get("/get_all_conversations_token")
async def get_all_conversations_token(current_user = Depends(oauth2.get_current_user)):
    current_user_id_1 = { "userId_1": current_user['id'] }
    current_user_id_2 = { "userId_2": current_user['id'] }
    conversations_1 = schemas.list_conversations(database.collection_conversations.find(current_user_id_2))
    conversations_2 = schemas.list_conversations(database.collection_conversations.find(current_user_id_1))
    
    if not conversations_1:
        if not conversations_2:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found any conversation in our account!")
        
    list_convert = [conversations_1, conversations_2]
    merged_conversations = list(itertools.chain(*list_convert))
    
    user_in_conversations = list(dict(
                                        id = cverssconvert['id'], 
                                        user_1 = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(cverssconvert['user_1'])})),
                                        user_2 = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(cverssconvert['user_2'])})),
                                        created_at = cverssconvert['created_at']
                                    ) for cverssconvert in merged_conversations)
    
    messages_find = schemas.list_messages(database.collection_messages.find())
    user_in_message = list(dict(message, user = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(message['owner_id'])}))) for message in messages_find)
    
    def get_messages(data, conversation):
        final_msgs = []
        for x in data:
            if x['conversation_id'] == conversation['id']:
                final_msgs.append(x)
        return final_msgs
    
    all_in_conversations = list(dict(converss, 
                                    messages = get_messages(user_in_message, converss),
                                    ) for converss in user_in_conversations)
    
    return {"data": all_in_conversations}

@router.get("/conversation_id/{id}", status_code=status.HTTP_202_ACCEPTED)
async def get_conversations_id(id):
    conversation_find = schemas.initial_conversation(database.collection_conversations.find_one({"_id": ObjectId(id)}))
    
    if not conversation_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found conversation with id: {id}")
    
    user_in_conversation = dict(id = conversation_find['id'], 
                                user_1 = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(conversation_find['user_1'])})),
                                user_2 = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(conversation_find['user_2'])})),
                                created_at = conversation_find['created_at'])
    messages_find = schemas.list_messages(database.collection_messages.find({"conversation_id": conversation_find['id']}))
    messages_in_conversation = await list(dict(message, user = schemas.initial_user(database.collection_users.find_one({"_id": ObjectId(message['owner_id'])}))) for message in messages_find)
    all_in_conversation = await dict(user_in_conversation, messages = messages_in_conversation)
    
    return {"data": all_in_conversation}
    


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_conversation(conversation: models.Conversation, current_user = Depends(oauth2.get_current_user)):
    
    if conversation.userId_1 == current_user['id']:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You can't create a conversation with yourself!")
    
    conversations = schemas.list_conversations(database.collection_conversations.find()) 
    
    for i in conversations:
        if i['user_1'] == current_user['id'] and i['user_2'] == conversation.userId_1 or i['user_1'] == conversation.userId_1 and i['user_2'] == current_user['id']:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You can't create with a conversation exits!")
    
    conversation_add = database.collection_conversations.insert_one(dict(conversation, userId_2 = current_user['id'], created_at = datetime.utcnow()))
    
    conversation_after_created = database.collection_conversations.find_one({"_id": ObjectId(conversation_add.inserted_id)})
    
    return {"data": schemas.initial_conversation(conversation_after_created), "Message": "Created successfully!!!", }


@router.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_conversation(id):
    conversation_find_delete = database.collection_conversations.find_one({"_id": ObjectId(id)})
    
    if not conversation_find_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found conversation with id: {id}")
    
    database.collection_conversations.find_one_and_delete({"_id": ObjectId(id)})
    
    return {"data": f"Delete successfully with id {id}"}