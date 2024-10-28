from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine

DB_URL = f"postgresql://postgres:bhavesh@localhost:5432/employee"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine,autoflush=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
