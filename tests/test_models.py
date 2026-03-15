import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from models import Base, Post, PostStatus
from datetime import datetime

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_post_required_fields(db_session):
    post = Post(title="Test Title", content="Test Content", author="Author")
    db_session.add(post)
    db_session.commit()
    assert post.id is not None
    assert post.status == PostStatus.draft
    assert isinstance(post.created_at, datetime)
    assert isinstance(post.updated_at, datetime)


def test_post_status_values(db_session):
    post = Post(title="Test", content="C", author="A", status=PostStatus.published)
    db_session.add(post)
    db_session.commit()
    assert post.status == PostStatus.published
    post2 = Post(title="T2", content="C2", author="A2", status=PostStatus.archived)
    db_session.add(post2)
    db_session.commit()
    assert post2.status == PostStatus.archived


def test_post_missing_required(db_session):
    post = Post(content="C", author="A")
    db_session.add(post)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_post_date_handling(db_session):
    post = Post(title="Date Test", content="C", author="A")
    db_session.add(post)
    db_session.commit()
    assert isinstance(post.created_at, datetime)
    assert isinstance(post.updated_at, datetime)
