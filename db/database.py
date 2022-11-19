import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    os.getenv('DATABASE_CONNECTION_STRING'),
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)