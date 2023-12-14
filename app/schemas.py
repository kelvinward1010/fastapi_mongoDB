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