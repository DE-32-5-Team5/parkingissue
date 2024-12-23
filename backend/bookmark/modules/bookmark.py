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
# bookmarks 테이블 조회
def select_bookmarks_info(idtype, uid, bookmark_longitude, bookmark_latitude):
    connection = connect_db()

    with connection:
        with connection.cursor() as cursor:
            sql = """
            SELECT title, address,
            (6371 * acos(cos(radians(%s)) * cos(radians(mapy)) * 
            cos(radians(mapx) - radians(%s)) + sin(radians(%s)) * sin(radians(mapy)))) AS distance
            FROM festival_info
            WHERE
                fid IN (
                    SELECT fid 
                    FROM user_bookmarks
                    WHERE %s = %s
                )
            ORDER BY distance ASC
            """
            cursor.execute(sql, (bookmark_latitude, bookmark_longitude, bookmark_latitude, idtype, uid))
            result = cursor.fetchall()
            return result