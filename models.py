from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class PostStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    status = Column(Enum(PostStatus), default=PostStatus.draft, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
