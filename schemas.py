from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class PostCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    author: Optional[str] = Field(None, max_length=100)
    status: Optional[PostStatus] = PostStatus.draft

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    author: Optional[str] = Field(None, max_length=100)
    status: Optional[PostStatus] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    status: PostStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
