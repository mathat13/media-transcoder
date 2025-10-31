import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db import Base
from factories import JobFactory
from main import app, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    """Fresh DB session for each test."""
    session = TestingSessionLocal()
    JobFactory._meta.sqlalchemy_session = session

    session.begin_nested()

    # Override FastAPI DB dependency for this test only
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.rollback()
    session.close()
