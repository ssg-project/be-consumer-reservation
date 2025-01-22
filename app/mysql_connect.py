from app.config import DB_HOST, DB_PASS, DB_NAME, DB_USER
import pymysql

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
