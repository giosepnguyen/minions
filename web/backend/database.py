import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Đọc thông tin từ file .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Chuỗi kết nối tới MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo "engine" - cầu nối chính tới database
engine = create_engine(DATABASE_URL)

# Tạo phiên làm việc (session) để truy vấn dữ liệu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để các "model" (bảng) sau này kế thừa
Base = declarative_base()

# Hàm này dùng để lấy 1 kết nối DB mỗi khi cần
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()