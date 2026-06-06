import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Read from environment variable (set by docker-compose), fallback to local dev
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://osint:osint123@localhost:5432/osint_db"
)

# The engine is the core interface to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of this SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemy 2.0-style declarative base
class Base(DeclarativeBase):
    pass


# Dependency to get the database session in our API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
