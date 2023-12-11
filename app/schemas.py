from datetime import datetime


def initial_post(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
    }


def list_posts(posts) -> list:
    return[initial_post(post) for post in posts]