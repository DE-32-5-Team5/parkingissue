import pymysql.cursors
from db import location_db

def select_park_info(park_id):
    connection = location_db()

    with connection:
        with connection.cursor() as cursor:
            # Prepare SQL query
            # i = parkid
            # f = 가격
            # o = 운영 시간
            sql = """
            SELECT
                i.park_id AS park_id,
                f.free_time AS free_time,
                f.basic_time AS basic_time,
                f.basic_charge AS basic_charge,
                f.additional_time AS additional_time,
                f.additional_charge AS additional_charge,
                f.daily_charge AS daily_charge,
                f.monthly_charge AS monthly_charge,
                o.wee_orn_st AS wee_orn_st,
                o.wee_orn_et AS wee_orn_et,
                o.wk_orn_st AS wk_orn_st,
                o.wk_orn_et AS wk_orn_et,
                o.hol_orn_st AS hol_orn_st,
                o.hol_orn_et AS hol_orn_et,
                r.park_total AS park_total,
                TIME_TO_SEC(TIMEDIFF(o.wee_orn_et, o.wee_orn_st)) AS weekly,
                TIME_TO_SEC(TIMEDIFF(o.wk_orn_et, o.wk_orn_st)) AS weekend,
                TIME_TO_SEC(TIMEDIFF(o.hol_orn_et, o.hol_orn_st)) AS holiday
            FROM
                parkingarea_info AS i
            LEFT JOIN
                parkingarea_fee AS f ON i.park_id = f.park_id
            LEFT JOIN
                parkingarea_opertime AS o ON i.park_id = o.park_id
            LEFT JOIN
                parkingarea_realtime AS r ON i.park_id = r.park_id
            WHERE
                i.park_id = %s;
            """
            # Execute the query with proper parameterization
            cursor.execute(sql, (park_id,))
            result = cursor.fetchone()
            return result

def related_data(text: str, cls: str, lat: float, lon: float):
    connection = location_db()
    if cls == 'park':
        with connection:
            with connection.cursor() as cursor:
                sql = f"""
                SELECT park_nm AS {text}
                FROM (
                    SELECT park_nm,
                        (
                            6371 * acos(
                                cos(radians({lat})) * cos(radians(park_la)) *
                                cos(radians(park_lo) - radians({lon})) +
                                sin(radians({lat})) * sin(radians(park_la))
                            )
                        ) AS distance
                    FROM parkingarea_info
                    WHERE park_nm LIKE '%{text}%'
                ) AS subquery
                ORDER BY distance ASC
                LIMIT 5;
                """
                cursor.execute(sql,)
                result = cursor.fetchall()
                return result
    else:
        with connection:
            with connection.cursor() as cursor:
                sql = f"""
                SELECT title AS {text}
                FROM (
                    SELECT title,
                        (
                            6371 * acos(
                                cos(radians({lat})) * cos(radians(mapy)) *
                                cos(radians(mapx) - radians({lon})) +
                                sin(radians({lat})) * sin(radians(mapx))
                            )
                        ) AS distance
                    FROM festival_info
                    WHERE title LIKE '%{text}%'
                ) AS subquery
                ORDER BY distance ASC
                LIMIT 5;
                """
                cursor.execute(sql,)
                result = cursor.fetchall()
                return result
