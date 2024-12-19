import pymysql.cursors

def connect_db():
    connection = pymysql.connect(
        host='10.0.4.80',
        port=6033,
        user='root',
        password='samdul2024$',
        database='parkingissue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def searchParkDB(word):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT park_id, park_nm, park_addr, park_la, park_lo
            FROM parkingarea_info
            WHERE park_nm LIKE '%{word}%'
            LIMIT 1;
            """
            cursor.execute(sql,)
            result = cursor.fetchone()
            return result

def searchHotDB(word):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = f"""
            SELECT contentid, mapx, mapy
            FROM festival_info
            WHERE title LIKE '%{word}%'
            LIMIT 1;
            """
            cursor.execute(sql,)
            result = cursor.fetchone()
            return result