from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserResponse
    created_at: datetime

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    exp: datetime


class VoteCreate(BaseModel):
    post_id: int
    # pydantic.conint() can be used to set more restrictions on integer values
    vote_direction: conint(le=1, ge=0)
