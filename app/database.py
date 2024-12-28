from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

postgres_user = 'postgres'
postgres_password = urllib.parse.quote_plus('Chennai@05')
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db_name = 'fastapi'
postgres_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db_name}'

engine = create_engine(postgres_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()