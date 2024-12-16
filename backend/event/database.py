# import os
# from dotenv import load_dotenv, find_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session

# dotenv_path = find_dotenv()
# print("Found .env at:", dotenv_path)

# # .env 파일에서 환경 변수 로드
# load_dotenv(dotenv_path=dotenv_path)

# # print("DB_HOST:", os.getenv('DB_HOST'))
# # print("DB_PORT:", os.getenv('DB_PORT'))

# # 데이터베이스 연결 URL을 환경 변수에서 가져오기
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# # 데이터베이스 연결 URL
# SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # 데이터베이스 엔진 생성
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# # 세션 생성기
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 기본 클래스
# Base = declarative_base()

# # DB 세션을 얻는 함수
# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db  # 이 위치에서 db 세션을 반환
#     finally:
#         db.close()  # 함수가 끝나면 세션을 종료