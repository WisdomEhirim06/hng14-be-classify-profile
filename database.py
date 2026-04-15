import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from a .env file (for local development)
load_dotenv()

# Get the Supabase connection string from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy requires the URL to start with "postgresql://" 
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the engine connected to Supabase
# pool_pre_ping=True prevents crashes from stale serverless connections
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()