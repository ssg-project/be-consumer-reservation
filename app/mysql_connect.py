from app.config import DB_HOST, DB_PASS, DB_NAME, DB_USER
import pymysql

# SQLAlchemy 엔진 및 세션 생성
# engine = create_engine(
#     DATABASE_URL,
#     pool_size=10,
#     max_overflow=20,
#     pool_pre_ping=True,
#     pool_recycle=3600,
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def insert_reservation(user_id, concert_id):
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
    )

    cursor = connection.cursor()      
    query = "INSERT INTO reservations (user_id, concert_id) VALUES (%s, %s)"

    try:
        cursor.execute(query, (user_id, concert_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
