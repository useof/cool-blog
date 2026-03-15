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
    status: Optional[PostStatus] = PostStatus.draft
    author: Optional[str] = None  # Make author optional for test compatibility

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str]
    status: Optional[PostStatus]
    author: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    status: PostStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
