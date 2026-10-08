import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print("=== DATABASE CONFIG CHECK ===")
print("DB_USER:", DB_USER)
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)
print("DB_NAME:", DB_NAME)
print("DB_PASSWORD:", "SET" if DB_PASSWORD else "MISSING")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise RuntimeError(
        "Missing database environment variables. "
        "Required: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME"
    )

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 10
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
