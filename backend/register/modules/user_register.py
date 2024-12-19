import pymysql.cursors
import mysql.connector
def connect_db():
    connection = mysql.connector.connect(
        host='10.0.4.80',
        port=6033,
        user='root',
        password='samdul2024$',
        database='parkingissue',
        auth_plugin='mysql_native_password'  # 또는 'caching_sha2_password'
    )
    return connection

# 유저 id 중복 검사
def check_user_id(user_id):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT user_id
            FROM user_info
            WHERE user_id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone())
            return result

# 유저 정보 삽입
def insert_user_info(user_name, user_nick, user_id, user_pw):
    connection = connect_db()
    print(f"&&&&&& {user_name}, {user_nick}, {user_id}, {user_pw} &&&&&&&&&&")
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO user_info (user_name, user_nick, user_id, user_pw) VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (user_name, user_nick, user_id, user_pw))
                connection.commit()  # 커밋을 명시적으로 수행
                print("데이터 삽입 성공")
                return True
    except Exception as e:
        # 에러 로그 출력
        print("데이터 삽입 중 에러 발생!")
        print(f"에러 메시지: {e}")
        print(f"SQL: {sql}")
        print(f"파라미터: {user_name}, {user_nick}, {user_id}, {user_pw}")
        return False
    finally:
        if connection.is_connected():
            connection.close()
            print("데이터베이스 연결이 닫혔습니다.")
