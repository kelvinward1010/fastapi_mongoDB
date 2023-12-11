from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class Post(BaseModel):
    title: str
    content: str
    
class PostCreate(Post):
    created_at: datetime
    
    class Config:
        from_attributes = True