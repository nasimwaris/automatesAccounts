from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
db
DATABASE_URL = DATABASE_URL = "sqlite:///C:/Users/Nasim/Downloads/sqlite-tools-win-x64-3490200/receipts.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
