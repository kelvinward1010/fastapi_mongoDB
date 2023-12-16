from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal



#Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None


#Users
class User(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(User):
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr
    old_password: str
    password: str
    
    
#Posts
class Post(BaseModel):
    title: str
    content: str
    
class PostCreate(Post):
    created_at: datetime
    owner_id: str
    
    class Config:
        from_attributes = True
        
#Comments
class Comment(BaseModel):
    content: str
    
#Like
class Like(BaseModel):
    isLike: Literal[0,1]