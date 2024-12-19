import pymysql.cursors

def connect_db():
    connection = pymysql.connect(
        host='127.0.0.1',
        port=6033,
        user='root',
        password='samdul2024$',
        database='parkingissue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection    
# 유저 id 중복 검사
def check_user_id(user_id):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT id
            FROM user_info
            WHERE id = %s;
            """
            cursor.execute(sql, (user_id,))
            result = bool(cursor.fetchone()) #테이블에 아이디 값이 이미 존재하면 true/ 없으면 false
            return result
# 유저 정보 삽입
def insert_user_info(user_name, user_nick, user_id, user_pw):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO user_info (name, nickname, id, password) VALUES (%s, %s, %s, %s)
            """
            result = bool(cursor.execute(sql, (user_name, user_nick, user_id, user_pw)))
            return result