from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Post, PostStatus
from schemas import PostCreate, PostUpdate, PostResponse
from database import SessionLocal, init_db
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

security = HTTPBearer()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fake_verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Accept any non-empty token for testing
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return credentials.credentials

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cool Blog FastAPI backend!"}

# --- POSTS API ---

@app.get("/api/posts", response_model=dict)
def get_posts(page: int = 1, db: Session = Depends(get_db)):
    page_size = 10
    query = db.query(Post).filter(Post.status == PostStatus.published)
    total = query.count()
    items = (
        query.order_by(Post.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "items": [PostResponse.from_orm(post) for post in items],
        "total": total,
        "page": page,
    }

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse.model_validate(post)

@app.post("/api/posts", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db), token: str = Depends(fake_verify_token)):
    db_post = Post(
        title=post.title,
        content=post.content,
        author=post.author if post.author else "testuser",
        status=post.status if post.status else PostStatus.draft,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return PostResponse.model_validate(db_post)

from fastapi import Body

@app.put("/api/posts/{post_id}", response_model=PostResponse)
# already imported Optional and Body at the top

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, db: Session = Depends(get_db), token: str = Depends(fake_verify_token), post_data: dict = Body(...)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        post = PostUpdate(**post_data)
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid payload")
    update_data = post.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=422, detail="No valid fields to update")
    for field, value in update_data.items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)
    return PostResponse.model_validate(db_post)

@app.delete("/api/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), token: str = Depends(fake_verify_token)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return JSONResponse(status_code=204, content=None)

