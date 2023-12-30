from datetime import datetime

def initial_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": user["email"],
        "password": user["password"],
        "created_at": user["created_at"],
    }

def list_users(users) -> list:
    return [initial_user(user) for user in users]

#Post
def initial_post(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "owner_id": post["owner_id"],
        "likes": post["likes"],
        "created_at": post["created_at"],
    }

def list_posts(posts) -> list:
    return [initial_post(post) for post in posts]


#Comment
def initial_comment(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "content": comment["content"],
        "owner_id": comment["owner_id"],
        "post_id": comment["post_id"],
        "created_at": comment["created_at"],
    }

def list_comments(comments) -> list:
    return [initial_comment(comment) for comment in comments]


#Conversation
def initial_conversation(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "user_1": conversation["userId_1"],
        "user_2": conversation["userId_2"],
        "created_at": conversation["created_at"],
    }

def list_conversations(conversations) -> list:
    return [initial_conversation(conversation) for conversation in conversations]

#Conversation
def initial_message(message) -> dict:
    return {
        "id": str(message["_id"]),
        "content": message["content"],
        "conversation_id": message['conversation_id'],
        "owner_id": message["owner_id"],
        "created_at": message["created_at"],
    }

def list_messages(messages) -> list:
    return [initial_message(message) for message in messages]