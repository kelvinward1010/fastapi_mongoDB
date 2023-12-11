from datetime import datetime

def initial_user(user) -> dict:
    return {
        "id": str(user["_id"]),
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
        "created_at": post["created_at"],
    }

def list_posts(posts) -> list:
    return [initial_post(post) for post in posts]