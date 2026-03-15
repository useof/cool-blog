import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import Post
from pydantic import ValidationError
from schemas import PostCreate, PostUpdate, PostResponse

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Setup in-memory SQLite for SQLAlchemy model tests
def get_session():
    engine = create_engine("sqlite:///:memory:")
    Post.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_post_model_required_fields():
    session = get_session()
    # Should fail: missing required fields
    with pytest.raises(TypeError):
        post = Post()
        session.add(post)
        session.commit()

def test_post_model_status_enum():
    session = get_session()
    # Should fail: invalid status value
    post = Post(title="Test", content="Test content", status="not_a_status")
    session.add(post)
    with pytest.raises(IntegrityError):
        session.commit()

def test_post_model_date_handling():
    session = get_session()
    # Should fail: published_at is not a datetime
    post = Post(title="Test", content="Test content", status="draft", published_at="not_a_date")
    session.add(post)
    with pytest.raises(Exception):
        session.commit()

def test_post_create_schema_validation():
    # Should fail: missing required fields
    with pytest.raises(ValidationError):
        PostCreate()
    # Should fail: invalid status
    with pytest.raises(ValidationError):
        PostCreate(title="Test", content="Test content", status="not_a_status")
    # Should fail: published_at is not a datetime
    with pytest.raises(ValidationError):
        PostCreate(title="Test", content="Test content", status="draft", published_at="not_a_date")

def test_post_update_schema_partial():
    # Should fail: invalid status
    with pytest.raises(ValidationError):
        PostUpdate(status="not_a_status")
    # Should fail: published_at is not a datetime
    with pytest.raises(ValidationError):
        PostUpdate(published_at="not_a_date")

def test_post_response_schema():
    # Should fail: missing required fields
    with pytest.raises(ValidationError):
        PostResponse()
