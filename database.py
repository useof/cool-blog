from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# --- Post CRUD helpers for tests and API ---
def get_post_by_id(db, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db, skip: int = 0, limit: int = 10, published_only: bool = True):
    query = db.query(Post)
    if published_only:
        query = query.filter(Post.status == 'published')
    return query.offset(skip).limit(limit).all()

def create_post(db, post):
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def update_post(db, db_post, updates: dict):
    for key, value in updates.items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db, db_post):
    db.delete(db_post)
    db.commit()
