import pymysql.cursors
from db import location_db

def searchParkDB(word):
    connection = location_db()

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
    connection = location_db()

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