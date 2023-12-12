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
    
#Posts
class Post(BaseModel):
    title: str
    content: str
    
class PostCreate(Post):
    created_at: datetime
    
    class Config:
        from_attributes = True