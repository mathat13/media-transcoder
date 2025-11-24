from sqlalchemy import Column, Integer, String, DateTime, create_engine, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

DATABASE_URL = "sqlite:///./jobs.db"  # SQLite file

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String, nullable=False)           # e.g. "movie" or "episode"
    source_path = Column(String, nullable=False)        # original file path
    output_path = Column(String, nullable=True)         # final transcoded file
    status = Column(String, default="pending")          # current workflow state
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    # metadata = Column(JSON, nullable=True)              # optional extra info

# Create the table
Base.metadata.create_all(bind=engine)