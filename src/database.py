import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Read from environment variable (set by docker-compose), fallback to local dev
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://osint:osint123@localhost:5432/osint_db"
)

# The engine is the core interface to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of this SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our database models will inherit from this Base class
Base = declarative_base()

# Dependency to get the database session in our API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Why we are doing this (Plumbing): This script acts as the master key. The get_db function is especially important—it ensures that every time a user makes an API request, we open a database connection, do our work, and safely close it so the server doesn't crash from too many open connections.
