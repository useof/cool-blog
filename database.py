from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Post, PostStatus

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# --- Post CRUD operations ---

def get_posts_paginated(db, page: int = 1, size: int = 10, only_published: bool = True):
    query = db.query(Post)
    if only_published:
        query = query.filter(Post.status == PostStatus.published)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, total

def get_post_by_id(db, post_id: int, only_published: bool = True):
    query = db.query(Post).filter(Post.id == post_id)
    if only_published:
        query = query.filter(Post.status == PostStatus.published)
    return query.first()

def create_post(db, post_data):
    post = Post(**post_data)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def update_post(db, post_id: int, update_data):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    for key, value in update_data.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    db.delete(post)
    db.commit()
    return True
